import os
import glob
import cer

jvs = r""

replace_word = str.maketrans("", "", "、。 \u3000")

corpus = []
for speaker in glob.glob(os.path.join(jvs, '*', 'parallel100' + os.sep)):
    with open(os.path.join(speaker, 'transcripts_utf8.txt'), 'r', encoding='utf8') as f:
        transcripts = f.read().splitlines()
    with open(os.path.join(speaker, 'transcripts_hypothesis_whisper.txt'), 'r', encoding='utf8') as f:
        hypothesis = f.read().splitlines()
    corpus.append([speaker, transcripts, hypothesis])

#総語数
total_chara=0
#総誤り語数
total_diff_chara=0

for speaker, transcripts, hypothesis in corpus:
    print(f'speaker: {speaker}')
    for i in range(len(transcripts)):
        r_a, r_t = transcripts[i].split(':')
        for j in range(len(hypothesis)):
            h_a, h_t = hypothesis[j].split(':')
            if r_a == h_a:
                break
        else:
            continue

        str_r = r_t.translate(replace_word)
        str_h = h_t.translate(replace_word)
        num_charas, diff_charas = cer.diffLines(i+1,str_r, str_h)

        #総語数と総誤り語数をカウントアップ
        total_chara+=num_charas
        total_diff_chara+=diff_charas

##最終的な出力
print("#################################################################")
print("総文字数:"+str(total_chara) + \
    "  総誤り文字数:"+str(total_diff_chara) + \
    "  文字誤り率:"+str(total_diff_chara/total_chara) \
    )
