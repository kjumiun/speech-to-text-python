import os
import glob
import wer

jvs = ""

replace_word = str.maketrans("", "", "、。 \u3000")

corpus = []
for speaker in glob.glob(os.path.join(jvs, '*', 'parallel100' + os.sep)):
    with open(os.path.join(speaker, 'transcripts_utf8.txt'), 'r', encoding='utf8') as f:
        transcripts = f.read().split()
    with open(os.path.join(speaker, 'transcripts_hypothesis.txt'), 'r', encoding='utf8') as f:
        hypothesis = f.read().split()
    corpus.append([speaker, transcripts, hypothesis])

for speaker, transcripts, hypothesis in corpus:
    for i in range(len(transcripts)):
        r_a, r_t = transcripts[i].split(':')
        for j in range(len(hypothesis)):
            h_a, h_t = hypothesis[j].split(':')
            if r_a == h_a:
                break
        else:
            continue
        


exit()