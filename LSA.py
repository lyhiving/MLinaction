# _*_ coding: utf-8 _*_

from numpy import *
from numpy import linalg as la
from math import log
from numpy import asarray, sum
import sys

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
				self.A[i,d] += 1
		self.A = self.A.T

	def build2(self):
		print self.wdict.keys()
		self.keys = [k for k in self.wdict.keys() if not k in self.stopwords]
		self.keys.sort()
		self.A = zeros([len(self.keys), self.dcount])
		for i, k in enumerate(self.keys):
			for d in self.wdict[k]:
				self.A[i,d] += 1
		self.A = self.A.T

	def TFIDF(self):
		WordsPerDoc = sum(self.A, axis=0)
		DocsPerWord = sum(asarray(self.A > 0, 'i'), axis=1)
		rows, cols = self.A.shape
		for i in range(rows):
			for j in range(cols):
				self.A[i,j] = (self.A[i,j] / WordsPerDoc[j]) * log(float(cols) / DocsPerWord[i])

	def printA(self):
		print self.A.shape
		print self.A

	def calc(self):
		self.U, self.S, self.Vt = la.svd(self.A)
		return self.U, self.S, self.Vt

	def maxWeight(self,Sigma, weight=0.9):
		sig2 = Sigma ** 2
		sigsum = sum(sig2)
		sigsum_value = sigsum * weight
		for n in range(len(Sigma)):
			if sum(sig2[:n]) > sigsum_value:
				return n

	def simpleTest(self):
		titles =[
			"The Neatest Little Guide to Stock Market Investing",
			"Investing For Dummies, 4th Edition",
			"The Little Book of Common Sense Investing: The Only Way to Guarantee Your Fair Share of Stock Market Returns",
			"The Little Book of Value Investing",
			"Value Investing: From Graham to Buffett and Beyond",
			"Rich Dad's Guide to Investing: What the Rich Invest in, That the Poor and the Middle Class Do Not!",
			"Investing in Real Estate, 5th Edition",
			"Stock Investing For Dummies",
			"Rich Dad's Advisors: The ABC's of Real Estate Investing: The Secrets of Finding Hidden Profits Most Investors Miss" ]

		for t in titles:
			self.parse(t)
		## 生成一个DTM矩阵
		self.build()
		## 输出词频权重
		self.printA()
		self.TFIDF()
		## 输出TF-IDF权重
		self.printA()
		print '----------------------'
		## 计算SVD
		u, s, vt = self.calc()

		print "奇异值矩阵为"
		print s
		n90 = self.maxWeight(s , 0.9)
		print "前项目占据了奇异值信息量的90%:",n90

		Sig3 = mat([[s[0], 0, 0, 0, 0], [0, s[1], 0, 0, 0], [0 ,0 ,s[2], 0, 0], [0 ,0 ,0, s[3], 0], [0, 0, 0, 0, s[4]]])
		#print Sig3
		print "模拟原始矩阵"
		newMat = mat(u[:,0:5]) * Sig3 * mat(vt[0:5,:])
		#print newMat
		t =  mat(self.A) - newMat
		print t


	def corpusTest(self):
		courses = [line.strip() for line in file('data/LSA/coursera_corpus')]
		courses_name = [course.split('\t')[0] for course in courses]
		print courses_name[0:2]
		for t in courses_name:
			self.parse(t)
		self.build2()
		## 输出词频权重
		self.printA()
		self.TFIDF()
		## 输出TF-IDF权重
		self.printA()
		## 计算SVD
		u, s, vt = self.calc()
		print "奇异值矩阵为"
		print u.shape, s.shape, vt.shape
		print s
		n90 = self.maxWeight(s , 0.9)
		print "前项目占据了奇异值信息量的90%:",n90

		emptyMat = zeros(shape=(n90, n90))
		i = 0
		for a in emptyMat:
			a[i] = s[i]
			i = i + 1

	def weiboTest(self):
		texts = [line.strip() for line in file('data/LSA/wb_clean.txt')]
		test_words = [course.split('\t') for course in texts]
		for doc in test_words:
			self.parse(doc)
		self.build2()
		self.printA()
		self.TFIDF()
		self.printA()
		u, s, vt = self.calc()
		print "奇异值矩阵为"
		print u.shape, s.shape, vt.shape
		print s
		n90 = self.maxWeight(s , 0.4)
		print "前项目占据了奇异值信息量的90%:",n90
		n90 = self.maxWeight(s , 0.5)
		print "前项目占据了奇异值信息量的90%:",n90
		n90 = self.maxWeight(s , 0.6)
		print "前项目占据了奇异值信息量的90%:",n90

if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')
	type = sys.getfilesystemencoding()

	stopwords = ['and','edition','for','in','little','of','the','to','a','1','2','3','4']
	ignorechars = ''',:'!()&-'''
	lsa = LSA(stopwords, ignorechars)
	#lsa.simpleTest()
	#lsa.corpusTest()
	#lsa.weiboTest()



	from hmgis.TextMining.parseFile import *
	p = parseCSV('lib/chinesestopwords.txt', 'lib/userdict')
	p.parse('data/LSA/jiangbt.csv', 'data/LSA/wb_clean.txt')
