import os
import glob
import speech_recognition

recognizer = speech_recognition.Recognizer()

jvs = r""

replace_word = str.maketrans("", "", "、。 \u3000")

corpus = []
for speaker in glob.glob(os.path.join(jvs, '*', 'parallel100' + os.sep)):
    with open(os.path.join(speaker, 'transcripts_utf8.txt'), 'r', encoding='utf8') as f:
        transcripts = f.read().split()
    speeches = []
    for speech in transcripts:
        speech_file = glob.glob(os.path.join(speaker, 'wav24kHz16bit', '*' + speech.split(':')[0] + '*'))
        if speech_file:
            speeches.append(speech_file[0])
        else:
            transcripts.remove(speech)
    corpus.append([speaker, transcripts, speeches])

for speaker, transcripts, speeches in corpus:
    if os.path.exists(os.path.join(speaker, 'transcripts_hypothesis.txt')):
        if os.path.getsize(os.path.join(speaker, 'transcripts_hypothesis.txt')) != 0:
            continue
    print(f'\nspeaker: {speaker}')
    with open(os.path.join(speaker, 'transcripts_hypothesis.txt'), 'w', encoding='utf8') as hypothesis:
        for i in range(len(speeches)):
            print("\rRecognizing speeches... {} %".format((i+1)*100//len(speeches)), end="")
            with speech_recognition.AudioFile(speeches[i]) as source:
                audio = recognizer.record(source)
            result = recognizer.recognize_google(audio, language='ja-JP')#.translate(replace_word)
            hypothesis.write(':'.join([os.path.basename(speeches[i]).split('.')[0], result])+'\n')
