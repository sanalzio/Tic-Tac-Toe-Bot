from bgm import *

mybgm=bgm()
mybgm.loadmodel('xox')
#print(mybgm.data)
print((mybgm.getprediction(['-', 'X', 'O', '-', 'X', '-', '-', '-', '-'])))
#print((mybgm.getprediction(['.', 'X', '.', '.', 'X', '.', '.', '-', '.'])))