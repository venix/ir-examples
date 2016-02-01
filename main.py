"""
Copyright (C) 2013 Michael Eleftheriades eleftheriades@gmail.com
This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

Description: A simple example for calculating the similarities between a set of documents
and a query.
    """
import re, math

STOPWORDS = ['a','able','about','across','after','all','almost','also','am','among',
             'an','and','any','are','as','at','be','because','been','but','by','can',
             'cannot','could','dear','did','do','does','either','else','ever','every',
             'for','from','get','got','had','has','have','he','her','hers','him','his',
             'how','however','i','if','in','into','is','it','its','just','least','let',
             'like','likely','may','me','might','most','must','my','neither','no','nor',
             'not','of','off','often','on','only','or','other','our','own','rather','said',
             'say','says','she','should','since','so','some','than','that','the','their',
             'them','then','there','these','they','this','tis','to','too','twas','us',
             'wants','was','we','were','what','when','where','which','while','who',
             'whom','why','will','with','would','yet','you','your', '.', ',', '!' , '?', ' ']
STOPWORDS = ['']

doc1 = "This open source program is distributed under the GNU license"
doc2 = "This software is released under the open source licence"
doc3 = "This open source application calculates the similarity between three documents it is released under open source license"

docs = {
  'doc1': doc1,
  'doc2' :doc2,
  'doc3':doc3
}
query = {
  'query1:': "GNU open source license"
}


class Indexer():
  """
  Class: Indexer
  Description: The indexer splits the documents in the collection into tokens,
  removes any stopwords if required and removes any unecessary symbols.
  It calculates the term frequency of each term in a document and stores it in an
  inverted index (matrix) i.e term doc1, doc2, doc3 along with the tf value of that term in that document.
  """
  def __init__(self, collection, parsed = True):
    self.collection = collection
    self.parsed = parsed

  def createIvertedIndex(self):
    invertedIndex = {}
    for docId, doc in self.collection.iteritems():
      doc = re.sub('[!@#$.?*]', '', doc)
      doc.strip()
      tf = {}
      for token in doc.split():
        token = token.lower()
        token = token.replace(" ", "")

        if token not in STOPWORDS:
          if token not in invertedIndex:
            invertedIndex[token] = {}
          if token not in tf:
            tf[token] = 1
          if docId in invertedIndex[token]:
            tf[token] +=1
          invertedIndex[token][docId] = tf[token]
    return invertedIndex

  def printInvertedIndex(self):

    print "%-15s: " % "Terms: ",
    print "%34s  " % " { docId : Term Frequency(tf) }"
    for k,v in self.createIvertedIndex().iteritems():
      print "%-15s: " % k,
      print "%34s  " % v

  def saveInvertedIndex(self, where='/', database='false'):
    #store the index somewhere on file or database
    pass

class WeightsMatrix():
  def __init__(self, invertedIndex, collectionSize):
    self.invertedIndex = invertedIndex #.copy()
    self.collectionSize = collectionSize

  def calculateIDF(self):
    tokensIDF = {}
    documentFrequency = 0
    for token, postingList in self.invertedIndex.iteritems():
      documentFrequency = len(postingList)
      idf = math.log(float(self.collectionSize)/documentFrequency)
      #idf = math.log(float(self.collectionSize)/documentFrequency, 2.71828)
      tokensIDF[token] = idf
    return tokensIDF

  def printTokensIDF(self):
    for key,value in calculateIDF().iteritems():
      print '{0:<20}'.format(key),
      print '{0:>20.2f}'.format(round(value,2))

  def calculateWeights(self, query=False, idfs=False):
    weights = {}
    tokensIDF = {}
    if not query:
      tokensIDF = self.calculateIDF()
    else:
      tokensIDF = idfs.copy()
    for token in self.invertedIndex:
      for docId in self.invertedIndex[token]:
        tf = self.invertedIndex[token][docId]
        if docId not in weights:
          weights[docId] =  {}
        if token in tokensIDF:
          weights[docId][token] = tf * tokensIDF[token]
    return weights

  def calculateDocumentVectorLength(self):
    docsVectorLength = {}
    for doc, value in self.calculateWeights().iteritems():
      summation = 0
      for term, weight in value.iteritems():
        summation = summation + (weight ** 2)

      docsVectorLength[doc] = math.sqrt(summation)
    return docsVectorLength

  def calculateQueryVectorLength(self, idfs = None):
    queryVectorLength = {}
    tokensIDF = idfs.copy()
    for query, value in self.calculateWeights(True, tokensIDF).iteritems():
      summation = 0
      for term, weight in value.iteritems():
        summation = summation + (weight ** 2)
      queryVectorLength[query] = math.sqrt(summation)
    return queryVectorLength

  def printWeights(self):
    print "PRINTING WEIGHTS"
    for key,value in self.calculateWeights().iteritems():
      print "*"*15,
      print 'DocID:{0:<0}'.format(key),
      print "*"*15

      for k, v in value.iteritems():
        print '{0:<10}'.format(k),
        print '{0:>10}'.format(v)
    print "*"*30

def dotProduct(queryWeights, documentsWeights):
  dotProducts = {}
  for docId, termDocWeight in documentsWeights.iteritems():
    results = 0
    for term, weight in termDocWeight.iteritems():
      for queryId, termQueryWeight in queryWeights.iteritems():
        if term in termQueryWeight:
          results = results + weight * termQueryWeight[term]
    dotProducts[docId] = results
  return dotProducts

def vectorLengthsProduct(docsVectorLengths, queryVectorLengths):
  vectorLengthProducts = {}
  for docId, docVectorLength in docsVectorLengths.iteritems():
    product = 0
    for queryId, queryVectorLength in queryVectorLengths.iteritems():
      product = queryVectorLength * docVectorLength
    vectorLengthProducts[docId] = product
  return vectorLengthProducts

def cosineSimilarity(dotProducts,vectorLengthsProducts):
  similarities = {}
  for docId, dotProduct in dotProducts.iteritems():
    similarity = 0
    similarity = dotProduct / vectorLengthsProducts[docId]
    similarities[docId] = similarity
  return similarities


index = Indexer(docs)

invertedIndexMain = index.createIvertedIndex()
index.printInvertedIndex()
wm = WeightsMatrix(invertedIndexMain, len(docs))

documentsWeights = wm.calculateWeights()

termIDFs = wm.calculateIDF()

docsVectorLengths =  wm.calculateDocumentVectorLength()

queryIndexer = Indexer(query)
invertedQueryIndex = queryIndexer.createIvertedIndex()

qm = WeightsMatrix(invertedQueryIndex, len(query))
queryWeights = qm.calculateWeights(True,termIDFs)

queryVectorLengths = qm.calculateQueryVectorLength(termIDFs)

#Calculating Similarities:
dotProducts=  dotProduct(queryWeights,documentsWeights)
print "\n"
print "Dot Products: ", dotProducts
vectorLengthsProducts = vectorLengthsProduct(docsVectorLengths,queryVectorLengths)
print "\n"
print "Vector Lengths Products: ", vectorLengthsProducts
similarities =  cosineSimilarity(dotProducts,vectorLengthsProducts)

print "\n"
from operator import itemgetter
sorted_similarities = sorted(similarities.iteritems(), key=itemgetter(1))
sorted_similarities.reverse()
for rank, similarity in enumerate(sorted_similarities):
  print "Rank= " + str(rank+1) + " " + similarity[0]+ ": " + str(similarity[1])





