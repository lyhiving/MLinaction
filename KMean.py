# _*_ coding: utf-8 _*_
from numpy import *
import matplotlib
import matplotlib.pyplot as plt


class Kmeans:
	def loadDataSet(self, fileName):      #general function to parse tab -delimited floats
		dataMat = []                #assume last column is target value
		fr = open(fileName)
		for line in fr.readlines():
			curLine = line.strip().split('\t')
			fltLine = map(float, curLine) #map all elements to float()
			dataMat.append(fltLine)
		return dataMat

	## 欧几里得距离
	def distEclud(self, vecA, vecB):
		return sqrt(sum(power(vecA - vecB, 2))) #la.norm(vecA-vecB)

	## 球面距离
	def distSLC(self, vecA, vecB):#Spherical Law of Cosines
		a = sin(vecA[0, 1] * pi / 180) * sin(vecB[0, 1] * pi / 180)
		b = cos(vecA[0, 1] * pi / 180) * cos(vecB[0, 1] * pi / 180) * \
		    cos(pi * (vecB[0, 0] - vecA[0, 0]) / 180)
		return arccos(a + b) * 6371.0 #pi is imported with numpy

	## k为随机质心的数量
	def randCent(self, dataSet, k):
		n = shape(dataSet)[1]
		centroids = mat(zeros((k, n)))#create centroid mat
		dataSet = asarray(dataSet)
		for j in range(n):#create random cluster centers, within bounds of each dimension
			minJ = min(dataSet[:, j])
			rangeJ = float(max(dataSet[:, j]) - minJ)
			centroids[:, j] = mat(minJ + rangeJ * random.rand(k, 1))
		return centroids

	##-------------------------------------------------------------------------
	## 一般KMeans方法
	def kMeans(self, dataSet, k, distMeas=distEclud, createCent=randCent):
		m = shape(dataSet)[0]
		clusterAssment = mat(zeros((m, 2)))#create mat to assign data points
		#to a centroid, also holds SE of each point
		centroids = createCent(dataSet, k)
		clusterChanged = True
		while clusterChanged:
			clusterChanged = False
			for i in range(m):#for each data point assign it to the closest centroid
				minDist = inf;
				minIndex = -1
				for j in range(k):
					distJI = distMeas(centroids[j, :], dataSet[i, :])
					if distJI < minDist:
						minDist = distJI;
						minIndex = j
				if clusterAssment[i, 0] != minIndex: clusterChanged = True
				clusterAssment[i, :] = minIndex, minDist ** 2
			print centroids
			for cent in range(k):#recalculate centroids
				ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A == cent)[0]]#get all the point in this cluster
				centroids[cent, :] = mean(ptsInClust, axis=0) #assign centroid to mean
		return centroids, clusterAssment

	# 改进后的Kmeans方法，即二分K均值法
	def biKmeans(self, dataSet, k, distMeas=distEclud, createCent=randCent):
		m = shape(dataSet)[0]
		clusterAssment = mat(zeros((m, 2)))
		centroid0 = mean(dataSet, axis=0).tolist()[0]
		centList = [centroid0] #create a list with one centroid
		for j in range(m):#calc initial Error
			clusterAssment[j, 1] = distMeas(mat(centroid0), dataSet[j, :]) ** 2
		while (len(centList) < k):
			lowestSSE = inf
			for i in range(len(centList)):
				ptsInCurrCluster = dataSet[nonzero(clusterAssment[:, 0].A == i)[0],
				                   :]#get the data points currently in cluster i
				centroidMat, splitClustAss = self.kMeans(ptsInCurrCluster, 2, distMeas, createCent)
				sseSplit = sum(splitClustAss[:, 1])#compare the SSE to the currrent minimum
				sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:, 0].A != i)[0], 1])
				print "sseSplit, and notSplit: ", sseSplit, sseNotSplit
				if (sseSplit + sseNotSplit) < lowestSSE:
					bestCentToSplit = i
					bestNewCents = centroidMat
					bestClustAss = splitClustAss.copy()
					lowestSSE = sseSplit + sseNotSplit
			bestClustAss[nonzero(bestClustAss[:, 0].A == 1)[0], 0] = len(centList) #change 1 to 3,4, or whatever
			bestClustAss[nonzero(bestClustAss[:, 0].A == 0)[0], 0] = bestCentToSplit
			print 'the bestCentToSplit is: ', bestCentToSplit
			print 'the len of bestClustAss is: ', len(bestClustAss)
			centList[bestCentToSplit] = bestNewCents[0, :].tolist()[0]#replace a centroid with two best centroids
			centList.append(bestNewCents[1, :].tolist()[0])
			clusterAssment[nonzero(clusterAssment[:, 0].A == bestCentToSplit)[0],
			:] = bestClustAss#reassign new clusters, and SSE
		return mat(centList), clusterAssment

	## 计算KMeans聚类的准备工作
	def kMeansTest(self):
		dataMat = self.loadDataSet('data/kmean/testSet.txt')
		## 将List转换为ndarray
		dataMat = asarray(dataMat)
		# 计算两个质心点坐标
		print self.randCent(dataMat, 2)
		print self.distEclud(dataMat[0], dataMat[1])

	##以下为测试方法
	## 一般KMEANS聚类
	def KMeansTest2(self):
		dataMat = mat(self.loadDataSet('data/kmean/testSet.txt'))
		myCentroids, clustAssing = self.kMeans(dataMat, 4, self.distEclud, self.randCent)
		print myCentroids
		print clustAssing

	## 二分KMENAS聚类
	def KMeansTest3(self):
		dataMat = mat(self.loadDataSet('data/kmean/testSet2.txt'))
		centList, newAssment = self.biKmeans(dataMat, 3, self.distEclud, self.randCent)
		print centList


	def ClusterClubsTest(self, numClust=5):
		datList = []
		for line in open('data/kmean/places.txt').readlines():
			lineArr = line.split('\t')
			datList.append([float(lineArr[4]), float(lineArr[3])])
		datMat = mat(datList)
		myCentroids, clustAssing = self.biKmeans(datMat, numClust, self.distSLC, self.randCent)
		fig = plt.figure()
		rect = [0.1, 0.1, 0.8, 0.8]
		scatterMarkers = ['s', 'o', '^', '8', 'p', \
		                  'd', 'v', 'h', '>', '<']
		axprops = dict(xticks=[], yticks=[])
		ax0 = fig.add_axes(rect, label='ax0', **axprops)
		imgP = plt.imread('data/kmean/Portland.png')
		ax0.imshow(imgP)
		ax1 = fig.add_axes(rect, label='ax1', frameon=False)
		for i in range(numClust):
			ptsInCurrCluster = datMat[nonzero(clustAssing[:, 0].A == i)[0], :]
			markerStyle = scatterMarkers[i % len(scatterMarkers)]
			ax1.scatter(ptsInCurrCluster[:, 0].flatten().A[0], ptsInCurrCluster[:, 1].flatten().A[0],
			            marker=markerStyle, s=90)
		ax1.scatter(myCentroids[:, 0].flatten().A[0], myCentroids[:, 1].flatten().A[0], marker='+', s=300)
		plt.show()

	def ScikitKMeansTest(self):
		dataMat = self.loadDataSet('data/kmean/testSet.txt')
		from sklearn.cluster import KMeans

		kmeans = KMeans(init='k-means++', n_clusters=5, n_init=10)
		kmeans.fit(dataMat)

		import numpy as np
		import pylab as pl

		h = .02     # point in the mesh [x_min, m_max]x[y_min, y_max].
		reduced_data = np.array(dataMat)
		# Plot the decision boundary. For that, we will assign a color to each
		x_min, x_max = reduced_data[:, 0].min() + 1, reduced_data[:, 0].max() - 1
		y_min, y_max = reduced_data[:, 1].min() + 1, reduced_data[:, 1].max() - 1
		xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

		# Obtain labels for each point in mesh. Use last trained model.
		Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
		# Put the result into a color plot
		Z = Z.reshape(xx.shape)

		pl.imshow(Z, interpolation='nearest',
		          extent=(xx.min(), xx.max(), yy.min(), yy.max()),
		          cmap=pl.cm.Paired,
		          aspect='auto', origin='lower')

		pl.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
		# Plot the centroids as a white X
		centroids = kmeans.cluster_centers_
		print centroids
		pl.scatter(centroids[:, 0], centroids[:, 1],
		           marker='x', s=169, linewidths=3,
		           color='w', zorder=10)
		pl.xlim(x_min, x_max)
		pl.ylim(y_min, y_max)

		pl.show()


if __name__ == "__main__":
	kmeans = Kmeans()
	kmeans.ClusterClubsTest(6)