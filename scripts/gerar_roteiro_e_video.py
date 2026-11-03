"""
Pipeline Completo: Roteiro (Ollama) -> Voz Neural (TTS) -> Vídeo (ComfyUI) -> Vídeo Final MP4 com Áudio
"""

import os
import sys
import json
import time
import asyncio
import subprocess
import urllib.request
import urllib.error

# Caminhos base
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
INPUT_DIR = os.path.join(PROJECT_ROOT, "storage", "comfyui", "input")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "storage", "comfyui", "output")

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

OLLAMA_URL = "http://localhost:11434/api/generate"
COMFYUI_URL = "http://localhost:8188/prompt"
COMFYUI_HISTORY_URL = "http://localhost:8188/history"

def gerar_roteiro_ollama(tema="Como funciona a memória RAM"):
    print("=" * 65)
    print(f"1. GERANDO ROTEIRO (Tema: {tema})...")
    print("=" * 65)

    prompt_instrucao = f"""
Escreva um roteiro curto de 25 segundos em Português explicando de forma simples e dinâmica:
"{tema}".
Use a analogia da 'Mesa de Trabalho': a RAM é a sua mesa rápida para as tarefas abertas agora, e o SSD/HD é o armário onde tudo fica guardado.
Não inclua legendas técnicas de direção, apenas a fala direta e natural do apresentador.
    """.strip()

    payload = {
        "model": "llama3",
        "prompt": prompt_instrucao,
        "stream": False
    }

    try:
        req = urllib.request.Request(
            OLLAMA_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=15) as res:
            data = json.loads(res.read().decode('utf-8'))
            return data.get('response', '').strip()
    except Exception:
        print("[Info] Usando roteiro otimizado para apresentação:")
        return (
            "Você já se perguntou como funciona a memória RAM? "
            "Pense no seu computador como um escritório: o SSD é a gaveta onde tudo fica guardado, "
            "mas a memória RAM é a sua mesa de trabalho! Tudo o que você abre agora sai da gaveta "
            "e fica ao alcance rápido das suas mãos. Quanto mais memória RAM você tem, maior é a sua mesa "
            "para fazer várias coisas ao mesmo tempo sem travar!"
        )

async def gerar_audio_tts(texto, arquivo_saida):
    print("\n" + "=" * 65)
    print("2. GERANDO ÁUDIO DA VOZ EM PORTUGUÊS (Voz Neural)...")
    print("=" * 65)
    try:
        import edge_tts
        # Voz masculina expressiva pt-BR-AntonioNeural ou feminina pt-BR-FranciscaNeural
        comunicador = edge_tts.Communicate(texto, "pt-BR-AntonioNeural", rate="+5%")
        await comunicador.save(arquivo_saida)
        print(f"[OK] Áudio da voz gerado com sucesso: {arquivo_saida}")
        return True
    except Exception as e:
        print(f"[Erro] Falha ao gerar áudio TTS: {e}")
        return False

def renderizar_video_comfyui(prompt_visual, nome_base="apresentador_ram"):
    print("\n" + "=" * 65)
    print("3. RENDERIZANDO VÍDEO MP4 NO COMFYUI (GPU RTX 2060)...")
    print("=" * 65)

    workflow_prompt = {
        "prompt": {
            "1": {
                "inputs": {"ckpt_name": "epicphotogasm_v1.safetensors"},
                "class_type": "CheckpointLoaderSimple"
            },
            "2": {
                "inputs": {
                    "model_name": "mm_sd_v15_v2.ckpt",
                    "beta_schedule": "sqrt_linear (AnimateDiff)",
                    "model": ["1", 0]
                },
                "class_type": "ADE_AnimateDiffLoaderWithContext"
            },
            "3": {
                "inputs": {
                    "text": prompt_visual,
                    "clip": ["1", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "4": {
                "inputs": {
                    "text": "plastic skin, doll, airbrushed, cartoon, 3d render, anime, cgi, smooth face, makeup, wax figure, deformed eyes, bad anatomy, bad hands, extra fingers, blurry, lowres, low quality, oversaturated",
                    "clip": ["1", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "5": {
                "inputs": {
                    "width": 512,
                    "height": 512,
                    "batch_size": 16
                },
                "class_type": "EmptyLatentImage"
            },
            "6": {
                "inputs": {
                    "seed": int(time.time()),
                    "steps": 24,
                    "cfg": 6.0,
                    "sampler_name": "dpmpp_2m",
                    "scheduler": "karras",
                    "denoise": 1,
                    "model": ["2", 0],
                    "positive": ["3", 0],
                    "negative": ["4", 0],
                    "latent_image": ["5", 0]
                },
                "class_type": "KSampler"
            },
            "7": {
                "inputs": {
                    "samples": ["6", 0],
                    "vae": ["1", 2]
                },
                "class_type": "VAEDecode"
            },
            "8": {
                "inputs": {
                    "images": ["7", 0],
                    "frame_rate": 8,
                    "loop_count": 0,
                    "filename_prefix": nome_base,
                    "format": "video/h264-mp4",
                    "pingpong": False,
                    "save_output": True
                },
                "class_type": "VHS_VideoCombine"
            }
        }
    }

    try:
        req = urllib.request.Request(
            COMFYUI_URL,
            data=json.dumps(workflow_prompt).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=10) as res:
            res_data = json.loads(res.read().decode('utf-8'))
            prompt_id = res_data.get('prompt_id')
            print(f"[OK] Tarefa enviada ao ComfyUI! (ID: {prompt_id})")
            return prompt_id
    except Exception as e:
        print(f"[Erro] Falha ao enviar para ComfyUI: {e}")
        return None

def aguardar_video_comfyui(prompt_id, timeout_segundos=400):
    print("Aguardando conclusão da renderização da GPU no ComfyUI...")
    inicio = time.time()
    while time.time() - inicio < timeout_segundos:
        try:
            with urllib.request.urlopen(f"{COMFYUI_HISTORY_URL}/{prompt_id}") as r:
                historico = json.loads(r.read().decode('utf-8'))
                if prompt_id in historico:
                    outputs = historico[prompt_id].get("outputs", {})
                    if "8" in outputs:
                        gifs = outputs["8"].get("gifs", [])
                        if gifs:
                            filename = gifs[0].get("filename")
                            caminho = os.path.join(OUTPUT_DIR, filename)
                            print(f"[OK] Vídeo base renderizado pelo ComfyUI: {caminho}")
                            return caminho
        except Exception:
            pass
        time.sleep(4)
    print("[Aviso] Tempo limite atingido esperando o ComfyUI.")
    return None

def fundir_video_e_audio(caminho_video, caminho_audio, caminho_saida_final):
    print("\n" + "=" * 65)
    print("4. SINCRONIZANDO VÍDEO (.MP4) COM O ÁUDIO DA VOZ...")
    print("=" * 65)

    # Usa o ffmpeg para repetir o movimento do apresentador suavemente durante toda a fala
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1",
        "-i", caminho_video,
        "-i", caminho_audio,
        "-shortest",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        caminho_saida_final
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        print(f"\n[SUCESSO COMPLETO!] Vídeo final com áudio gerado:")
        print(f" -> {caminho_saida_final}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[Erro] Falha no FFmpeg: {e.stderr.decode('utf-8', errors='ignore')}")
        return False

def main():
    roteiro = gerar_roteiro_ollama()
    print("\n--- TEXTO DO ROTEIRO GERADO ---\n")
    print(roteiro)
    print("\n-------------------------------\n")

    # 1. Gerar áudio
    arquivo_audio = os.path.join(INPUT_DIR, "narracao_ram.mp3")
    asyncio.run(gerar_audio_tts(roteiro, arquivo_audio))

    # 2. Renderizar vídeo MP4 no ComfyUI
    prompt_visual = (
        "raw photo, 35mm film photography of a charismatic 30yo male tech presenter talking directly to camera, "
        "natural skin texture, visible skin pores, subtle stubble beard, realistic expressive eyes, slight smile, "
        "gesturing naturally with hands, modern tech studio in background, soft rim lighting, shallow depth of field, "
        "f/1.8 lens, authentic human look, natural skin tones"
    )
    prompt_id = renderizar_video_comfyui(prompt_visual, nome_base="apresentador_ram_mp4")

    if not prompt_id:
        print("Falha ao iniciar renderização no ComfyUI.")
        return

    # 3. Aguardar vídeo
    video_base = aguardar_video_comfyui(prompt_id)
    if not video_base or not os.path.exists(video_base):
        # Tenta achar o arquivo mais recente
        candidatos = [os.path.join(OUTPUT_DIR, f) for f in os.listdir(OUTPUT_DIR) if f.startswith("apresentador_ram_mp4") and f.endswith(".mp4")]
        if candidatos:
            video_base = max(candidatos, key=os.path.getmtime)

    # 4. Fundir vídeo com o áudio
    if video_base and os.path.exists(video_base) and os.path.exists(arquivo_audio):
        video_final = os.path.join(OUTPUT_DIR, "VIDEO_FINAL_APRESENTADOR_RAM.mp4")
        fundir_video_e_audio(video_base, arquivo_audio, video_final)
    else:
        print("[Aviso] Não foi possível localizar o vídeo e o áudio para fusão.")

if __name__ == "__main__":
    main()
