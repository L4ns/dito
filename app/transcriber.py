import whisper

def transcribe_audio(path: str) -> str:
    model = whisper.load_model("tiny")
    result = model.transcribe(path)
    return result.get("text", "")
