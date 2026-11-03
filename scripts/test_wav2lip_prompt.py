import json
import urllib.request
import urllib.parse
import time

prompt = {
    "1": {
        "class_type": "LoadImage",
        "inputs": {
            "image": "apresentador.png"
        }
    },
    "2": {
        "class_type": "LoadAudio",
        "inputs": {
            "audio": "narracao_ram.mp3"
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
            "filename_prefix": "apresentador_lipsync",
            "format": "video/h264-mp4",
            "pingpong": False,
            "save_output": True
        }
    }
}

data = json.dumps({"prompt": prompt}).encode('utf-8')
req = urllib.request.Request("http://localhost:8188/prompt", data=data, headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode('utf-8'))
        print("Prompt enviado com sucesso! Prompt ID:", result.get("prompt_id"))
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code, e.read().decode('utf-8'))
except Exception as e:
    print("Error:", e)

