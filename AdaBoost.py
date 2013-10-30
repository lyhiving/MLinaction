# _*_ coding: utf-8 _*_

from numpy import *
class AdaBoost:

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

	def stumpClassify(self,dataMatrix,dimen,threshVal,threshIneq):#just classify the data
		retArray = ones((shape(dataMatrix)[0],1))
		if threshIneq == 'lt':
			retArray[dataMatrix[:,dimen] <= threshVal] = -1.0
		else:
			retArray[dataMatrix[:,dimen] > threshVal] = -1.0
		return retArray


	def buildStump(self, dataArr,classLabels,D):
		dataMatrix = mat(dataArr); labelMat = mat(classLabels).T
		m,n = shape(dataMatrix)
		numSteps = 10.0; bestStump = {}; bestClasEst = mat(zeros((m,1)))
		minError = inf #init error sum, to +infinity
		for i in range(n):#loop over all dimensions
			rangeMin = dataMatrix[:,i].min(); rangeMax = dataMatrix[:,i].max();
			stepSize = (rangeMax-rangeMin)/numSteps
			for j in range(-1,int(numSteps)+1):#loop over all range in current dimension
				for inequal in ['lt', 'gt']: #go over less than and greater than
					threshVal = (rangeMin + float(j) * stepSize)
					predictedVals = self.stumpClassify(dataMatrix,i,threshVal,inequal)#call stump classify with i, j, lessThan
					errArr = mat(ones((m,1)))
					errArr[predictedVals == labelMat] = 0
					weightedError = D.T*errArr  #calc total error multiplied by D
					#print "split: dim %d, thresh %.2f, thresh ineqal: %s, the weighted error is %.3f" % (i, threshVal, inequal, weightedError)
					if weightedError < minError:
						minError = weightedError
						bestClasEst = predictedVals.copy()
						bestStump['dim'] = i
						bestStump['thresh'] = threshVal
						bestStump['ineq'] = inequal
		return bestStump,minError,bestClasEst


	def adaBoostTrainDS(self, dataArr, classLabels, numIt=40):
		"""
		:param dataArr:
		:param classLabels:
		:param numIt:
		:return:
		"""
		weakClassArr = []
		m = shape(dataArr)[0]
		D = mat(ones((m,1))/m)   #init D to all equal
		aggClassEst = mat(zeros((m,1)))
		for i in range(numIt):
			bestStump,error,classEst = self.buildStump(dataArr,classLabels,D)#build Stump
			#print "D:",D.T
			alpha = float(0.5*log((1.0-error)/max(error,1e-16)))#calc alpha, throw in max(error,eps) to account for error=0
			bestStump['alpha'] = alpha
			weakClassArr.append(bestStump)                  #store Stump Params in Array
			#print "classEst: ",classEst.T
			expon = multiply(-1*alpha*mat(classLabels).T,classEst) #exponent for D calc, getting messy
			D = multiply(D,exp(expon))                              #Calc New D for next iteration
			D = D/D.sum()
			#calc training error of all classifiers, if this is 0 quit for loop early (use break)
			aggClassEst += alpha*classEst
			#print "aggClassEst: ",aggClassEst.T
			aggErrors = multiply(sign(aggClassEst) != mat(classLabels).T,ones((m,1)))
			errorRate = aggErrors.sum()/m
			print "total error: ",errorRate
			if errorRate == 0.0: break

		return weakClassArr, aggClassEst

	def adaClassify(self, datToClass,classifierArr):
		dataMatrix = mat(datToClass)#do stuff similar to last aggClassEst in adaBoostTrainDS
		m = shape(dataMatrix)[0]
		aggClassEst = mat(zeros((m,1)))
		for i in range(len(classifierArr)):
			classEst = self.stumpClassify(dataMatrix,classifierArr[i]['dim'],classifierArr[i]['thresh'],classifierArr[i]['ineq'])
			aggClassEst += classifierArr[i]['alpha']*classEst
			print aggClassEst
		return sign(aggClassEst)

	def plotROC(self, predStrengths, classLabels):
		import matplotlib.pyplot as plt
		cur = (1.0,1.0) #cursor
		ySum = 0.0 #variable to calculate AUC
		numPosClas = sum(array(classLabels)==1.0)
		yStep = 1/float(numPosClas); xStep = 1/float(len(classLabels)-numPosClas)
		sortedIndicies = predStrengths.argsort()#get sorted index, it's reverse
		fig = plt.figure()
		fig.clf()
		ax = plt.subplot(111)
		#loop through all the values, drawing a line segment at each point
		for index in sortedIndicies.tolist()[0]:
			if classLabels[index] == 1.0:
				delX = 0; delY = yStep;
			else:
				delX = xStep; delY = 0;
				ySum += cur[1]
			#draw line from cur to (cur[0]-delX,cur[1]-delY)
			ax.plot([cur[0],cur[0]-delX],[cur[1],cur[1]-delY], c='b')
			cur = (cur[0]-delX,cur[1]-delY)
		ax.plot([0,1],[0,1],'b--')
		plt.xlabel('False positive rate'); plt.ylabel('True positive rate')
		plt.title('ROC curve for AdaBoost horse colic detection system')
		ax.axis([0,1,0,1])
		plt.show()
		print "the Area Under the Curve is: ",ySum*xStep

	def adaboostTest(self):
		dataArr, labels = self.loadSimpData()

		classifierArr, aggClassEst= self.adaBoostTrainDS(dataArr,labels,30)
		# 对[0,0]的分类
		print self.adaClassify([0, 0], classifierArr)

		## 训练数据对数据进行分类
		dataArr, labels = self.loadDataSet("data/adaboost/horseColicTraining2.txt")
		classifierArr, aggClassEst = self.adaBoostTrainDS(dataArr,labels,50)
		testdataArr, testlabels = self.loadDataSet("data/adaboost/horseColicTest2.txt")
		prediction10 = self.adaClassify(testdataArr,classifierArr)
		errArr = mat(ones((67,1)))
		print errArr[prediction10 != mat(testlabels).T].sum()/67
		## 展示ROC曲线
		self.plotROC(aggClassEst.T, labels)

	def scikitAdaboost(self):
		import pylab as pl
		import numpy as np

		from sklearn.ensemble import AdaBoostClassifier
		from sklearn.tree import DecisionTreeClassifier
		from sklearn.datasets import make_gaussian_quantiles
		X, y = adaboost.loadDataSet("data/svm/testSet.txt")
		X = np.asarray(X)
		y = np.asarray(y)
		# Create and fit an AdaBoosted decision tree
		bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1),
								algorithm="SAMME",
								n_estimators=200)

		bdt.fit(X, y)

		plot_colors = "br"
		plot_step = 0.02
		class_names = "AB"
		pl.figure(figsize=(10, 5))
		h = .02  # step size in the mesh
		# Plot the decision boundaries
		x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
		y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
		xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
						np.arange(y_min, y_max, h))

		# title for the plots
		titles = ['SVC with linear kernel',
				'SVC with RBF kernel',
				'SVC with polynomial (degree 3) kernel',
				'LinearSVC (linear kernel)']

		Z = bdt.predict(np.c_[xx.ravel(), yy.ravel()])
		Z = Z.reshape(xx.shape)
		cs = pl.contourf(xx, yy, Z, cmap=pl.cm.Paired)
		pl.axis("tight")
		# Plot the training points
		plot_colors = "br"
		plot_step = 0.02
		class_names = "AB"



		pl.legend(loc='upper right')
		pl.xlabel("Decision Boundary")
		pl.show()

## AdaBoost是采用Boosting方法来将弱分类器（比随机比例50%好不了多少）
## 通过组合的方式来构成强分类器，提升分类水平
if __name__ == "__main__":
	adaboost = AdaBoost()

	#adaboost.adaboostTest()

	adaboost.scikitAdaboost()