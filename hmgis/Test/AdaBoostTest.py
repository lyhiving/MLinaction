# _*_ coding: utf-8 _*_
from numpy import *
from hmgis.Classifier.AdaBoost import *
class AdaBoostTest:
	def loadSimpData(self):
		datMat = matrix([[ 1. ,  2.1],
			[ 2. ,  1.1],
			[ 1.3,  1. ],
			[ 1. ,  1. ],
			[ 2. ,  1. ]])
		classLabels = [1.0, 1.0, -1.0, -1.0, 1.0]
		return datMat,classLabels

	## 修改后的数据加载器，能自动从数据中获得一个表
	def loadDataSet(self,fileName):      #general function to parse tab -delimited floats
		numFeat = len(open(fileName).readline().split('\t')) #get number of fields
		dataMat = []; labelMat = []
		fr = open(fileName)
		for line in fr.readlines():
			lineArr =[]
			curLine = line.strip().split('\t')
			for i in range(numFeat-1):
				lineArr.append(float(curLine[i]))
			dataMat.append(lineArr)
			labelMat.append(float(curLine[-1]))
		return dataMat,labelMat

	def adaboostTest(self):
		dataArr, labels = self.loadSimpData()

		ada = AdaBoost()
		classifierArr, aggClassEst= ada.adaBoostTrainDS(dataArr,labels,30)
		# 对[0,0]的分类
		print ada.adaClassify([0, 0], classifierArr)

		## 训练数据对数据进行分类
		dataArr, labels = self.loadDataSet("data/adaboost/horseColicTraining2.txt")
		## 培训数据
		classifierArr, aggClassEst = ada.adaBoostTrainDS(dataArr,labels,50)
		testdataArr, testlabels = self.loadDataSet("data/adaboost/horseColicTest2.txt")
		## 数据分类
		prediction10 = ada.adaClassify(testdataArr,classifierArr)
		errArr = mat(ones((67,1)))
		print errArr[prediction10 != mat(testlabels).T].sum()/67
		## 展示ROC曲线
		ada.plotROC(aggClassEst.T, labels)

	def scikitAdaboost(self):
		import pylab as pl
		import numpy as np

		from sklearn.ensemble import AdaBoostClassifier
		from sklearn.tree import DecisionTreeClassifier
		from sklearn.datasets import make_gaussian_quantiles
		X, y = self.loadDataSet("data/adaboost/horseColicTraining2.txt")
		X = np.asarray(X)
		y = np.asarray(y)
		# Create and fit an AdaBoosted decision tree
		bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1),
								algorithm="SAMME",
								n_estimators=200)
		bdt.fit(X, y)
		testdataArr, testlabels = self.loadDataSet("data/adaboost/horseColicTest2.txt")
		Z = bdt.predict(np.asarray(testdataArr))
		print Z
		print mat(testlabels)
