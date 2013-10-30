# _*_ coding: utf-8 _*_

from numpy import *

class Regression:
	def loadDataSet(self, fileName):      #general function to parse tab -delimited floats
	    numFeat = len(open(fileName).readline().split('\t')) - 1 #get number of fields
	    dataMat = []; labelMat = []
	    fr = open(fileName)
	    for line in fr.readlines():
	        lineArr =[]
	        curLine = line.strip().split('\t')
	        for i in range(numFeat):
	            lineArr.append(float(curLine[i]))
	        dataMat.append(lineArr)
	        labelMat.append(float(curLine[-1]))
	    return dataMat,labelMat

	def standRegres(self, xArr,yArr):
	    xMat = mat(xArr); yMat = mat(yArr).T
	    xTx = xMat.T*xMat
	    if linalg.det(xTx) == 0.0:
	        print "This matrix is singular, cannot do inverse"
	        return
	    ws = xTx.I * (xMat.T*yMat)
	    return ws

	def lwlr(self, testPoint,xArr,yArr,k=1.0):
	    xMat = mat(xArr); yMat = mat(yArr).T
	    m = shape(xMat)[0]
	    weights = mat(eye((m)))
	    for j in range(m):                      #next 2 lines create weights matrix
	        diffMat = testPoint - xMat[j,:]     #
	        weights[j,j] = exp(diffMat*diffMat.T/(-2.0*k**2))
	    xTx = xMat.T * (weights * xMat)
	    if linalg.det(xTx) == 0.0:
	        print "This matrix is singular, cannot do inverse"
	        return
	    ws = xTx.I * (xMat.T * (weights * yMat))
	    #print ws
	    return testPoint * ws

	## 获得所有点的估值
	def lwlrTest(self, testArr,xArr,yArr,k=1.0):  #loops over all the data points and applies lwlr to each one
	    m = shape(testArr)[0]
	    yHat = zeros(m)
	    for i in range(m):
	        yHat[i] = self.lwlr(testArr[i],xArr,yArr,k)
	    return yHat

	def lwlrTestPlot(self, xArr,yArr,k=1.0):  #same thing as lwlrTest except it sorts X first
	    yHat = zeros(shape(yArr))       #easier for plotting
	    xCopy = mat(xArr)
	    xCopy.sort(0)
	    for i in range(shape(xArr)[0]):
	        yHat[i] = self.lwlr(xCopy[i],xArr,yArr,k)
	    return yHat,xCopy

	## 一元线性回归方程
	def simpleTest(self):
		xArr, yArr = self.loadDataSet('data/reg/ex0.txt')
		print xArr[0:2]
		ws = self.standRegres(xArr, yArr)
		print ws
		xMat = mat(xArr);yMat = mat(yArr)
		yHat = xMat * ws

		import matplotlib.pyplot as plt
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.scatter(xMat[:,1].flatten().A[0], yMat.T[:,0].flatten().A[0])
		xCopy = xMat.copy()
		xCopy.sort(0)
		yHat = xCopy*ws
		m = xCopy[:, 1]
		ax.plot(array(m), array(yHat))
		plt.show()

	def multiTest(self):
		xArr, yArr = self.loadDataSet('data/reg/ex0.txt')
		yHat = self.lwlrTest(xArr, xArr, yArr, 0.01)
		xMat = mat(xArr)
		strInd = xMat[:,1].argsort(0)
		xSort = xMat[strInd][:,0,:]

		import matplotlib.pyplot as plt
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.scatter(xMat[:,1].flatten().A[0], mat(yArr).T[:,0].flatten().A[0])
		ax.plot(array(xSort[:,1]), array(yHat[strInd]))
		plt.show()

	## 接下来的都用scikit的函数算了

	def ridgeRegression(self):
		xArr, yArr = self.loadDataSet('data/reg/abalone.txt')

		## 岭回归
		from sklearn import linear_model
		clf = linear_model.Ridge (alpha = .5)
		clf.fit (xArr, yArr)
		print clf.coef_
		print clf.intercept_
		## 预测过程
		print clf.predict([[1,	0.35,	0.265,	0.09,	0.2255,	0.0995,	0.0485,	0.07]])


		## CART决策树回归
		from sklearn.tree import DecisionTreeRegressor
		clf_2 = DecisionTreeRegressor(max_depth=5)
		clf_2.fit(xArr, yArr)
		print clf_2.predict([[1,	0.35,	0.265,	0.09,	0.2255,	0.0995,	0.0485,	0.07]])

## 本代码直接介绍了各种回归方法，可以详细参见scikit的相关代码
if __name__ == "__main__":
	reg  = Regression()
	#reg.simpleTest()
	#reg.multiTest()
	#
	#岭回归
	reg.ridgeRegression()