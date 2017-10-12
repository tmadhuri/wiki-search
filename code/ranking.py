#!/usr/bin/env python
# -*- coding: utf-8 -*

import math
import timeit
from scipy import spatial
from tokenizer import *
from stemmer import *
from indexer import *

tertiaryIndex = {}
pageMap = {}


def parseQuery(query):
	query = tokenize(query, stopWords = "NoRem")

	queryTerms = []
	queryTermFields = []

	comp = iter(range(len(query)))

	for i in comp:
		if query[i] in ['t', 'b', 'e', 'r', 'i', 'c']:
			
			if query[i+1] in queryTerms:
				ind = queryTerms.index(query[i+1])
				queryTermFields[ind].append(query[i])
			
			else:
				queryTerms.append(query[i+1])
				queryTermFields.append([query[i]])
			
			comp.next()

		else:
			if query[i] in queryTerms:
				ind = queryTerms.index(query[i])
				queryTermFields[ind].extend(['t', 'b', 'e', 'r', 'i', 'c'])

			else:
				queryTerms.append(query[i])
				queryTermFields.append(['t', 'b', 'e', 'r', 'i', 'c'])

	queryTerms = stemList(queryTerms)

	return (queryTerms, queryTermFields)


def getPostingsList(term):
	try:
		startIndex = tertiaryIndex[term[0] + term[1]]
	except:
		startIndex = tertiaryIndex[term[0]]

	primary = open('../primaryIndex.txt', 'r')
	secondary = open('../secondaryIndex.txt', 'r')

	secondary.seek(int(startIndex))

	line = secondary.readline()

	while(line != '' and line.split(':')[0] != term):
		line = secondary.readline()

	primaryLine = float(line.split(':')[1])

	primary.seek(primaryLine)
	postings = primary.readline()

	return postings


def getScore(index, queryTermFields, fieldFreq, n):
	tf = 0.0

	fields = re.split(ur"(t|b|e|r|i|c)", fieldFreq, flags = re.U)

	for i in queryTermFields[index]:
		try:
			if i == 't':
				tf += (10 * float(fields[fields.index(i) + 1]))
			else:
				tf += float(fields[fields.index(i) + 1])
		except ValueError:
			tf += 0.0

	try:
		tf = 1.0 + math.log(float(tf))
	except ValueError:
		tf = 1.0

	idf = math.log(10000000 / float(n))

	return (tf*idf, idf)


def getDocVec(queryTerms, queryTermFields):
	docVecs = {}
	idfMap = {}

	for i in range(len(queryTerms)):
		try:
			postingsList = getPostingsList(queryTerms[i]).split(':')[1].split('|')
		except:
			continue

		for j in range(len(postingsList)-1):
			doc = postingsList[j]
			doc = doc.split('-')

			if doc[0] not in docVecs:
				docVecs[doc[0]] = [0 for x in range(len(queryTerms))]

			docVecs[doc[0]][i], idf = getScore(i, queryTermFields, doc[1], len(postingsList))

			idfMap[queryTerms[i]] = idf

	return docVecs, idfMap


def getQueryVec(queryTerms, queryTermFields, idfMap):
	queryVec = [0 for x in range(len(queryTerms))]

	for i in range(len(queryTerms)):
		try:
			tf = 1.0 + math.log(float(len(queryTermFields[i])))
		except ValueError:
			tf = 1.0

		idf = idfMap[queryTerms[i]]

		queryVec[i] = tf*idf

	return queryVec


def computeSimilarity(queryVec, docVecs, n):
	similarity = {}

	if n == 1:
		for doc in docVecs:
			similarity[doc] = docVecs[doc][0]

	else:
		for doc in docVecs:
			similarity[doc] = 1 - spatial.distance.cosine(queryVec, docVecs[doc])

	return similarity


def displayPages(similarity):
	similarity = sorted(similarity.items(), key=lambda x:x[1], reverse = True)
	
	i = 0

	while ((i < 10) and (i < len(similarity))):
		print 'PageId: ', similarity[i][0], '--- PageTitle: ', pageMap[similarity[i][0]]
		i += 1


def getRankedDocuments(query):
	queryTerms, queryTermFields = parseQuery(query)

	docVecs, idfMap = getDocVec(queryTerms, queryTermFields)

	queryVec = getQueryVec(queryTerms, queryTermFields, idfMap)

	similarity = computeSimilarity(queryVec, docVecs, len(queryTerms))

	displayPages(similarity)


if __name__ == "__main__":
	tertiary = open('../tertiaryIndex.txt', 'r')

	for line in tertiary:
		line = line.split(':')
		tertiaryIndex[line[0].strip()] = line[1].strip()

	pagemap = open('../pageMap.txt', 'r')

	for line in pagemap:
		line = line.split(':')
		pageMap[line[0].strip()] = line[1].strip()


	while(1):
		query = raw_input('>>>')
		
		startTime = timeit.default_timer()		
		getRankedDocuments(query)
		
		elapsedTime = timeit.default_timer() - startTime
		print "time : ", elapsedTime		
