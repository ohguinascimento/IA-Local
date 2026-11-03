"""
Montador do Video Final com Apresentador Real Falando (Lip-Sync) + B-Rolls
Combina o apresentador com sincronia labial gerado pelo Wav2Lip com os takes de hardware.
"""

import os
import subprocess

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "storage", "comfyui", "output")
INPUT_DIR = os.path.join(PROJECT_ROOT, "storage", "comfyui", "input")

LIPSYNC_VIDEO = os.path.join(OUTPUT_DIR, "apresentador_lipsync_00001-audio.mp4")
if not os.path.exists(LIPSYNC_VIDEO):
    LIPSYNC_VIDEO = os.path.join(OUTPUT_DIR, "apresentador_lipsync_00001.mp4")

BROLL_RAM = os.path.join(OUTPUT_DIR, "broll_ram_macro_00001.mp4")
TRANSICAO_PC = os.path.join(OUTPUT_DIR, "transicao_calculadora_pc_00001.mp4")
AUDIO_VOZ = os.path.join(INPUT_DIR, "narracao_ram.mp3")

OUTPUT_FINAL = os.path.join(OUTPUT_DIR, "VIDEO_APRESENTADOR_REAL_RAM_FINAL.mp4")

def montar():
    print("=" * 70)
    print("   CRIANDO CORTE PROFISSIONAL COM APRESENTADOR REAL (LIP-SYNC)")
    print("=" * 70)
    
    for f, name in [(LIPSYNC_VIDEO, "Apresentador Lip-Sync"), (BROLL_RAM, "B-Roll RAM"), (TRANSICAO_PC, "Transicao PC")]:
        if not os.path.exists(f):
            print(f"[Erro] Arquivo nao encontrado: {name} ({f})")
            return

    # Filter complex para fatiar o video sincronizado e inserir B-Rolls sem desalinhar a voz
    # 0s - 6s: Apresentador falando (Introducao)
    # 6s - 13s: Macro DDR5 RAM
    # 13s - 18s: Transicao Calculadora -> PC Gamer
    # 18s - 23.36s: Apresentador falando (Conclusao com sincronia exata de finalizacao)
    filter_complex = (
        "[0:v]trim=start=0:end=6,setpts=PTS-STARTPTS,scale=512:512,setsar=1,fps=30[v0];"
        "[1:v]loop=loop=3:size=300:start=0,trim=start=0:end=7,setpts=PTS-STARTPTS,scale=512:512,setsar=1,fps=30[v1];"
        "[2:v]loop=loop=2:size=300:start=0,trim=start=0:end=5,setpts=PTS-STARTPTS,scale=512:512,setsar=1,fps=30[v2];"
        "[0:v]trim=start=18:end=23.36,setpts=PTS-STARTPTS,scale=512:512,setsar=1,fps=30[v3];"
        "[v0][v1][v2][v3]concat=n=4:v=1:a=0[outv]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", LIPSYNC_VIDEO,
        "-i", BROLL_RAM,
        "-i", TRANSICAO_PC,
        "-i", AUDIO_VOZ,
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-map", "3:a:0",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUTPUT_FINAL
    ]

    print("Executando montagem com FFmpeg...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode == 0:
        print(f"\n[SUCESSO!] Video final de apresentador real produzido:")
        print(f" -> {OUTPUT_FINAL}")
    else:
        print(f"[Erro] Falha ao renderizar: {res.stderr.decode('utf-8', errors='ignore')}")

if __name__ == "__main__":
    montar()

