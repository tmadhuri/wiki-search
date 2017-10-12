#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == "__main__":
	primary = open('../primaryIndex.txt', 'r')
	secondary = open('secondaryIndex.txt', 'w+')

	prevPos = 0

	line = primary.readline()

	while (line != ''):
		term = line.split(':')
		secondary.write(term[0] + ':' + str(prevPos) + '\n')

		prevPos = primary.tell()
		line = primary.readline()
