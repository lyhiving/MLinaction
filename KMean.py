

class Kmeans:

	def loadDataSet(self,fileName):      #general function to parse tab -delimited floats
	    dataMat = []                #assume last column is target value
	    fr = open(fileName)
	    for line in fr.readlines():
	        curLine = line.strip().split('\t')
	        fltLine = map(float,curLine) #map all elements to float()
	        dataMat.append(fltLine)
	    return dataMat

	def kmeans(self):
		dataMat = self.loadDataSet('data/kmean/testSet.txt')
		from sklearn.cluster import KMeans
		kmeans = KMeans(init='k-means++', n_clusters= 5, n_init=10)
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
		print Z
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
	kmeans.kmeans()