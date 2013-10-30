# _*_ coding: utf-8 _*_
from numpy import *
import sys

## logistic函数是要寻找一种最佳拟合方法，这一点与线性方程非常类似
## 但它使用了梯度下降法来最快速地寻找数据
## 这使得它对多参数的二分分类比较适合
class logistic:

	def loadDataSet(self):
		dataMat = []; labelMat = []
		fr = open('data/logistic/testSet.txt')
		for line in fr.readlines():
			lineArr = line.strip().split()
			dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
			labelMat.append(int(lineArr[2]))
		return dataMat,labelMat

	def sigmoid(self, inX):
		return 1.0/(1+exp(-inX))

	## 梯度下降法求最佳拟合参数
	## 拟合了500次
	def gradAscent(self, dataMatIn, classLabels):
		dataMatrix = mat(dataMatIn)             #convert to NumPy matrix
		labelMat = mat(classLabels).transpose() #convert to NumPy matrix
		m,n = shape(dataMatrix)
		alpha = 0.001
		maxCycles = 500
		weights = ones((n,1))
		for k in range(maxCycles):              #heavy on matrix operations
			h = self.sigmoid(dataMatrix*weights)     #matrix mult
			error = (labelMat - h)              #vector subtraction
			weights = weights + alpha * dataMatrix.transpose()* error   #matrix mult
		## 将matrix转化为ndarry
		weights = asarray(weights).reshape(-1)
		return weights

	## 随机梯度
	## 拟合200次
	def stocGradAscent0(self, dataMatrix, classLabels):
		m,n = shape(dataMatrix)
		alpha = 0.01
		weights = ones(n)   #initialize to all ones
		for i in range(m):
			h = self.sigmoid(sum(dataMatrix[i]*weights))
			error = classLabels[i] - h
			weights = weights + alpha * error * dataMatrix[i]
		return weights

	## 改进随机梯度
	def stocGradAscent1(self, dataMatrix, classLabels, numIter=150):
		m,n = shape(dataMatrix)
		weights = ones(n)   #initialize to all ones
		for j in range(numIter):
			dataIndex = range(m)
			for i in range(m):
				alpha = 4/(1.0+j+i)+0.0001    #apha decreases with iteration, does not
				randIndex = int(random.uniform(0,len(dataIndex)))#go to 0 because of the constant
				h = self.sigmoid(sum(dataMatrix[randIndex]*weights))
				error = classLabels[randIndex] - h
				weights = weights + alpha * error * dataMatrix[randIndex]
				del(dataIndex[randIndex])
		return weights

	def logiTest(self):
		dataArr, labelMat = self.loadDataSet()
		return self.gradAscent(dataArr, labelMat)


	def plotBestfit(self, weights):
		import numpy as np
		import matplotlib.pyplot as plt
		dataMat,labelMat = self.loadDataSet()

		dataArr = array(dataMat)
		n = shape(dataArr)[0]
		xcord1 = []; ycord1 = []
		xcord2 = []; ycord2 = []
		for i in range(n):
			if int(labelMat[i])== 1:
				xcord1.append(dataArr[i,1]); ycord1.append(dataArr[i,2])
			else:
				xcord2.append(dataArr[i,1]); ycord2.append(dataArr[i,2])
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
		ax.scatter(xcord2, ycord2, s=30, c='green')
		x = np.arange(-3.0, 3.0, 0.1)
		a = float(weights[0])
		b = float(weights[1])
		c = float(weights[2])
		y = ( -a - b * x) / c
		ax.plot(x, y)
		plt.xlabel('X1')
		plt.ylabel('X2')
		plt.show()

	## 计算分类
	def classifyVector(self, inX, weights):
		prob = self.sigmoid(sum(inX*weights))
		if prob > 0.5: return 1.0
		else: return 0.0

	def colicTest(self):
		frTrain = open('data/logistic/horseColicTraining.txt')
		frTest = open('data/logistic/horseColicTest.txt')
		## 获得培训集
		trainingSet = []; trainingLabels = []
		for line in frTrain.readlines():
			currLine = line.strip().split('\t')
			lineArr =[]
			for i in range(21):
				lineArr.append(float(currLine[i]))
			trainingSet.append(lineArr)
			trainingLabels.append(float(currLine[21]))
		## 对培训集进行训练
		trainWeights = self.stocGradAscent1(array(trainingSet), trainingLabels, 1000)
		errorCount = 0; numTestVec = 0.0
		## 读取测试集
		for line in frTest.readlines():
			numTestVec += 1.0
			currLine = line.strip().split('\t')
			lineArr =[]
			for i in range(21):
				lineArr.append(float(currLine[i]))
			## 测试函数
			if int(self.classifyVector(array(lineArr), trainWeights))!= int(currLine[21]):
				errorCount += 1
		errorRate = (float(errorCount)/numTestVec)
		print "the error rate of this test is: %f" % errorRate
		return errorRate

	def multiTest(self):
		numTests = 10; errorSum=0.0
		for k in range(numTests):
			errorSum += self.colicTest()
		print "after %d iterations the average error rate is: %f" % (numTests, errorSum/float(numTests))

if __name__ == "__main__":
	logic = logistic()
	dataArr, labelMat = logic.loadDataSet()
	weights = logic.gradAscent(dataArr, labelMat)
	#logic.plotBestfit(weights)

	weights = logic.stocGradAscent0(array(dataArr), labelMat)
	#logic.plotBestfit(weights)

	weights = logic.stocGradAscent1(array(dataArr), labelMat, 200)
	#logic.plotBestfit(weights)

	##
	logic.multiTest()