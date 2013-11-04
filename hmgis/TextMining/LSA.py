# _*_ coding: utf-8 _*_

from math import log

from numpy import *
from numpy import linalg as la
from numpy import asarray, sum


class LSA(object):
	def __init__(self, stopwords, ignorechars):
		self.stopwords = stopwords
		self.ignorechars = ignorechars
		self.wdict = {}
		self.dcount = 0

	def parse(self, doc):
		#words = doc.split();
		words = doc
		for w in words:
			w = w.lower().translate(None, self.ignorechars)
			if w in self.stopwords:
				continue
			elif w in self.wdict:
				self.wdict[w].append(self.dcount)
			else:
				self.wdict[w] = [self.dcount]
		self.dcount += 1

	## 生成一个DTM矩阵
	def build(self):
		self.keys = [k for k in self.wdict.keys() if len(self.wdict[k]) > 1]
		self.keys.sort()
		self.A = zeros([len(self.keys), self.dcount])
		for i, k in enumerate(self.keys):
			for d in self.wdict[k]:
				self.A[i, d] += 1
		self.A = self.A.T

	def build2(self):
		#print self.wdict.keys()
		self.keys = [k for k in self.wdict.keys() if not k in self.stopwords]
		self.keys.sort()
		self.A = zeros([len(self.keys), self.dcount])
		for i, k in enumerate(self.keys):
			for d in self.wdict[k]:
				self.A[i, d] += 1
		self.A = self.A.T

	def TFIDF(self):
		WordsPerDoc = sum(self.A, axis=0)
		DocsPerWord = sum(asarray(self.A > 0, 'i'), axis=1)
		rows, cols = self.A.shape
		for i in range(rows):
			for j in range(cols):
				self.A[i, j] = (self.A[i, j] / WordsPerDoc[j]) * log(float(cols) / DocsPerWord[i])

	def printA(self):
		print self.A.shape
		print self.A

	def calc(self):
		self.U, self.S, self.Vt = la.svd(self.A)
		return self.U, self.S, self.Vt

	def maxWeight(self, Sigma, weight=0.9):
		sig2 = Sigma ** 2
		sigsum = sum(sig2)
		sigsum_value = sigsum * weight
		for n in range(len(Sigma)):
			if sum(sig2[:n]) > sigsum_value:
				return n

