# _*_ coding: utf-8 _*_
from os import listdir
from sklearn.neighbors import KNeighborsClassifier

from hmgis.Classifier.KNN import *


class KNNTest:
	def createDataSet(self):
		group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
		labels = ['A', 'A', 'B', 'B']
		return group, labels

	def loadDataSetFromFile(self, filename):
		fr = open(filename)
		numberOfLines = len(fr.readlines())         #get the number of lines in the file
		returnMat = zeros((numberOfLines, 3))        #prepare matrix to return
		classLabelVector = []                       #prepare labels return
		fr = open(filename)
		index = 0
		for line in fr.readlines():
			line = line.strip()
			listFromLine = line.split('\t')
			returnMat[index, :] = listFromLine[0:3]
			classLabelVector.append(int(listFromLine[-1]))
			index += 1
		return returnMat, classLabelVector

	def knnTest(self):
		knn = KNNDemo()
		group, labels = self.createDataSet()
		print "原生分类器,[0,1]的分类结果为", knn.classify0([0, 1], group, labels, 3)
		## scikit learn代码
		neigh = KNeighborsClassifier(n_neighbors=3)
		neigh.fit(group, labels)
		print "SciKit的KNN分类器,[0,1]的分类结果为", neigh.predict([[0, 1]])

	def show2DPoint(self, filename):
		datingDataMat, datingLabels = self.loadDataSetFromFile(filename)
		knn = KNNDemo()
		normMat, ranges, minVals = knn.autoNorm(datingDataMat)
		knn.show2D(normMat, datingLabels)

	def show3DPoint(self, filename):
		datingDataMat, datingLabels = self.loadDataSetFromFile(filename)
		knn = KNNDemo()
		normMat, ranges, minVals = knn.autoNorm(datingDataMat)
		knn.show3D(normMat, datingLabels)

	## KNN分类
	def knnTest2(self, infile):
		hoRatio = 0.80      #hold out 10%
		datingDataMat, datingLabels = self.loadDataSetFromFile(infile)       #load data setfrom file
		knn = KNNDemo()
		normMat, ranges, minVals = knn.autoNorm(datingDataMat)
		m = normMat.shape[0]
		numTestVecs = int(m * hoRatio)
		errorCount = 0.0
		for i in range(numTestVecs):
			classifierResult = knn.classify0(normMat[i, :], normMat[numTestVecs:m, :], datingLabels[numTestVecs:m], 3)
			print "分类结果为: %d, 实际结果为: %d" % (classifierResult, datingLabels[i])
			if (classifierResult != datingLabels[i]): errorCount += 1.0
		print "总错误率为: %f" % (errorCount / float(numTestVecs))
		print errorCount, "个错误"

	## Scikit的KNN分类
	def knnTestScikit(self, infile):
		hoRatio = 0.80      #hold out 10%
		datingDataMat, datingLabels = self.loadDataSetFromFile(infile)       #load data setfrom file
		knn = KNNDemo()
		normMat, ranges, minVals = knn.autoNorm(datingDataMat)
		m = normMat.shape[0]
		numTestVecs = int(m * hoRatio)
		errorCount = 0.0
		## SCIKIT的KNN分类器
		neigh = KNeighborsClassifier(n_neighbors=3)
		## 训练集
		neigh.fit(normMat[numTestVecs:m, :], datingLabels[numTestVecs:m])
		for i in range(numTestVecs):
			## 分类过程
			classifierResult = neigh.predict(normMat[i, :])
			print "分类结果为: %d, 实际结果为: %d" % (classifierResult, datingLabels[i])
			if (classifierResult != datingLabels[i]): errorCount += 1.0
		print "SCIKIT分类总错误率为: %f" % (errorCount / float(numTestVecs))
		print errorCount

	def img2vector(self, filename):
		returnVect = zeros((1, 1024))
		fr = open(filename)
		for i in range(32):
			lineStr = fr.readline()
			for j in range(32):
				returnVect[0, 32 * i + j] = int(lineStr[j])
		return returnVect

	def handwritingClassTest(self):
		"""


		"""
		hwLabels = []
		trainingFileList = listdir('data/knn/trainingDigits')           #load the training set
		m = len(trainingFileList)
		trainingMat = zeros((m, 1024))
		for i in range(m):
			fileNameStr = trainingFileList[i]
			fileStr = fileNameStr.split('.')[0]     #take off .txt
			classNumStr = int(fileStr.split('_')[0])
			hwLabels.append(classNumStr)
			trainingMat[i, :] = self.img2vector('data/knn/trainingDigits/%s' % fileNameStr)

		neigh = KNeighborsClassifier(n_neighbors=3)
		neigh.fit(trainingMat, hwLabels)

		testFileList = listdir('data/knn/testDigits')        #iterate through the test set
		errorCount = 0.0
		mTest = len(testFileList)
		for i in range(mTest):
			fileNameStr = testFileList[i]
			fileStr = fileNameStr.split('.')[0]     #take off .txt
			classNumStr = int(fileStr.split('_')[0])
			vectorUnderTest = self.img2vector('data/knn/testDigits/%s' % fileNameStr)
			classifierResult = neigh.predict(vectorUnderTest)
			print "分类器结果: %d, 实际结果: %d" % (classifierResult, classNumStr)
			if (classifierResult != classNumStr): errorCount += 1.0
		print "\n总错误: %d" % errorCount
		print "\n错误率: %f" % (errorCount / float(mTest))