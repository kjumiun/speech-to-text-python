#-*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import numpy
import MeCab

'''
usage: python wer.py [original_file.txt]  [target_file.txt]
'''

def editDistance(r, h):
    '''
    This function is to calculate the edit distance of reference sentence and the hypothesis sentence.

    Main algorithm used is dynamic programming.

    Attributes: 
        r -> the list of words produced by splitting reference sentence.
        h -> the list of words produced by splitting hypothesis sentence.
    '''
    d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.uint8).reshape((len(r)+1, len(h)+1))
    for i in range(len(r)+1):
        d[i][0] = i
    for j in range(len(h)+1):
        d[0][j] = j
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                substitute = d[i-1][j-1] + 1
                insert = d[i][j-1] + 1
                delete = d[i-1][j] + 1
                d[i][j] = min(substitute, insert, delete)
    return d

def getStepList(r, h, d):
    '''
    This function is to get the list of steps in the process of dynamic programming.

    Attributes: 
        r -> the list of words produced by splitting reference sentence.
        h -> the list of words produced by splitting hypothesis sentence.
        d -> the matrix built when calulating the editting distance of h and r.
    '''
    x = len(r)
    y = len(h)
    list = []
    while True:
        if x == 0 and y == 0: 
            break
        elif x >= 1 and y >= 1 and d[x][y] == d[x-1][y-1] and r[x-1] == h[y-1]: 
            list.append("e")
            x = x - 1
            y = y - 1
        elif y >= 1 and d[x][y] == d[x][y-1]+1:
            list.append("i")
            x = x
            y = y - 1
        elif x >= 1 and y >= 1 and d[x][y] == d[x-1][y-1]+1:
            list.append("s")
            x = x - 1
            y = y - 1
        else:
            list.append("d")
            x = x - 1
            y = y
    return list[::-1]

def alignedPrint(list, r, h, result):
    '''
    This funcition is to print the result of comparing reference and hypothesis sentences in an aligned way.
    
    Attributes:
        list   -> the list of steps.
        r      -> the list of words produced by splitting reference sentence.
        h      -> the list of words produced by splitting hypothesis sentence.
        result -> the rate calculated based on edit distance.
    '''
    print("REF:", end=" ")
    for i in range(len(list)):
        if list[i] == "i":
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            print(" "*(len(h[index])), end=" ")
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) < len(h[index2]):
                print(r[index1] + " " * (len(h[index2])-len(r[index1])), end=" ")
            else:
                print(r[index1], end=" "),
        else:
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print(r[index], end=" "),
    print("\nHYP:", end=" ")
    for i in range(len(list)):
        if list[i] == "d":
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print(" " * (len(r[index])), end=" ")
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) > len(h[index2]):
                print(h[index2] + " " * (len(r[index1])-len(h[index2])), end=" ")
            else:
                print(h[index2], end=" ")
        else:
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            print(h[index], end=" ")
    print("\nEVA:", end=" ")
    for i in range(len(list)):
        if list[i] == "d":
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print("D" + " " * (len(r[index])-1), end=" ")
        elif list[i] == "i":
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            print("I" + " " * (len(h[index])-1), end=" ")
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) > len(h[index2]):
                print("S" + " " * (len(r[index1])-1), end=" ")
            else:
                print("S" + " " * (len(h[index2])-1), end=" ")
        else:
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print(" " * (len(r[index])), end=" ")
    print("\nWER: " + result)

def wer(r, h):
    """
    This is a function that calculate the word error rate in ASR.
    You can use it like this: wer("what is it".split(), "what is".split()) 
    """
    # build the matrix
    d = editDistance(r, h)

    # find out the manipulation steps
    list = getStepList(r, h, d)

    # print the result in aligned way
    result = float(d[len(r)][len(h)]) / len(r) * 100
    result = str("%.2f" % result) + "%"
    alignedPrint(list, r, h, result)

    #不一致の単語数
    word_error=d[len(r)][len(h)]
    #単語数
    words=len(r)
    return word_error,words

def separateWords(lists):
    word_array=[]
    tagger = MeCab.Tagger('-Ochasen')
    tagger.parse("")
    node = tagger.parseToNode(lists).next
    while node.next:
        word_array.append(node.surface)
        node = node.next
    return word_array


# ####実行前のチェック##############################################################################################
# ##コマンドライン引数のチェック
# #コマンドの引数が仕様通り
# if len(sys.argv) == 3:    
#     if (".txt" in sys.argv[1]) and  (".txt" in sys.argv[2]):
#         pass
#     else:
#         print("input_file extension does not match '.txt'")
#         sys.exit()
# #コマンドの引数が合わない場合は中断
# else:
#     print("usage: python wer.py [original_file.txt]  [target_file.txt]")
#     sys.exit()

# ##ファイルの行数チェック
# with open(sys.argv[1],'r') as f:
#     lines1 = [s.strip() for s in f.readlines()]
#     num_rows1=len(lines1)
# with open(sys.argv[2],'r') as f:
#     lines2 = [s.strip() for s in f.readlines()]
#     num_rows2=len(lines2)

# if num_rows1 != num_rows2:
#     print("error: Number of lines is different [original_file.txt]  [target_file.txt]")
#     sys.exit()

####メイン処理##############################################################################################
if __name__ == '__main__':
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    #ファイルの1行づつを配列へ格納
    with open(filename1, 'r', encoding="utf8") as ref:
        r = ref.read().split()
    with open(filename2, 'r', encoding="utf8") as hyp:
        h = hyp.read().split()
    
    word_error_total=0
    words_total=0
    for index in range(len(r)):
        #1行を形態素解析して単語のリストにする
        morpheme_r = separateWords(r[index])
        morpheme_h = separateWords(h[index])
        word_error,words = wer(morpheme_r, morpheme_h)
        word_error_total+=word_error
        words_total+=words
    
    #総不一致の単語数/総単語数
    print("word_error_total/words_total")
    print(word_error_total,"/",words_total,"=",word_error_total/words_total)
