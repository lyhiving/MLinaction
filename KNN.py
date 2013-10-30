#coding:utf-8
#采用原生代码和scikit Learn库共同测试

from numpy import *
import operator
from os import listdir
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D

class KNNDemo:

	## 创建KNN第一个测试数据集
	def createDataSet(self):
		group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
		labels = ['A','A','B','B']
		return group, labels

	## inX 需要分类的数据
	## dataSet 训练集
	## labels 训练集分类
	## KNN选择的数量
	def classify0(self, inX, dataSet, labels, k):
		dataSetSize = dataSet.shape[0]
		diffMat = tile(inX, (dataSetSize,1)) - dataSet
		sqDiffMat = diffMat**2
		sqDistances = sqDiffMat.sum(axis=1)
		distances = sqDistances**0.5
		sortedDistIndicies = distances.argsort()
		classCount={}
		for i in range(k):
			voteIlabel = labels[sortedDistIndicies[i]]
			classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
		sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
		return sortedClassCount[0][0]

	## KNN最简单的代码
	def knnTest(self):
		## 原生代码
		group, labels = self.createDataSet()
		print self.classify0([0,1], group, labels, 3)
		## scikit learn代码
		neigh = KNeighborsClassifier(n_neighbors=3)
		neigh.fit(group, labels)
		print(neigh.predict([[0, 1]]))

	##------------------------------------------------------------------------------

	## 从文件中加载数据
	def file2matrix(self, filename):
		fr = open(filename)
		numberOfLines = len(fr.readlines())         #get the number of lines in the file
		returnMat = zeros((numberOfLines,3))        #prepare matrix to return
		classLabelVector = []                       #prepare labels return
		fr = open(filename)
		index = 0
		for line in fr.readlines():
			line = line.strip()
			listFromLine = line.split('\t')
			returnMat[index,:] = listFromLine[0:3]
			classLabelVector.append(int(listFromLine[-1]))
			index += 1
		return returnMat,classLabelVector

	## 将点数据进行2维可视化
	def show2DTest(self, datingDataMat, datingLabels):
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.scatter(datingDataMat[:,1],datingDataMat[:,2], 15.0*array(datingLabels), 15.0*array(datingLabels))
		plt.show()

	## 将点数据进行三维可视化，即最多只能显示3个属性
	def show3DTest(self, datingDataMat, datingLabels):
		fig = pl.figure(1, figsize=(8, 6))
		ax = Axes3D(fig, elev=-150, azim=110)
		ax.scatter(datingDataMat[:, 1], datingDataMat[:, 2], datingDataMat[:, 0], c=datingLabels)
		ax.set_title("Point 3 Properties Visualization")
		ax.set_xlabel("1st")
		ax.set_ylabel("2nd")
		ax.set_zlabel("3rd")
		pl.show()

	##------------------------------------------------------------------------------

	## 归一化处理函数，以防止参数之间的值差距过大
	## 使得所有制均在-1至1之间
	def autoNorm(self, dataSet):
		minVals = dataSet.min(0)
		maxVals = dataSet.max(0)
		ranges = maxVals - minVals
		normDataSet = zeros(shape(dataSet))
		m = dataSet.shape[0]
		normDataSet = dataSet - tile(minVals, (m,1))
		normDataSet = normDataSet/tile(ranges, (m,1))   #element wise divide
		return normDataSet, ranges, minVals

	## KNN分类
	def datingClassTest(self):
		hoRatio = 0.80      #hold out 10%
		datingDataMat,datingLabels = self.file2matrix('data/knn/datingTestSet2.txt')       #load data setfrom file
		normMat, ranges, minVals = self.autoNorm(datingDataMat)
		m = normMat.shape[0]
		numTestVecs = int(m*hoRatio)
		errorCount = 0.0
		for i in range(numTestVecs):
			classifierResult = self.classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
			print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i])
			if (classifierResult != datingLabels[i]): errorCount += 1.0
		print "the total error rate is: %f" % (errorCount/float(numTestVecs))
		print errorCount

	## Scikit的KNN分类
	def datingClassTest2(self):
		hoRatio = 0.80      #hold out 10%
		datingDataMat,datingLabels = self.file2matrix('data/knn/datingTestSet2.txt')       #load data setfrom file
		normMat, ranges, minVals = self.autoNorm(datingDataMat)
		m = normMat.shape[0]
		numTestVecs = int(m*hoRatio)
		errorCount = 0.0
		## SCIKIT的KNN分类器
		neigh = KNeighborsClassifier(n_neighbors=3)
		## 训练集
		neigh.fit(normMat[numTestVecs:m,:],datingLabels[numTestVecs:m])
		for i in range(numTestVecs):
			## 分类过程
			classifierResult = neigh.predict(normMat[i,:])
			print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i])
			if (classifierResult != datingLabels[i]): errorCount += 1.0
		print "the total error rate is: %f" % (errorCount/float(numTestVecs))
		print errorCount

	##------------------------------------------------------------------------------
	## 以下例子是将图像进行分类
	def img2vector(self, filename):
		returnVect = zeros((1,1024))
		fr = open(filename)
		for i in range(32):
			lineStr = fr.readline()
			for j in range(32):
				returnVect[0,32*i+j] = int(lineStr[j])
		return returnVect

	def handwritingClassTest(self):
		hwLabels = []
		trainingFileList = listdir('data/knn/trainingDigits')           #load the training set
		m = len(trainingFileList)
		trainingMat = zeros((m,1024))
		for i in range(m):
			fileNameStr = trainingFileList[i]
			fileStr = fileNameStr.split('.')[0]     #take off .txt
			classNumStr = int(fileStr.split('_')[0])
			hwLabels.append(classNumStr)
			trainingMat[i,:] = self.img2vector('data/knn/trainingDigits/%s' % fileNameStr)

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
		print "\n错误率: %f" % (errorCount/float(mTest))


if __name__ == "__main__":
	knn = KNNDemo()
	## 加载数据
	datingDataMat, datingLabels = knn.file2matrix('data/knn/datingTestSet2.txt')
	#knn.show2DTest(datingDataMat, datingLabels)
	## 将数据进行归一化
	normMat, ranges, minVals = knn.autoNorm(datingDataMat)
	## 数据可视化
	#knn.show3DTest(normMat, datingLabels)
	knn.datingClassTest()
	knn.datingClassTest2()
	knn.handwritingClassTest()
