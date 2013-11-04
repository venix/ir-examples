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
# A simple document i.e a document that contains just text
class Document(object)
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
	
	
	def __init__(self, title, docID, content, stemming= None, corpus = None ):
		self._title = title
		self._docID = docID #user defined for now
		self._content = content #content of the document a string for now
		self._corpus= corpus #the corpus that this document belong's to.
		self._tf= {}  
		self._weights = {} #tf-idf weights
		#Cleaning the document previously parsed
		self._content = re.sub('[!@#$.?*]', '', self._content)
		self._content.strip()
		self._content = re.sub('[!@#$.?*!"#%\'()*+,-./:;<=>&?@[\]^_`{|}~]', '', self._content)
		self._stemming = None
		#splitting the document and calculating term frequncy
		"""What i need for a document:
		idf 
		tf 
		documentVectorLength
		weight
		tfidf 
		"""
		#Calculate TF of all terms in the document and store in dictionary with Key: token, Value: tf
		for token in self._content.split():
			token = token.lower()
			token = token.replace(" ", "")
			if token not in self.STOPWORDS:
				if token not in self._tf:
					self._tf[token] = 1
				else:
					self._tf[token] +=1 

	
	def _set_corpus(self,corpus):
		""" need to recalculate weights(tf-idf) if the corpus changes 
			disabled for now
		"""
		#self._corpus = corpus

	@property
	def docID(self):
		return self._id

	@property 
	def terms(self):
		return self._tf


	@property
	def tokens(self):
		"""
		returns only tokens, with removed STOPWORDS, if it was enabled 
		and stemmed if it was enabled
		"""
		return self._tf.keys()






	def load(path):
		"""
		TODO: load a document from a specified filesystem path
		"""
		pass
	def save(self, path):
		"""
		TODO: save a document in txt format?  
		"""



	def __str__(self):
		string = "id: " + str(self.docId) + " content: " + self.content 
		return string

	def __unicode__(self):
		#to print with unicode "print unicode(object_name)"
		string = "id: " + str(self.docId) + " content: " + self.content 
		return unicode(string)