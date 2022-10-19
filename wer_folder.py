import os
import glob
import wer
import sys

# ppp=print
# def print(*str):
#     with open("wer_whisper_hiroshiba_2000epoch.txt", "w") as f:
#         ppp(*str, file=f)

speaker = ""

replace_word = str.maketrans("", "", "、。 \u3000")

corpus = []
with open(os.path.join(speaker, 'transcripts_utf8.txt'), 'r', encoding='utf8') as f:
    transcripts = f.read().splitlines()
with open(os.path.join(speaker, 'transcripts_google_speech_recognition.txt'), 'r', encoding='utf8') as f:
    hypothesis = f.read().splitlines()
corpus.append([speaker, transcripts, hypothesis])

word_error_total=0
words_total=0

for speaker, transcripts, hypothesis in corpus:
    print(f'speaker: {speaker}')
    for i in range(len(transcripts)):
        r_a, r_t = transcripts[i].split(':')
        for j in range(len(hypothesis)):
            h_a, h_t = hypothesis[j].split(':')
            if r_a[-3:] == h_a[-3:]:
                break
        else:
            continue

        morpheme_r = wer.separateWords(r_t.translate(replace_word))
        morpheme_h = wer.separateWords(h_t.translate(replace_word))
        word_error, words = wer.wer(morpheme_r, morpheme_h)
        word_error_total += word_error
        words_total += words

print("word_error_total/words_total")
print(word_error_total,"/",words_total,"=",word_error_total/words_total)
        


exit()