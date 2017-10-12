#!/usr/bin/env python
# -*- coding: utf-8 -*-

tertiaryIndex = {}

def writeToFile(dictionary, toFile):

	out = open(toFile, 'w+')

	dictionary = sorted(dictionary.items(), key=lambda x:x[0])

	for i in dictionary:
		out.write(str(i[0]) + ':' + str(i[1]) + '\n')

	out.close()


if __name__ == "__main__":
	secondary = open('../secondaryIndex.txt', 'r')

	char = ''

	prevPos = 0

	line = secondary.readline()

	while (line != ''):
		term = line.split(':')

		try:
			newChar = term[0][0] + term[0][1]
		except:
			newChar = term[0][0]

		if newChar == char:
			prevPos = secondary.tell()
		else:
			char = newChar
			tertiaryIndex[char] = prevPos
			prevPos = secondary.tell()

		line = secondary.readline()

	writeToFile(tertiaryIndex, 'tertiaryIndex.txt')