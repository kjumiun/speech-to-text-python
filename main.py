from google.cloud import speech

base = ""
sample_rate = 24000

speech_client = speech.SpeechClient()

speech_config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=sample_rate,
    language_code='ja-JP')

with open(base, "rb") as f:
    content = f.read()
audio = speech.RecognitionAudio(content=content)

response = speech_client.recognize(config=speech_config, audio=audio)

print(response)