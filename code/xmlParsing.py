#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import codecs
import xml.sax
from wikiPage import WikiPage

invertedIndex = {}
pageMap = {}
tertiaryIndex = {}
fileCount = 0
pageCount = 0

class WikiHandler(xml.sax.ContentHandler):
	
	def __init__(self):	
		self.CurrentData = ""
		self.page = ""
		self.title = ""
		self.id = ""
		self.text = ""

	def startElement(self, tag, attributes):
		self.CurrentData = tag
		self.text = ""

		if tag == "page":

			global pageCount, fileCount

			pageCount += 1
			if pageCount > 1000:
				createIntermediateFile()
				fileCount += 1
				pageCount = 0

			self.page = WikiPage()
		
		if tag == "redirect":
			self.page.bodyText = attributes["title"].encode('utf8')

	def endElement(self, tag):
		if tag == "page":
			pageMap[self.page.id] = self.page.title
			self.page.getInvertedIndex(invertedIndex)
			del self.page

		if tag == "title":
			self.page.title = self.title

		if tag == "id" and self.page.id == "":
			self.page.id = self.id

		if tag == "text":
			self.page.text = self.text

	def characters(self, content):
		if self.CurrentData == "title":
			self.title = content.encode('utf8')
		
		if self.CurrentData == "id":
			self.id = content.encode('utf8')
		
		if self.CurrentData == "text":
			self.text += content.encode('utf8')


def xmlParser(xmlFileName):
	parser = xml.sax.make_parser()
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)

	Handler = WikiHandler()
	parser.setContentHandler(Handler)
	
	parser.parse(xmlFileName)


def createIntermediateFile():

	global invertedIndex

	invertedIndex = sorted(invertedIndex.items(), key=lambda x:x[0])

	out = open(str(fileCount) + '.txt', 'w+')

	for posting in invertedIndex:
		out.write(posting[0] + ':'.encode('utf8'))

		for doc in posting[1]:
			out.write(doc + '-'.encode('utf8'))

			for field in posting[1][doc]:
				out.write(field + str(posting[1][doc][field]))

			out.write('|'.encode('utf8'))

		out.write('\n'.encode('utf8'))

	invertedIndex = {}

	out.close()


def mergeFiles():
	out = open(sys.argv[2], 'w+')
	
	for i in range(1, fileCount):
		temp = open('0.txt', 'r')
		final = open('final.txt', 'w+')
		f = open(str(i) + '.txt', 'r')

		term = temp.readline()
		term1 = f.readline()

		while(term != '' and term1 != ''):
			if term.split(':')[0] == term1.split(':')[0]:
				term = term.strip() + term1.split(':')[1]
				final.write(term)
				term = temp.readline()
				term1 = f.readline()

			elif term.split(':')[0] < term1.split(':')[0]:
				final.write(term)
				term = temp.readline()

			elif term.split(':')[0] > term1.split(':')[0]:
				final.write(term1)
				term1 = f.readline()

		while(term != ''):
			final.write(term)
			term = temp.readline()

		while(term1 != ''):
			final.write(term1)
			term1 = f.readline()

		temp.close()
		final.close()
		f.close()

		os.remove('0.txt')
		os.rename('final.txt', '0.txt')

	for i in range(1, fileCount):
		os.remove(str(i) + '.txt')

	os.rename('0.txt', sys.argv[2])


def createTertiaryIndex():
	primary = open(sys.argv[2], 'r')
	char = ''

	prevPos = 0

	line = primary.readline()

	while (line != ''):
		term = line.split(':')

		try:
			newChar = term[0][0] + term[0][1]
		except:
			newChar = term[0][0]

		if newChar == char:
			prevPos = primary.tell()
		else:
			char = newChar
			tertiaryIndex[char] = prevPos
			prevPos = primary.tell()

		line = primary.readline()

	primary.close()


def writeToFile(dictionary, toFile):

	out = open(toFile, 'w+')

	dictionary = sorted(dictionary.items(), key=lambda x:x[0])

	for i in dictionary:
		out.write(str(i[0]) + ':' + str(i[1]) + '\n')

	out.close()


if __name__ == "__main__":
	if len(sys.argv) < 3:
		sys.stderr.write("Usage: " + sys.argv[0] + " <test_dump.xml> <test_index>\n")
		sys.exit(2)

	xmlFileName = sys.argv[1]
	xmlParser(xmlFileName)

	mergeFiles()

	writeToFile(pageMap, 'pageMap.txt')

	createTertiaryIndex()
	writeToFile(tertiaryIndex, 'tertiaryIndex.txt')