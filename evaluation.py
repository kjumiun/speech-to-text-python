# for arm64 Mac need to do 'brew install mecab' and 'pip install mecab-python3' before run it
import MeCab

transcripts = ""
speeches = ""
replace_word = str.maketrans("", "", "、。")

with open(transcripts, 'r') as f:
    r = f.read().split()

transcripts_formed = []
for s in r:
    s = s.split(':')[1]
    s = s.translate(replace_word)
    transcripts_formed.append(s)

tagger = MeCab.Tagger("-Ochasen")
tagger.parse("")
node = tagger.parseToNode(transcripts_formed[0]).next
while node.next:
    print(node.feature)
    node = node.next