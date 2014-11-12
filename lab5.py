import string
import re
import numpy
import pprint
from sets import Set
from math import log10, floor

allDics = {}
  
def main():

  # Read in fv 1
  #b1 = ['after carnival','again seems','also light','although normal','also owns','been restored','carnival which','certificates view','come end','commission after']

  # read in fv 2
  #b2 = ['activities both','also owns','both companies','british petroleum','committee ','financial trading','inc said','investment activities','joint management','management committee']

  # Open outcopy2.txt and save as variable since it'll be used in several different ways
  inputFile = open("outcopy2.txt", "r")

  docID = 1

  for document in inputFile:
    if not document == '\n':
      allDics[docID] = { 'bigrams' : extractBigram(document)}
      docID += 1
    

  # Create the jaccard similiarity matrix.  Will be (#docs x #docs).
  simMatrix = [[0 for x in xrange(docID-1)] for x in xrange(docID-1)]

  # iterate through all of the documents comparing each one to the others
  # Outer loop gets b1
  for eachDocID in allDics:
    b1 = allDics[eachDocID]['bigrams']
    i = eachDocID
    while i < docID:
      b2 = allDics[i]['bigrams']
      #print(b2)
      jaccard = computeJaccard(b1, b2)
      addToMatrix(simMatrix, eachDocID, i, jaccard)

      # # # ADD TO MATRIX[EACHDOCID][I] THE JACCARD VALUE
      # # # THEN 1 FOR MATRIX[EACHDOCID][EACHDOCID]
      
      print(jaccard)
      print('\n\n')
      i += 1

  pp = pprint.PrettyPrinter(depth=7)
  pp.pprint(simMatrix)


def computeJaccard(b1, b2):

  # Replace '<>' with '[]'
  b1 = re.sub('[<]', '', re.sub('[>]', '', b1))
  b1 = b1.split(",")
  b1 = map(lambda x: x.strip(), b1)
  b2 = re.sub('[<]', '', re.sub('[>]', '', b2))
  b2 = b2.split(",")
  b2 = map(lambda x: x.strip(), b2)
  print(b1)
  print(b2)
  
  # get size of intersection
  intersect = set(b1).intersection(b2)
  print(intersect)
  sizeIntersect = len(intersect)
  print("intersection size = ", sizeIntersect)

  # get size of union
  uni = set(b1).union(b2)
  sizeUnion = len(uni)
  print("union size = ", sizeUnion)

  # divide sizeInt/sizeUnion
  jaccard = float(sizeIntersect)/sizeUnion

  return jaccard

def extractBigram(line):
  # format of each doc should be <class label> <bigram vector>
  # first is doc id
  indx = 0
  count = 0
  # Iterate through the first few characters in line to remove document
  # ID and space before topics list
  for x in range(0, len(line)):
    if line[x] == "<":
      count += 1
    if count==2: 
      break
    indx += 1

  # Set the line to be the line without docID and space
  line = line[indx:]
  bigram = line
  return bigram

def addToMatrix(simMatrix, docIndx1, docIndx2, jaccard):
  simMatrix[docIndx1-1][docIndx2-1] = jaccard



main()
