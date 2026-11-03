import os

path = os.path.join("storage", "comfyui", "custom_nodes", "ComfyUI_wav2lip", "wav2lip.py")
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

# Normalize CRLF to LF for reliable editing
c = c.replace("\r\n", "\n")

if "import soundfile as sf" not in c:
    c = c.replace("import torchaudio\n", "import torchaudio\nimport soundfile as sf\n")

old_load = """    def load(self, audio):
        audio_path = folder_paths.get_annotated_filepath(audio)
        waveform, sample_rate = torchaudio.load(audio_path)
        audio = {"waveform": waveform.unsqueeze(0), "sample_rate": sample_rate}
        return (audio, )"""

new_load = """    def load(self, audio):
        audio_path = folder_paths.get_annotated_filepath(audio)
        try:
            data, sample_rate = sf.read(audio_path, dtype='float32')
            waveform = torch.from_numpy(data)
            if waveform.ndim == 1:
                waveform = waveform.unsqueeze(0)
            else:
                waveform = waveform.transpose(0, 1)
            audio = {"waveform": waveform.unsqueeze(0), "sample_rate": sample_rate}
            return (audio, )
        except Exception as e:
            print(f"Fallback to torchaudio: {e}")
            waveform, sample_rate = torchaudio.load(audio_path)
            audio = {"waveform": waveform.unsqueeze(0), "sample_rate": sample_rate}
            return (audio, )"""

c = c.replace(old_load, new_load)

old_save = """        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio_path = temp_audio.name
            # Convert waveform back to tensor and ensure it's 2D [1, samples]
            waveform_tensor = torch.tensor(waveform).unsqueeze(0)  # Shape: [1, samples]
            torchaudio.save(temp_audio_path, waveform_tensor, sample_rate)
            print(f"Saved temporary audio file at {temp_audio_path}")"""

new_save = """        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio_path = temp_audio.name
            try:
                sf.write(temp_audio_path, waveform, sample_rate)
            except Exception as e:
                waveform_tensor = torch.tensor(waveform).unsqueeze(0)
                torchaudio.save(temp_audio_path, waveform_tensor, sample_rate)
            print(f"Saved temporary audio file at {temp_audio_path}")"""

c = c.replace(old_save, new_save)

with open(path, "w", encoding="utf-8") as f:
    f.write(c)

print("Updated wav2lip.py with soundfile successfully!")

