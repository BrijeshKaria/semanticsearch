import sys
import numpy as np
from bert_serving.client import BertClient
bc = BertClient()

filename = sys.argv[1]

f = open(filename, 'r')
s, sv = [], []
for line in f:
    sentence = line.strip().lower()
    print (sentence)
    vector = bc.encode([sentence])[0]
    s.append(sentence)
    sv.append(vector / np.linalg.norm(vector))

print ('0 & 1 \t\t 1 & 2 \t\t 1 & 2')

print ('Cosine Similarity:      ', round(np.dot(sv[0], sv[1]),3), '\t\t', round(np.dot(sv[0], sv[2]),3), '\t\t', round(np.dot(sv[1], sv[2]),3))
print ('Inv. Manhattan Distance:', round(1.0/np.linalg.norm((sv[0] - sv[1]),1),3), '\t\t', round(1.0/np.linalg.norm((sv[0] - sv[2]),1),3), '\t\t', round(1.0/np.linalg.norm((sv[1] - sv[2]),1),3))
print ('Inv. Euclidean Distance:', round(1/np.linalg.norm((sv[0] - sv[1]),2),3), '\t\t', round(1.0/np.linalg.norm((sv[0] - sv[2]),2),3), '\t\t', round(1.0/np.linalg.norm((sv[1] - sv[2]),2),3))
