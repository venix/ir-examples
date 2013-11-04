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

#remove this stopwords from the documents
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

docs = {'doc1': doc1, 'doc2' :doc2, 'doc3':doc3 }
query = {'query1:'  : "GNU open source license" }


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
		""" 
		function : createIvertedIndex 
		description: creates and returns inverted index, including term frequency
		"""
		#invertedIndex {'term' : {docID: tf} }
		invertedIndex = {} 
		for docId, doc in self.collection.iteritems():
			#Cleaning the doc content
			doc = re.sub('[!@#$.?*]', '', doc)
			doc.strip()
			#To store the term frequencies as {'term' : tf}
			#temp storage of term frequencies of the current document
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
			#invertedIndex.pop("")
		return invertedIndex

	def printInvertedIndex(self):
		#print self.createIvertedIndex()
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
		#self.tokensIDF = {}

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
	
	def calculateWeights(self, query=False, idfs = False):
		# invertedIndex returns {'term': [doc1,doc2] , 'term2' : [doc1,doc3]}
		weights = {}
		tokensIDF = {} 
		if not query:
			tokensIDF = self.calculateIDF()
			#print "DOCUMENTS IDFS ", tokensIDF
		else: #if is query 
			tokensIDF = idfs.copy()
			#print "QUERY IDFS ", tokensIDF
		for token in self.invertedIndex:
			#print "posting list : " , invertedIndex[term]
			for docId in self.invertedIndex[token]:
				tf = self.invertedIndex[token][docId]
				#weighted term frequency 
				#wtf = (1 + math.log10(tf)) if tf > 0 else 0
				#print "tf of term:%s of DocID: %s is %s" %(term,docID, tf)
				if docId not in weights:
					weights[docId] =  {}
				#tf uses non-log scaled term frequency wtf uses log scaled
				if token in tokensIDF:
					weights[docId][token] = tf * tokensIDF[token]
		#print weights
		#print "Weights:", weights
		#{docID : {"term": weight }}
		return weights

	def calculateDocumentVectorLength(self):
		docsVectorLength = {}
		for doc, value in self.calculateWeights().iteritems():
			summation = 0
			for term, weight in value.iteritems():
				# if doc == 'doc1':
				# 	print "term: %s weight: %s " % (term,weight)
				summation =  summation  + (weight ** 2)
				#print "Sum: ", summation
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
			# print "Doc%s  : %s " %  (str(i), key)
			print "*"*15,
			print 'DocID:{0:<0}'.format(key),
			print "*"*15
			#print '{0:>40}'.format(value)
			for k, v in value.iteritems():
				print '{0:<10}'.format(k),
				print '{0:>10}'.format(v)
		print "*"*30

#CALCULATE COSINE SIMILARITY HERE:
# NEEDS document weights = documentsWeights and query weights = queryWeights 
def dotProduct(queryWeights, documentsWeights):
	#queryWeights, documentsWeights return #{docID/queryID : {"term": weight }}
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

#Finaly the similarity between the Query Document and the Documents in the colection
def cosineSimilarity(dotProducts,vectorLengthsProducts):
	similarities = {}
	for docId, dotProduct in dotProducts.iteritems():
		similarity = 0
		similarity = dotProduct / vectorLengthsProducts[docId]
		similarities[docId] = similarity
	return similarities


#Initialise index give the collection
index = Indexer(docs)
#Creat the inverted Index 
invertedIndexMain = index.createIvertedIndex()
index.printInvertedIndex()
wm = WeightsMatrix(invertedIndexMain, len(docs))
#Calculating document weights (tf-idf values)
documentsWeights = wm.calculateWeights()
#wm.printWeights()
#PRINTING IDF VALUES 
termIDFs = wm.calculateIDF()
# print "TERMS IDF : ", termIDFs
#PRINTING DVL VALUES: 
docsVectorLengths =  wm.calculateDocumentVectorLength()
# print "DOCS vector lengths ", docsVectorLengths

# **************** QUERY CALCULATIONS ***************
#A query is a document that needs to be indexed similarly
#print "*"*25 + " QUERY " + "*"*25
queryIndexer = Indexer(query)
invertedQueryIndex = queryIndexer.createIvertedIndex()
#queryIndexer.printInvertedIndex()
qm= WeightsMatrix(invertedQueryIndex, len(query))
queryWeights = qm.calculateWeights(True,termIDFs)
# print "PRINTING WEIGHTS"
# print queryWeights
#Printing Query Weights
# for key,value in queryWeights.iteritems():
# 	# print "Doc%s  : %s " %  (str(i), key)
# 	print "*"*15,
# 	print 'DocID:{0:<0}'.format(key),
# 	print "*"*15
# 	#print '{0:>40}'.format(value)
# 	for k, v in value.iteritems():
# 		print '{0:<10}'.format(k),
# 		print '{0:>10}'.format(v)
# print "*"*30
#Calculating query vector lengths

queryVectorLengths =  qm.calculateQueryVectorLength(termIDFs)
#print queryVectorLengths

#Calculating Similarities:
dotProducts=  dotProduct(queryWeights,documentsWeights)
print "\n"
print "Dot Products: ", dotProducts
vectorLengthsProducts = vectorLengthsProduct(docsVectorLengths,queryVectorLengths)
print "\n"
print "Vector Lengths Products: ", vectorLengthsProducts
similarities =  cosineSimilarity(dotProducts,vectorLengthsProducts)
# print "**" * 10
# print "--" * 10
# print "Similarities : ", similarities
# print "--" * 10
# print "**" * 10
print "\n"
from operator import itemgetter
sorted_similarities = sorted(similarities.iteritems(), key=itemgetter(1))
sorted_similarities.reverse()
for rank, similarity in enumerate(sorted_similarities):
	print "Rank= " + str(rank+1) + " " + similarity[0]+ ": " + str(similarity[1])
# for key,value in sorted_similarities.iteritems():
# 	# print "Doc%s  : %s " %  (str(i), key)
# 	print "*"*15,
# 	print 'DocID:{0:<0}'.format(key),
# 	print "*"*15
# 	print '{0:>40}'.format(value)
	



