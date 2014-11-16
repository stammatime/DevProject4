import string
import re
import sys
import numpy
import pprint
import random
from sets import Set

allDics = {}
  
def main():

  # Open outcopy2.txt and save as variable since it'll be used in several different ways
  inputFile = open("bigramOut.txt", "r")

  docID = 1

  # Create a dictionary for the docID --> bigrams
  for document in inputFile:
    if not document == '\n':
      allDics[docID] = { 'bigrams' : extractBigram(document)}
      docID += 1

  # Value of K for k-minhash  
  k = 16
    
  # Create the jaccard similiarity matrix.  Will be (#docs x #docs).
  simMatrix = [[0 for x in xrange(docID-1)] for x in xrange(docID-1)]
  mseMatrix = [[0 for x in xrange(docID-1)] for x in xrange(docID-1)]


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


  minHashMatrix = minHash(inputMatrix, k, docID)
  
  # Calculate the MSE between our Jaccard matrix and the minhash matrix
  #meanSquareError(simMatrix, minHashMatrix, mseMatrix, docID)

  pp = pprint.PrettyPrinter(depth=docID)
  pp.pprint(minHashMatrix)


# Len = len(bigramList) = #bigrams
def minHash(inputMatrix, k, numDocs):

  # Num rows in the hash function will be the # rows in the input matrix
  rows = len(inputMatrix)
  # Cols is the number of columns in the input matrix, ie # docs
  cols = len(inputMatrix[0])
  sigRows = k
  
  
  # Sig matrix initialize with series of max int
  sigMatrix = []
  for i in range(sigRows):
    sigMatrix.append([sys.maxint] * cols)
  
  for r in range(rows):
    # If value = 1, and signature > hash value, replace signature with hash value
    # According to the k-minhash algorithm.
    for c in range(cols):
        if inputMatrix[r][c] == 0:
            continue
        for i in range(sigRows):
            hashvalue = (random.random()*r+random.random()%sys.maxint)%numDocs
            if sigMatrix[i][c] > hashvalue:
                sigMatrix[i][c] = round(hashvalue, 2)

  return sigMatrix
      

def computeJaccard(b1, b2):

  # Replace '<>' with '[]'
  b1 = re.sub('[<]', '', re.sub('[>]', '', b1))
  b1 = b1.split(",")
  b1 = map(lambda x: x.strip(), b1)
  b2 = re.sub('[<]', '', re.sub('[>]', '', b2))
  b2 = b2.split(",")
  b2 = map(lambda x: x.strip(), b2)
  #print(b1)
  #print(b2)
  
  # get size of intersection
  intersect = set(b1).intersection(b2)
  #print(intersect)
  sizeIntersect = len(intersect)
  #print("intersection size = ", sizeIntersect)

  # get size of union
  uni = set(b1).union(b2)
  sizeUnion = len(uni)
  #print("union size = ", sizeUnion)

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

def meanSquareError(jaccardMatrix, minHashMatrix, mseMatrix, docID):
  # Outer loop iterates over rows
  for i in xrange(docID-1):
    # Inner loop iterates over columns
    for l in xrange(docID-1):
      # MSE takes in actual and predicted values as parameters
      mse = numpy.mean(((minHashMatrix[i][l] - jaccardMatrix[i][l])**2))

      # Add value to MSE Matrix
      mseMatrix[i][l] = mse


main()
