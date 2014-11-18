import string
import re
import sys
import numpy
import pprint
import random
import time
from sets import Set

allDics = {}
  
def main():

  # Open outcopy2.txt and save as variable since it'll be used in several different ways
  inputFile = open("outcopy2.txt", "r")

  docID = 1

  # Create a dictionary for the docID --> bigrams
  for document in inputFile:
    if not document == '\n':
      allDics[docID] = { 'bigrams' : extractBigram(document)}
      docID += 1

    
  # Create the jaccard similiarity matrix.  Will be (#docs x #docs).
  simMatrix = [[0 for x in xrange(docID-1)] for x in xrange(docID-1)]

  # Iterate through all of the documents comparing each one to the others
  for eachDocID in allDics:
    b1 = allDics[eachDocID]['bigrams']
    i = eachDocID
    while i < docID:
      b2 = allDics[i]['bigrams']
      jaccard = computeJaccard(b1, b2)
      addToMatrix(simMatrix, eachDocID, i, jaccard)
      i += 1


  # Create a set of unique strings that are the bigrams
  bigramList = Set()
  for eachDocID in allDics:
    allDics[eachDocID]['bigrams'] = re.sub('[<]', '', re.sub('[>]', '', allDics[eachDocID]['bigrams'])).strip().split(',')
    for bigrm in allDics[eachDocID]['bigrams']:
      bigramList.add(bigrm)

      
  # Create the (bigram x Document) matrix
  inputMatrix = []
  for x in range(len(bigramList)):
    inputMatrix.append([])


  # Fill the matrix with 1s if bigram is present in document, 0 o.w.
  bIndx = 0
  for b in bigramList:
    for did in allDics:
      inputMatrix[bIndx].append(1 if b in allDics[did]['bigrams'] else 0)
    bIndx += 1

  k = 16
  print
  while k <= 128:
    print "k = " + str(k)
    start = time.time()
    sigMatrix = hashIt(inputMatrix, docID, k)
    jaccardEstimate = sigJaccard(sigMatrix, k)
    meanSquareError(simMatrix, jaccardEstimate, docID)
    end = time.time()
    print "Seconds to complete: " + str(end - start) + "\n"
    k = k*2


  pp = pprint.PrettyPrinter(depth=docID)
  #pp.pprint(simMatrix)
  #pp.pprint(jaccardEstimate)
  #pp.pprint(sigMatrix)


def hashIt(inputMatrix, numDocs, k):
  p = 32416188517  
  rows = len(inputMatrix)
  cols = len(inputMatrix[0])

  sigMatrix = []
  for i in range(k):
    sigMatrix.append([sys.maxint] * cols)

  for perm in range(k):
    a = round((random.random())*10**18, 0)
    b = round((random.random())*10**15, 0)
    for c in range(cols):
      minSig = p
      for r in range(rows):
        if inputMatrix[r][c] == 1:
          # value = ((index of '1')*a + b)%p%N
          value = (r*a+b)%p%numDocs
          # Update minhash-signature value
          if minSig > value:
            minSig = value
      sigMatrix[perm][c] = int(minSig)

  pp = pprint.PrettyPrinter()
  # pp.pprint(sigMatrix)
  return sigMatrix
    

def computeJaccard(b1, b2):

  # Replace '<>' with '[]'
  b1 = re.sub('[<]', '', re.sub('[>]', '', b1))
  b1 = b1.split(",")
  b1 = map(lambda x: x.strip(), b1)
  b2 = re.sub('[<]', '', re.sub('[>]', '', b2))
  b2 = b2.split(",")
  b2 = map(lambda x: x.strip(), b2)
  
  # get size of intersection
  intersect = set(b1).intersection(b2)
  sizeIntersect = len(intersect)

  # get size of union
  uni = set(b1).union(b2)
  sizeUnion = len(uni)

  # divide sizeInt/sizeUnion
  jaccard = float(sizeIntersect)/sizeUnion
  return jaccard

def sigJaccard(sigMatrix, k):
  cols = len(sigMatrix[0])
  rows = len(sigMatrix)
  estJaccard = [[0 for x in xrange(cols)] for x in xrange(cols)]

  for c in range(cols):
    for x in range(c, cols):
      intersect = 0
      for r in range(rows):
        if sigMatrix[r][c] == sigMatrix[r][x]:
          intersect += 1
      union = (k*2)-intersect
      estJaccard[c][x] = round((float(intersect)/union), 3)

  return estJaccard

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

def meanSquareError(jaccardMatrix, minHashMatrix, docID):
  # Outer loop iterates over rows
  numsum = 0
  count = 0
  for i in xrange(docID-1):
    # Inner loop iterates over columns
    for l in xrange(docID-1):
      # MSE takes in actual and predicted values as parameters
      numsum += (minHashMatrix[i][l] - jaccardMatrix[i][l])**2
      count += 1
      
  mse = numsum/docID
  print "MSE = " + str(mse)

main()
