"""
Copyright (C) 2013 Michael Eleftheriades
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
#Corpus - A collection of documents
import re, math, unicodedata
from pprint import pprint
class Corpus():
	#A collection of documents 
	#documents = [doc1(object), doc2 , doc3]
	def __init__(self, documents = [], query = [], scheme="TFIDF"):
		#invertedIndex {'term' : {docID: tf} }
		self.documents = documents
		self.n = len(self.documents)
		self.scheme = scheme
		self.query = query
		self.idfs = {} #{term: idf}
		self.dfs = {} #{term: df}
		self.weights = {} #{term: {doc:weight}}
		self.qweights = {} #{term: {doc:weight}}
		self.dvl = {} #{doc: document_vector_length}
		self.qdvl = {} # {doc: query vector length }
		self.initialise()
	def initialise(self):
		self.df()
		#print "Document frequencies of terms: "
		#pprint(self.dfs)
		self.idf()
		#print "Document inversed frequencies of terms: "
		#pprint(self.idfs)
		if self.documents:
			for document in self.documents:
				summation = 0
				for term, idf_v in self.idfs.iteritems():
				 	current_weight = self.calculate_weight(document,term)
				 	if term not in self.weights:
				 		self.weights[term] = {}
				 		self.weights[term][document]= current_weight
				 	else: 
						self.weights[term][document] = current_weight
					summation += current_weight ** 2
				current_dvl = self.calculate_dvl(summation)
				self.dvl[document] = current_dvl
			print "We are here1 : "
			print "Docs dvl ", pprint(self.weights)
			# print "Weights: "
			# for term, values in self.weights.iteritems():
			# 	print "term: ", term
			# 	#print "Values: ", values
			# 	for document, weight in values.iteritems():
			# 	 	print "{%s: %f}" %(document.docId, weight)
			#self.printWeights()
		if not self.query:
			self.query = Document('q', 'love time contact mathematics')
			summation = 0
			for term, idf_v in self.idfs.iteritems():
			 	current_weight = self.calculate_weight(self.query,term)
			 	if term not in self.qweights:
			 		self.qweights[term] = {}
			 		self.qweights[term][self.query]= current_weight
			 	else: 
					self.weights[term][self.query] = current_weight
				summation += current_weight ** 2
			current_qdvl = self.calculate_dvl(summation)
			self.qdvl[self.query] = current_qdvl
			print "We are here: "
			#self.printWeights(True)
			print "Queries dv ", pprint(self.qweights)
		# print "Weights: "
		# for term, values in self.qweights.iteritems():
		# 	print "term: ", term
		# 	#print "Values: ", values
		# 	for document, weight in values.iteritems():
		# 	 	print "{%s: %f}" %(document.docId, weight)
		##################### TEMP TO PRINT SIMILARITIES ##############
		print "SIMILARITIES: "
		for document in self.documents:
			print "Document No: ", document.docId
			print self.similarity(self.query,document)
	def printWeights(self, query=False):
		if not query:
			w = self.weights
		else: w = self.qweights
		for term, values in w.iteritems():
			print "term: ", term
			#print "Values: ", values
			for document, weight in values.iteritems():
			 	print "{id%s: %f}" %(document.docId, weight)

	def df(self):
		#return the document frequency of a term in the collection
		#for now calculate the documentFrequency of all terns in the collection
		for document in self.documents:
			for term, tf in document.terms.iteritems():
				if term:
					term = self.translate_non_alphanumerics(term)

					if term in self.dfs:
						self.dfs[term] += 1
					else:
						self.dfs[term] = 1
	
	def translate_non_alphanumerics(self,to_translate, translate_to=u''):
		not_letters_or_digits = u'!"#%\'()*+,-./:;<=>&?@[\]^_`{|}~'
		translate_table = dict((ord(char), translate_to) for char in not_letters_or_digits)
		return to_translate.translate(translate_table)

	def idf(self):
		#for document in self.documents:
		for term, df in self.dfs.iteritems():
			n = self.n 
			#print " term: %s df: %f n: %f" % (term, df, n)
			#print "n/df= ", n/df
			self.idfs[term] = abs(math.log10(float(self.n)/ df))

	def wtf(self, document,term):
		#weighted term frequency 1 + log(tf) if tf > 0 else 0
		value = 0
		if term in document.terms:
			value = document.terms[term]
		#wtf_v = (1 + math.log(float(value))) if value > 0 else 0
		#wtf_v = (float(value)) if value > 0 else 0
		wtf_v = (1 + math.log10(float(value))) if value > 0 else 0
		#this didn't work for some reason
		#wtf_v = (1 + math.log(document.temrs[term])) if document.terms[term] > 0 else 0
		return wtf_v

	def calculate_weight(self, document, term):
		if term in self.idfs:
			#self.weights[term][document] = wtf(document) *self.idfs[term]
			return self.wtf(document,term) * self.idfs[term]

	def calculate_dvl(self,summed_weights ):
		result = abs(math.sqrt(summed_weights))
		return result

	def similarity(self,query, document):
		#similarity is the sum of the product of the weights of the two documents
		#divded bu their vector lengths
		 #weights: #{term: {doc:weight}}
		summation = 0
		for term, values in self.qweights.iteritems():
			for queryId, qweight in values.iteritems():
		 		summation += qweight * self.weights[term][document]
		dotproduct = summation
		if self.qdvl[query] != 0 and self.dvl[document] !=0 :
			simialrity = float(dotproduct) / (self.qdvl[query] * self.dvl[document])
		else: simialrity = 0
		return simialrity

	def append(document):
		self.documents.append(document)
	def __str__(self):
		string = "DOTO: string: __str__ "
		return string

	def __unicode__(self):
		#to print with unicode "print unicode(object_name)"
		string = "DOTO: unicode __unicode__"
		return unicode(string)
