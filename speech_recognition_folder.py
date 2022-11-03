import os
import glob
import whisper
import speech_recognition
from time import sleep

print('initializing...')
model = whisper.load_model("large")
recognizer = speech_recognition.Recognizer()

'''
Speech to Text by Whisper and Google Speech Recognition

base: Path to the folder containing the speech data (folder/speech.wav)
'''

base = ""

def whisper_sst(speeches: list, out_path: str) -> None:
    with open(os.path.join(out_path, 'transcripts_whisper.txt'), 'w', encoding='utf8') as hypothesis:
        for i in range(len(speeches)):
            print("\rRecognizing speeches... {} % ".format((i+1)*100//len(speeches)), end="")
            result = model.transcribe(speeches[i])#.translate(replace_word)
            hypothesis.write(':'.join([os.path.basename(speeches[i]).split('.')[0], result["text"]])+'\n')

def google_speech_recognition_sst(speeches: list, out_path: str) -> None:
    with open(os.path.join(out_path, 'transcripts_google_speech_recognition.txt'), 'w', encoding='utf8') as hypothesis:
        for i in range(len(speeches)):
            print("\rRecognizing speeches... {} %".format((i+1)*100//len(speeches)), end="")
            with speech_recognition.AudioFile(speeches[i]) as source:
                audio = recognizer.record(source)
            result = ''
            for _ in range(3):
                try:
                    result = recognizer.recognize_google(audio, language='ja-JP')#.translate(replace_word)
                except speech_recognition.UnknownValueError:
                    print(" Google Speech Recognition could not understand audio")
                    sleep(1)
                    continue
                else:
                    break
            hypothesis.write(':'.join([os.path.basename(speeches[i]).split('.')[0], result])+'\n')

def main() -> None:
    wavs = glob.glob(os.path.join(base, '*.wav'))
    whisper_sst(wavs, base)
    google_speech_recognition_sst(wavs, base)

if __name__ == '__main__':
    main()