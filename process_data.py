import string
from sets import Set
import re
from collections import defaultdict

# out.arff becomes the input file for Weka.  It contains the transformed data
o = open("out_short.arff", "w")
topicList = []
freqList = []
wordSet = Set()
allArticles = []
allBigrams =  []


def classifier():

        # Iterate through each "line" in file
        # line = document in this environment
        for line in open("outcopy.txt", "r"):
                if not line == '\n':
                		processline_Bigram(line)
                        #processLine_WordFreq(line)

        #print ("processLine complete")
        # Creates a unique set of all words used
        #createUniqueSet()
        #print ("unique set complete")
        #allWordsList = list(wordSet)
        
       # count = 0

        # Create a list that conatains a dict matching each word to its freq for each article    
        """for article in freqList:
                article = ''.join(x for x in article if x not in '()')
                article = article.split(",")
                dictionary = defaultdict(lambda: "0", {})

                articleWords = []
                articleFreqs = []
                zip(article[0::2], article[1::2])
                
                for x in article:
                        if x.isdigit():
                                articleFreqs.append(x)
                        else:
                                articleWords.append(x)

                articleWordFreqPairs = zip(articleWords,articleFreqs)
               
                for pair in articleWordFreqPairs:
                        dictionary[pair[0]] = pair[1]

                allArticles.append(dictionary)

                print("article " + str(count) + "added to allArticles")
                count += 1
        

        for topic in topicList:
                if topicList.count(topic) <= 3:
                        while topicList.count(topic) != 0:
                                ind = topicList.index(topic)
                                topicList.pop(ind)
                                allArticles.pop(ind)


        #print("Transform input begin")
        # Transform input does the majority of the text processing
        # to put it into weka friendly format.
        transformInput(topicList, allArticles, allWordsList)"""

        
        while True:
    		try:
        		topicList.remove('\n')
    		except ValueError:
        		break
        while True:
    		try:
        		topicList.remove('')
    		except ValueError:
        		break        		

        #print topicList
        print allBigrams
        bigramOut = open("bigramOut.txt", "w")
        b = 0
        for bi in allBigrams:
        	bigramOut.write(str(b)+" ")
        	#bigramOut.write(topicList[b] + " ")
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

        bigramList = line[(x+2):index]
        bigramList = bigramList.split(",")

       	if bigramList[0] != "":
        	allBigrams.append(bigramList)
        
        


        # Return index of place in line where we're currently at so we
        # can find where to start bigram list
        return {'c':index}





"""def transformInput(topicList, allArticles, allWordsList):
        
        o.write("@RELATION word_frequency\n\n")
        
        # Iterate through all of the words in doc and assign each to it's own "attribute" tag for weka
        # Filter out anything capitalized 
        attrList = removeDuplicates(map(lambda x: re.sub('[^a-z]+', '', x), allWordsList))
        for w in attrList:
                o.write("@ATTRIBUTE " + w + " NUMERIC\n")
        #print ("remove all duplicates start")
        tList = removeDuplicates(topicList)
        o.write("@ATTRIBUTE class-zzz {" + ",".join(tList) + "}\n")
        #print ("remove all duplicates complete")
        o.write("@DATA \n")
        i = -1
        #print ("loop1 start")
        
        # Iterate through all of the data and print out the matrix for word frequency
        for data in allArticles:
                i += 1
                if topicList[i] == "" or topicList[i] == "\n":
                        continue

                frequencies = []
                for word in attrList:
                        frequencies.append(data[word])

                o.write(",".join(frequencies) + "," + re.sub('[\n  :;\[\]\(\)<>]*', '', topicList[i]) + "\n")
                print ("data element " + str(i))
                
        #print ("end")

# Remove any duplicate words and any whitespace/punctuation etc.                         
def removeDuplicates(topicList):
        seen = set()
        for topic in topicList:
                if topic != "" and topic != '\n':
                        seen.add(re.sub('[\n  :;\[\]\(\)<>]*', '', topic))
                        

        return map(lambda x: x, seen)


def createUniqueSet():
        # Create a unique set of words in the word frequency vector
        tempWords = ''.join(freqList)
        tempWords = ''.join(x for x in tempWords if x not in '()')
        tempWords = tempWords.split(",")

        
        # Creates a set of unique words from articles
        for word in tempWords:
                if not word.isdigit():
                        wordSet.add(word)
                        """


classifier()