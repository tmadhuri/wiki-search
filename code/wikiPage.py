#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from tokenizer import *
from stemmer import *
from indexer import *

labels = re.compile(u'(===*.*===*)', flags = re.U)
extLnk = re.compile(u'==*.*External\s*[lL]inks\s*==*', flags = re.U)
ref = re.compile(u'==*.*[rR]eferences\s*==*', flags = re.U)
refTag = re.compile(ur"ref", flags = re.U)
categ = re.compile(ur"\[\[[cC]ategory:(.*?)\]\]", flags = re.DOTALL)
info = re.compile(ur"\{\{Infobox(.*?)\}\}", flags = re.U)

class WikiPage():
	def __init__(self):
		self.id = ""
		self.title = ""
		self.bodyText = ""
		self.infobox = ""
		self.externalLinks = ""
		self.references = ""
		self.categories = ""
		self.text = ""

	def parseText(self):

		self.text = re.sub(refTag, " ", self.text)

		self.categories = str(re.findall(categ, self.text))
		self.text = re.sub(categ, " ", self.text)

		self.infobox = str(re.findall(info, self.text))
		self.text = re.sub(info, " ", self.text)

		self.text = re.split(labels, self.text)
		
		comp = iter(range(len(self.text)))
		for i in comp:
			if re.search(extLnk, self.text[i]):
				try:
					self.externalLinks = self.text[i+1]
					comp.next()
				except:
					pass

			elif re.search(ref, self.text[i]):
				try:
					self.references = self.text[i+1]
					comp.next()
				except:
					pass

			else:
				self.bodyText += self.text[i]

	def tokenize(self):
		self.title = tokenize(self.title, stopWords = "NoRem")
		self.bodyText = tokenize(self.bodyText)
		self.externalLinks = tokenize(self.externalLinks)
		self.references = tokenize(self.references)
		self.infobox = tokenize(self.infobox)
		self.categories = tokenize(self.categories)

	def stem(self):
		self.title = stemList(self.title)
		self.bodyText = stemList(self.bodyText)
		self.externalLinks = stemList(self.externalLinks)
		self.references = stemList(self.references)
		self.infobox = stemList(self.infobox)
		self.categories = stemList(self.categories)

	def getInvertedIndex(self, invertedIndex):
		self.parseText()
		self.tokenize()
		self.stem()
		
		invertedIndex = createIndex(invertedIndex, self.title, self.id, 't')
		invertedIndex = createIndex(invertedIndex, self.bodyText, self.id, 'b')
		invertedIndex = createIndex(invertedIndex, self.externalLinks, self.id, 'e')
		invertedIndex = createIndex(invertedIndex, self.references, self.id, 'r')
		invertedIndex = createIndex(invertedIndex, self.infobox, self.id, 'i')
		invertedIndex = createIndex(invertedIndex, self.categories, self.id, 'c')