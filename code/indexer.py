#!/usr/bin/env python
# -*- coding: utf-8 -*-

def createIndex(invertedIndex, tokens, docId, field):
	
	for i in tokens:
		
		if i in invertedIndex and docId in invertedIndex[i]:
			if field in invertedIndex[i][docId]:
				invertedIndex[i][docId][field] += 1
			else:
				invertedIndex[i][docId][field] = 1

		elif i in invertedIndex:
			invertedIndex[i][docId] = {}
			invertedIndex[i][docId][field] = 1

		else:
			invertedIndex[i] = {}
			invertedIndex[i][docId] = {}
			invertedIndex[i][docId][field] = 1

	return invertedIndex