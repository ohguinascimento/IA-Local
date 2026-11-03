"""
Montador de Video Dinamico (Apresentador + B-Rolls de Hardware + Audio Narrado)
Combina multiplas cenas de IA para criar uma apresentacao fluida com cortes profissionais.
"""

import os
import sys
import subprocess

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "storage", "comfyui", "output")
INPUT_DIR = os.path.join(PROJECT_ROOT, "storage", "comfyui", "input")

AUDIO_PATH = os.path.join(INPUT_DIR, "narracao_ram.mp3")
VIDEO_FINAL = os.path.join(OUTPUT_DIR, "VIDEO_TECNOLOGIA_RAM_DINAMICO.mp4")

def montar_video():
    print("=" * 70)
    print("   MONTANDO VIDEO DINAMICO: APRESENTADOR + B-ROLLS DE HARDWARE")
    print("=" * 70)

    # Identificar os melhores clipes disponiveis
    arquivos = os.listdir(OUTPUT_DIR)
    
    # 1. Cena Apresentador
    cenas_apresentador = [os.path.join(OUTPUT_DIR, f) for f in arquivos if f.startswith("apresentador_ram_mp4") and f.endswith(".mp4")]
    # 2. Cena B-Roll Memoria RAM
    cenas_ram = [os.path.join(OUTPUT_DIR, f) for f in arquivos if f.startswith("broll_ram") and f.endswith(".mp4")]
    # 3. Cena PC Gamer / Transicao
    cenas_pc = [os.path.join(OUTPUT_DIR, f) for f in arquivos if f.startswith("transicao_calculadora_pc") and f.endswith(".mp4")]

    if not cenas_apresentador or not cenas_pc:
        print("[Erro] Clipes basicos necessarios nao encontrados.")
        return

    clip_apresentador = cenas_apresentador[-1]
    clip_pc = cenas_pc[-1]
    clip_ram = cenas_ram[-1] if cenas_ram else clip_pc

    print("Cenas selecionadas para o corte:")
    print(f" 1. Abertura (Apresentador) : {os.path.basename(clip_apresentador)}")
    print(f" 2. B-Roll (Memoria RAM)    : {os.path.basename(clip_ram)}")
    print(f" 3. Conclusao (PC Gamer)    : {os.path.basename(clip_pc)}")
    print(f" Faixa de Audio             : {os.path.basename(AUDIO_PATH)}\n")

    # Criar lista de concatenacao com repeticoes suaves para preencher o tempo do audio (23s)
    lista_txt = os.path.join(OUTPUT_DIR, "concat_list.txt")
    with open(lista_txt, "w", encoding="utf-8") as f:
        # Repete cada clipe duas vezes para dar ~6 segundos por cena
        f.write(f"file '{clip_apresentador.replace(os.sep, '/')}'\n")
        f.write(f"file '{clip_apresentador.replace(os.sep, '/')}'\n")
        f.write(f"file '{clip_ram.replace(os.sep, '/')}'\n")
        f.write(f"file '{clip_ram.replace(os.sep, '/')}'\n")
        f.write(f"file '{clip_pc.replace(os.sep, '/')}'\n")
        f.write(f"file '{clip_pc.replace(os.sep, '/')}'\n")

    # Comando FFmpeg para concatenar os videos e sincronizar com a voz
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", lista_txt,
        "-i", AUDIO_PATH,
        "-shortest",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        VIDEO_FINAL
    ]

    print("Processando com FFmpeg...")
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        print(f"\n[SUCESSO!] Video final montado com cortes dinamicos:")
        print(f" -> {VIDEO_FINAL}")
    except subprocess.CalledProcessError as e:
        print(f"[Erro] Falha no FFmpeg: {e.stderr.decode('utf-8', errors='ignore')}")
    finally:
        if os.path.exists(lista_txt):
            os.remove(lista_txt)

if __name__ == "__main__":
    montar_video()

