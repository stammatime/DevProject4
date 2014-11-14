import string
import re
import numpy
import pprint
import random
from sets import Set

allDics = {}
  
def main():

  # Open outcopy2.txt and save as variable since it'll be used in several different ways
  inputFile = open("bigramOut.txt", "r")

  docID = 1

  for document in inputFile:
    if not document == '\n':
      allDics[docID] = { 'bigrams' : extractBigram(document)}
      docID += 1
    
  # Dictionary of random numbers
  k = 16
  randoDics = []
  for x in range(k):
    randoDics.append({'x':random.random(), 'y':random.random()})
  

  # Create the jaccard similiarity matrix.  Will be (#docs x #docs).
  simMatrix = [[0 for x in xrange(docID-1)] for x in xrange(docID-1)]
  mseMatrix = [[0 for x in xrange(docID-1)] for x in xrange(docID-1)]
  #minHashMatrix = [[0 for x in xrange(docID-1)] for x in xrange(docID-1)]

  minHashMatrix = [[1.0, 1.0, 0.0, 0.06, 0.02, 0.0, 0.0],
 [0, 1.0, 0.0, 0.04, 0.0, 0.0, 0.003],
 [0, 0, 1.0, 0.0, 0.0, 0.0, 0.0],
 [0, 0, 0, 1.0, 0.11, 0.0, 0.0],
 [0, 0, 0, 0, 1.0, 0.03, 0.0],
 [0, 0, 0, 0, 0, 1.0, 0.0],
 [0, 0, 0, 0, 0, 0, 1.0]]

  # iterate through all of the documents comparing each one to the others
  # Outer loop gets b1
  for eachDocID in allDics:
    b1 = allDics[eachDocID]['bigrams']
    i = eachDocID
    while i < docID:
      b2 = allDics[i]['bigrams']
      jaccard = computeJaccard(b1, b2)
      addToMatrix(simMatrix, eachDocID, i, jaccard)
      
      #print(jaccard)
      #print('\n\n')
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


  # Calculate the MSE between our Jaccard matrix and the minhash matrix
  meanSquareError(simMatrix, minHashMatrix, mseMatrix, docID)
  minHash(inputMatrix, randoDics, docID, len(bigramList), k)

  pp = pprint.PrettyPrinter(depth=7)
  #pp.pprint(simMatrix)
  #pp.pprint(inputMatrix)
  #pp.pprint(mseMatrix)


# Len = len(bigramList) = #bigrams
def minHash(inputMatrix, randoDics, numDocs, length, k):
  # Big prime number to mod by 
  bigPrimeNumber = 22801760837
  i = 0
  
  # Sig matrix
  sigMatrix = [range(numDocs-1) for x in range(k)]
  pp = pprint.PrettyPrinter(depth=80)
  
  
  for ck in range(k):
    # iterate over documents
    for d in range(numDocs-1):
      minTemp = bigPrimeNumber
      i = 0
      # Iterate over each bigram in the particular document
      while i < length:
        if inputMatrix[i][d] == 1 :
          possMin = (randoDics[ck]['x']*i+randoDics[ck]['y']%bigPrimeNumber)%numDocs
          if possMin < minTemp:
            minTemp = possMin
        i += 1
      # Add to the signature matrix the min hash value
      sigMatrix[ck][d] = minTemp


  pp.pprint(sigMatrix)

  # Insert similarity computation here
      

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
