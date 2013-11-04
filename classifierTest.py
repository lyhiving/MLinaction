# _*_ coding: utf-8 _*_
#
# author : chiangbt@gmail.com
# function : 整个包的测试起点
# 涵盖：
# 分类包：KNN、DecisionTree、Bayesian、Logistic、SVM、AdaBoostTest
# 回归包：线性回归、多元线性回归
# 聚类包：KMeans
# 文本挖掘：SVD、LSI、pLSA、LDA
# 需要安装的第三方包：numpy、scipy、nltk、scikit、gensim
#

import sys
from hmgis.Test.KNNTest import *
from hmgis.Test.DecisionTreeTest import *
from hmgis.Test.BayesianTest import *
from hmgis.Test.LogisticTest import *
from hmgis.Test.SVMTest import *
from hmgis.Test.AdaBoostTest import *
from hmgis.Test.RegressionTest import *
from hmgis.Test.KMeansTest import *
from hmgis.Test.SVDTest import *
from hmgis.Test.RecommendTest import *
from hmgis.Test.LSATest import *
from hmgis.Test.GensimTest.SimpledocTest import *


class ClassifierTest:
	## KNN距离分类测试
	def knnTest(self):
		knn = KNNTest()
		## 最简单的KNN测试，判断一个点的分类情况
		knn.knnTest()
		## 点的可视化
		knn.show2DPoint('data/knn/datingTestSet2.txt')
		knn.show3DPoint('data/knn/datingTestSet2.txt')
		## 从txt文件中获得数据进行分类
		## 分类前会进行归一化处理
		knn.knnTest2('data/knn/datingTestSet2.txt')
		print '-----------------------'
		## 使用scikit learn包中的KNN函数进行分类
		knn.knnTestScikit('data/knn/datingTestSet2.txt')
		## 测试笔迹
		## 将一幅图像转化为一行数据后进行KNN分类
		## 这种方法的最大问题是必须一次性加载数据到内存中，因此实际应用中并不适合
		knn.handwritingClassTest()

	def dtTest(self):
		dt = DecisionTreeDemo()
		dataMat, labels = dt.createDataset('data/dt/lenses.txt')
		dt.dtTest(dataMat, labels)

	def bayesianTest(self):
		bayesian = BayesianTest()
		listOPosts, listClasses = bayesian.loadDataSet()
		bayesian.testingNB()

		rssBayesian = RSSBayesianTest()
		rssBayesian.SingleClassifier()
		rssBayesian.scikitNBClassfier()
		rssBayesian.crossValidClassifier()

		emailBayesian = emailClassfier()
		emailBayesian.spamTest(bayesian)

	def logisticTest(self):
		logic = LogisticTest()
		logic.calGradAscent('data/logistic/testSet.txt')
		logic.calRandomGradAscent('data/logistic/testSet.txt')
		logic.calRandomGradAscent2('data/logistic/testSet.txt')
		logic.multiColicHorseTest()
		logic.calScikitLogistic('data/logistic/testSet.txt')

	def svmTest(self):
		svm = SVMTest()
		'''
		svm.testLinear()
		svm.testMultiLinear()
		svm.testRbf(2)
		svm.testDigits(('rbf',50))
		'''
		svm.testSciKitSVM()

	def adaBoostTest(self):
		ada = AdaBoostTest()
		#ada.adaboostTest()
		ada.scikitAdaboost()

	def regressionTest(self):
		reg = RegressionTest()
		#reg.simpleTest()
		#reg.multiTest()
		#
		#岭回归
		reg.ridgeRegression()

	def kmeansTest(self):
		kmeans = KMeansTest()
		#kmeans.kMeansTest()
		#kmeans.KMeansTest2()
		#kmeans.KMeansTest3()
		kmeans.ClusterClubsTest(6)

	#kmeans.ScikitKMeansTest()

	def SVDTest(self):
		svd = SVDTest()
		svd.svdTest1()
		svd.svdTest2()


	def recommendTest(self):
		recom = RecommendTest()
		recom.recommendTest()
		recom.recommendTest2()
		recom.singleInfoSimilary()

	def LSATest(self):
		lsa = LSATest()
		#lsa.simpleTest()
		#lsa.corpusTest()
		lsa.weiboTest()

	def GensimTest(self):
		gen = GensimTest()
		gen.simple()
		#gen.simple2()
		#gen.GIS3SNewsTopic()
		#gen.weiboTopic()
		## 两个词汇之间的相关性Spearman Rank Corralation公式
		a = [1, 0, 0, 1, 0, 0, 0, 0, 0]
		b = [0, 1, 1, 0, 1, 0, 0, 0, 0]
		#from scipy.stats import *
		#print spearmanr(a, b)


if __name__ == "__main__":
	reload(sys)                         # 2
	sys.setdefaultencoding('utf-8')
	type = sys.getfilesystemencoding()

	classifier = ClassifierTest()
	classifier.knnTest()
	#classifier.dtTest()
	#classifier.bayesianTest()
	#classifier.logisticTest()
	#classifier.svmTest()
	#classifier.adaBoostTest()
	#classifier.regressionTest()
	#classifier.kmeansTest()
	#classifier.SVDTest()
	#classifier.recommendTest()
	#classifier.LSATest()
	#classifier.GensimTest()