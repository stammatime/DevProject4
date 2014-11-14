import string
from sets import Set
import re
from collections import defaultdict

# out.arff becomes the input file for Weka.  It contains the transformed data
o = open("out.txt", "w")
topicList = []
freqList = []
wordSet = Set()
allArticles = []
allBigrams =  []


def classifier():

        # Iterate through each "line" in file
        # line = document in this environment
        for line in open("preprocess.txt", "r"):
        		line = line.rstrip('\n \r')
                	if len(line) > 0:
                		processline_Bigram(line)
                        #processLine_WordFreq(line)
    
#    	for docID in range(len(allBigrams)):
#    		print (str(docID+1) + ','.join(allBigrams[docID]) + "\n")
        	
#    	for docID in range(len(topicList)):
#    		print (str(docID+1) + ','.join(topicList[docID]) + "\n")
        
        bigramOut = open("bigramOut.txt", "w")
        b = 0
        for bi in allBigrams:
        	bigramOut.write(str(b+1)+" ")
        	bigramOut.write("<" + topicList[b] + "> ")
        	bigramOut.write("<" + ",".join(allBigrams[b])+ ">" + "\n")


        	#+ " " +topicList[b] + " " + allBigrams[b].join("")
        	b += 1
        print("Transform input end")
        bigramOut.close()
        o.close()

def processline_Bigram(line):
        # first is doc id
        count = 0
        # Iterate through the first few characters in line to remove document
        # ID and space before topics list
        for x in range(0, len(line)):
                if line[x] == "<":
                        count += 1
                        break

        # Set the line to be the line without docID and space
        line = line[count:]
        
        # Get topic value(s); be sure not to print blank topics
        topicValue = processTopic(x, line)
        x = topicValue["c"]
        topic = topicValue["string"]
        
        
        # Eliminate Place value(s)
        placeValue = processPlace(x+1, line)
        x = placeValue["c"]
        
        # Get bigram list end position so we can ignore it
        bigramValue = processBigram(x+1, line)
        x = bigramValue["c"]

        # Ensure that there is only one topic per doc.  If multiple, take the first one
        topics = topic.split(",")
        topic = topics[0]

        topicList.append(topic)

# This method read each line (document) and throws out docid, bigram list, places list





def processTopic(x, line):
        index = 0
        string = ""
        for c in range(x, len(line)):
                if not line[c] == ">":
                        string += line[c]
                else:
                        index = c
                        break
        
        return {'c':index,'string':string}


def processPlace(x, line):
        index = 0
        for c in range(x, len(line)):
                if line[c] == ">":
                        index = c
                        break

        # Return index of place in line where we're currently at so we
        # can find where to start bigram list
        return {'c':index}

def processBigram(x, line):
        index = 0
        
        AllBigramList = []
        
        bigramList= []
        for c in range(x, len(line)):
				
                if line[c] == ">":
                        index = c
                        break

        #beginning of bigram to end of bigram
        bigramList = line[(x+2):index]

        bigramList = bigramList.split(",")

       	#if bigramList[0] != "":
        allBigrams.append(bigramList)
        
        


        # Return index of place in line where we're currently at so we
        # can find where to start bigram list
        return {'c':index}

classifier()