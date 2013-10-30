# _*_ coding: utf-8 _*_
import numpy as np
import pylab as pl
from sklearn import svm, datasets

## 加载多维数据
def loadMultiDataSet(fileName):
	dataMat = []; labelMat = []
	fr = open(fileName)
	## 获得培训集
	dataMat = []; labelMat = []
	for line in fr.readlines():
		currLine = line.strip().split('\t')
		lineArr =[]
		for i in range(2):
			lineArr.append(float(currLine[i]))
		dataMat.append(lineArr)
		labelMat.append(float(currLine[2]))
	return dataMat,labelMat

## 使用SCIKIT工具实现SVM
if __name__ == "__main__":
	## 加载数据
	dataArr, labelArr = loadMultiDataSet('data/svm/testSet.txt')
	X = dataArr  # we only take the first two features. We could
	                      # avoid this ugly slicing by using a two-dim dataset
	Y = labelArr
	X = np.asarray(X)
	Y = np.asarray(Y)
	h = .02  # step size in the mesh

	# we create an instance of SVM and fit out data. We do not scale our
	# data since we want to plot the support vectors
	C = 1.0  # SVM regularization parameter
	svc = svm.SVC(kernel='linear', C=C).fit(X, Y)
	rbf_svc = svm.SVC(kernel='rbf', gamma=0.7, C=C).fit(X, Y)
	poly_svc = svm.SVC(kernel='poly', degree=3, C=C).fit(X, Y)
	lin_svc = svm.LinearSVC(C=C).fit(X, Y)

	## 预测过程
	print svc.predict([[7.139979, -2.329896]])

	# create a mesh to plot in
	x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
	y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
	xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
						np.arange(y_min, y_max, h))

	# title for the plots
	titles = ['SVC with linear kernel',
				'SVC with RBF kernel',
				'SVC with polynomial (degree 3) kernel',
				'LinearSVC (linear kernel)']


	for i, clf in enumerate((svc, rbf_svc, poly_svc, lin_svc)):
		# Plot the decision boundary. For that, we will assign a color to each
		# point in the mesh [x_min, m_max]x[y_min, y_max].
		pl.subplot(2, 2, i + 1)
		Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

		# Put the result into a color plot
		Z = Z.reshape(xx.shape)
		pl.contourf(xx, yy, Z, cmap=pl.cm.Paired)
		pl.axis('off')

		# Plot also the training points
		pl.scatter(X[:, 0], X[:, 1], c=Y, cmap=pl.cm.Paired)

		pl.title(titles[i])

	pl.show()