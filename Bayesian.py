# _*_ coding: utf-8 _*_
import sys
import re
from numpy import *
from twisted.test.test_pb import bigString
import jieba.posseg as pseg
import jieba

class bayesian:
	def loadDataSet(self):
		postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
		               ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
		               ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
		               ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
		               ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
		               ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
		classVec = [0, 1, 0, 1, 0, 1]    #1 is abusive, 0 not
		return postingList, classVec

	## 寻找出单个文档，其中词汇不重复
	def createVocabList(self, dataSet):
		vocabSet = set([])  #create empty set
		for document in dataSet:
			vocabSet = vocabSet | set(document) #union of the two sets
		return list(vocabSet)

	## 计算一个字符串的单词在词包中的位置
	def setOfWords2Vec(self, vocabList, inputSet):
		returnVec = [0] * len(vocabList)
		for word in inputSet:
			if word in vocabList:
				returnVec[vocabList.index(word)] += 1
			else:
				print "the word: %s is not in my Vocabulary!" % word
		return returnVec

	## 计算先验概率
	## P(B|A) = P(B)P(A|B)/P(B)P(A|B) + P(C)P(A|C)
	def trainNB0(self, trainMatrix, trainCategory):
		numTrainDocs = len(trainMatrix)
		numWords = len(trainMatrix[0])
		## 先验概率
		pAbusive = sum(trainCategory) / float(numTrainDocs)
		p0Num = ones(numWords)
		p1Num = ones(numWords)      #change to ones()
		p0Denom = 2.0;
		p1Denom = 2.0                        #change to 2.0
		## 类型AB的先验概率是根据此类型中词汇在词包中出现的次数除以总次数
		for i in range(numTrainDocs):
			if trainCategory[i] == 1:
				p1Num += trainMatrix[i]
				p1Denom += sum(trainMatrix[i])
			else:
				p0Num += trainMatrix[i]
				p0Denom += sum(trainMatrix[i])
		p1Vect = log(p1Num / p1Denom)         #change to log()
		p0Vect = log(p0Num / p0Denom)          #change to log()
		return p0Vect, p1Vect, pAbusive

	## 比较概率
	def classifyNB(self, vec2Classify, p0Vec, p1Vec, pClass1):
	## 由于所有类型的全概率都是一样的（分母一样），因此可以纯比分子
		p1 = sum(vec2Classify * p1Vec) + log(pClass1)    #element-wise mult
		p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
		if p1 > p0:
			return 1
		else:
			return 0

	## 测试单个词汇的类型
	def testingNB(self):
	## 加载已有数据集
		listOPosts, listClasses = self.loadDataSet()
		myVocabList = self.createVocabList(listOPosts)
		trainMat = []
		for postinDoc in listOPosts:
			trainMat.append(self.setOfWords2Vec(myVocabList, postinDoc))
		## 计算已有数据集中的先验概率
		p0V, p1V, pAb = self.trainNB0(array(trainMat), array(listClasses))

		## 测试不同字符串的后验概率
		testEntry = ['love', 'my', 'dalmation']
		thisDoc = array(self.setOfWords2Vec(myVocabList, testEntry))
		print testEntry, 'classified as: ', self.classifyNB(thisDoc, p0V, p1V, pAb)
		testEntry = ['stupid', 'garbage']
		thisDoc = array(self.setOfWords2Vec(myVocabList, testEntry))
		print testEntry, 'classified as: ', self.classifyNB(thisDoc, p0V, p1V, pAb)

## 电子邮件测试器
class emailClassfier:
	def textParse(self, bigString):
		import re

		listOfTokens = re.split(r'\W*', bigString)
		return [tok.lower() for tok in listOfTokens if len(tok) > 2]

	def spamTest(self, bayesian):
		docList = [];
		classList = [];
		fullText = []
		for i in range(1, 26):
			wordList = self.textParse(open('data/bayesian/email/spam/%d.txt' % i).read())
			docList.append(wordList)
			fullText.extend(wordList)
			classList.append(1)
			wordList = self.textParse(open('data/bayesian/email/ham/%d.txt' % i).read())
			docList.append(wordList)
			fullText.extend(wordList)
			classList.append(0)
		vocabList = bayesian.createVocabList(docList)#create vocabulary
		trainingSet = range(50);
		testSet = []           #create test set
		for i in range(10):
			randIndex = int(random.uniform(0, len(trainingSet)))
			testSet.append(trainingSet[randIndex])
			del (trainingSet[randIndex])
		trainMat = [];
		trainClasses = []
		for docIndex in trainingSet:#train the classifier (get probs) trainNB0
			trainMat.append(bayesian.setOfWords2Vec(vocabList, docList[docIndex]))
			trainClasses.append(classList[docIndex])
		p0V, p1V, pSpam = bayesian.trainNB0(array(trainMat), array(trainClasses))
		errorCount = 0
		for docIndex in testSet:        #classify the remaining items
			wordVector = bayesian.setOfWords2Vec(vocabList, docList[docIndex])
			if bayesian.classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
				errorCount += 1
				print "classification error", docList[docIndex]
		print 'the error rate is: ', float(errorCount) / len(testSet)
		#return vocabList,fullText





if __name__ == "__main__":
	reload(sys)                         # 2
	sys.setdefaultencoding('utf-8')
	type = sys.getfilesystemencoding()

	bayesian = bayesian()
	listOPosts, listClasses = bayesian.loadDataSet()
	myVocaList = bayesian.createVocabList(listOPosts)
	print myVocaList
	print bayesian.setOfWords2Vec(myVocaList, listOPosts[0])
	trainMat = []
	for postinDoc in listOPosts:
		trainMat.append(bayesian.setOfWords2Vec(myVocaList, postinDoc))

	p0V, p1V, pAb = bayesian.trainNB0(trainMat, listClasses)
	print p0V
	print p1V
	print pAb
	bayesian.testingNB()

	email = emailClassfier()
	email.spamTest(bayesian)