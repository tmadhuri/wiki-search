#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.sax
import sys

pageMap = {}

class WikiHandler(xml.sax.ContentHandler):
	
	def __init__(self):	
		self.CurrentData = ""
		self.page = ""
		self.title = ""
		self.id = ""
		self.id2 = ""
		self.title2 = ""

	def startElement(self, tag, attributes):
		self.CurrentData = tag

		if tag == "page":
			self.id = ""
			self.title = ""

	def endElement(self, tag):
		if tag == "page":
			print self.id
			pageMap[self.id] = self.title

		if tag == "title":
			self.title = self.title2

		if tag == "id" and self.id == "":
			self.id = self.id2

	def characters(self, content):
		if self.CurrentData == "title":
			self.title2 = content.encode('utf8')
		
		if self.CurrentData == "id":
			self.id2 = content.encode('utf8')


def xmlParser(xmlFileName):
	parser = xml.sax.make_parser()
	parser.setFeature(xml.sax.handler.feature_namespaces, 0)

	Handler = WikiHandler()
	parser.setContentHandler(Handler)
	
	parser.parse(xmlFileName)


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

	writeToFile(pageMap, sys.argv[2])