"""
Script de Renderizacao: Transicao Visual Fluida / Morphing
Calculadora Mecanica Vintage -> Computador Gamer Transparente Iluminado
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error

COMFYUI_URL = "http://localhost:8188/prompt"
COMFYUI_HISTORY_URL = "http://localhost:8188/history"

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "storage", "comfyui", "output")

def gerar_transicao_calculadora_pc(seed=None):
    if seed is None:
        seed = int(time.time())

    print("=" * 70)
    print("   TRANSICAO VISUAL CINEMATOGRAFICA (MORPHING): CALCULADORA -> PC GAMER")
    print("=" * 70)
    print("Etapas do Morphing:")
    print(" [Quadro 0-8]  : Calculadora mecanica antiga com engrenagens de latao e madeira")
    print(" [Quadro 9-17] : Efeito de dissolucao fluida (morphing) de engrenagens para circuitos")
    print(" [Quadro 18-24]: PC Gamer moderno transparente, vidro temperado e luzes RGB neon\n")

    # Cronograma de prompts (Prompt Scheduling com interpolacao esferica SLERP)
    sched_text = (
        '"0": "Cinematic shot of an antique vintage mechanical calculator with intricate moving brass gears and metal dials, dark wood desk, dramatic rim studio lighting, shallow depth of field, 4k resolution",\n'
        '"10": "Cinematic visual transition, split screen morphing, antique mechanical calculator dissolving into high-tech computer components, glowing brass gears melting into illuminated circuit boards, RGB glow, particle trails, smooth morph effect, 4k",\n'
        '"18": "Cinematic modern sleek transparent custom gaming PC illuminated by vibrant RGB lights, glass case, liquid cooling glowing tubes, high-tech digital code running in the dark background, dramatic studio lighting, 4k"'
    )

    workflow_prompt = {
        "prompt": {
            "1": {
                "inputs": {"ckpt_name": "DreamShaper_8_pruned.safetensors"},
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
                    "prompts": sched_text,
                    "clip": ["1", 1],
                    "tensor_interp": "slerp"
                },
                "class_type": "ADE_PromptScheduling"
            },
            "4": {
                "inputs": {
                    "text": "blurry, bad anatomy, deformed, distorted, low quality, worst quality, pixelated, static, freeze, flat lighting, glitch, artifacts",
                    "clip": ["1", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "5": {
                "inputs": {
                    "width": 512,
                    "height": 512,
                    "batch_size": 24
                },
                "class_type": "EmptyLatentImage"
            },
            "6": {
                "inputs": {
                    "seed": seed,
                    "steps": 22,
                    "cfg": 7.5,
                    "sampler_name": "euler_ancestral",
                    "scheduler": "normal",
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
                    "filename_prefix": "transicao_calculadora_pc",
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
            print(f"[OK] Tarefa enviada ao ComfyUI! ID: {prompt_id}")
            print("Renderizando na GPU RTX 2060...")
            return prompt_id
    except Exception as e:
        print(f"[Erro] Falha ao conectar ao ComfyUI: {e}")
        return None

def aguardar_video(prompt_id, timeout_segundos=400):
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
                            print(f"\n[SUCESSO] Video MP4 da transicao gerado!")
                            print(f" -> {caminho}")
                            return caminho
        except Exception:
            pass
        time.sleep(4)
    print("\n[Aviso] O video ainda esta sendo processado na GPU.")
    return None

if __name__ == "__main__":
    prompt_id = gerar_transicao_calculadora_pc()
    if prompt_id:
        aguardar_video(prompt_id)

