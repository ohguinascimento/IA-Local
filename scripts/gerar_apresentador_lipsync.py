"""
Pipeline Automatizado: Gerador de Apresentador com Lip-Sync Realista
Gera a voz em Português via TTS e aciona o ComfyUI (Wav2Lip) para sincronizar os lábios do apresentador.
"""

import os
import sys
import json
import time
import asyncio
import subprocess
import urllib.request
import urllib.parse

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
COMFYUI_INPUT = os.path.join(PROJECT_ROOT, "storage", "comfyui", "input")
COMFYUI_OUTPUT = os.path.join(PROJECT_ROOT, "storage", "comfyui", "output")
COMFY_URL = "http://localhost:8188"

ROTEIRO_PADRAO = (
    "A memória RAM é a mesa de trabalho do seu computador. "
    "Tudo o que você abre agora fica nela para o processador acessar em nanossegundos. "
    "Diferente do SSD, ela é ultrarrápida, mas temporária. "
    "Quando você desliga a máquina, tudo é limpo instantaneamente. "
    "Sem uma boa quantidade de RAM, seu sistema trava e fica lento."
)

async def gerar_audio_tts(texto, arquivo_saida):
    import edge_tts
    print(f"\n[1/3] Gerando locução neural em Português...")
    comunicador = edge_tts.Communicate(texto, voice="pt-BR-AntonioNeural", rate="+0%", pitch="+0Hz")
    await comunicador.save(arquivo_saida)
    print(f" -> Áudio gerado: {arquivo_saida}")

def enviar_prompt_comfy(imagem_nome, audio_nome, prefixo_saida):
    print(f"\n[2/3] Enviando fluxo Wav2Lip para o ComfyUI...")
    prompt = {
        "1": {
            "class_type": "LoadImage",
            "inputs": {
                "image": imagem_nome
            }
        },
        "2": {
            "class_type": "LoadAudio",
            "inputs": {
                "audio": audio_nome
            }
        },
        "3": {
            "class_type": "Wav2Lip",
            "inputs": {
                "images": ["1", 0],
                "audio": ["2", 0],
                "mode": "repetitive",
                "face_detect_batch": 8
            }
        },
        "4": {
            "class_type": "VHS_VideoCombine",
            "inputs": {
                "images": ["3", 0],
                "audio": ["3", 1],
                "frame_rate": 30.0,
                "loop_count": 0,
                "filename_prefix": prefixo_saida,
                "format": "video/h264-mp4",
                "pingpong": False,
                "save_output": True
            }
        }
    }

    data = json.dumps({"prompt": prompt}).encode('utf-8')
    req = urllib.request.Request(f"{COMFY_URL}/prompt", data=data, headers={'Content-Type': 'application/json'})
    
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        prompt_id = res.get("prompt_id")
        print(f" -> Prompt aceito pelo ComfyUI! ID: {prompt_id}")
        return prompt_id

def aguardar_conclusao(prompt_id):
    print(f"\n[3/3] Processando sincronização labial (Wav2Lip na GPU)...")
    inicio = time.time()
    while True:
        try:
            req = urllib.request.urlopen(f"{COMFY_URL}/history/{prompt_id}")
            history = json.loads(req.read().decode('utf-8'))
            if prompt_id in history:
                duracao = time.time() - inicio
                print(f" -> Concluído em {duracao:.1f} segundos!")
                return history[prompt_id]
        except Exception:
            pass
        time.sleep(2)

def main():
    print("=" * 70)
    print("      PIPELINE DE APRESENTADOR REALISTA COM LIP-SYNC (Wav2Lip)")
    print("=" * 70)

    audio_nome = "narracao_ram.mp3"
    audio_path = os.path.join(COMFYUI_INPUT, audio_nome)
    imagem_nome = "apresentador.png"
    prefixo = "apresentador_lipsync"

    if not os.path.exists(audio_path):
        asyncio.run(gerar_audio_tts(ROTEIRO_PADRAO, audio_path))
    else:
        print(f"[OK] Usando áudio existente: {audio_path}")

    prompt_id = enviar_prompt_comfy(imagem_nome, audio_nome, prefixo)
    resultado = aguardar_conclusao(prompt_id)

    print("\n" + "=" * 70)
    print(" [SUCESSO] Vídeo gerado com apresentador falando e sincronia labial!")
    print(f" Arquivos em: {COMFYUI_OUTPUT}")
    print("=" * 70)

if __name__ == "__main__":
    main()

