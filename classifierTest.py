# _*_ coding: utf-8 _*_
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
	def knnTest(self):
		knn = KNNTest()
		knn.knnTest()
		knn.show2DPoint('data/knn/datingTestSet2.txt')
		knn.show3DPoint('data/knn/datingTestSet2.txt')
		knn.knnTest2('data/knn/datingTestSet2.txt')
		print '-----------------------'
		knn.knnTestScikit('data/knn/datingTestSet2.txt')
		## 测试笔迹
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
		reg  = RegressionTest()
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
		#gen.simple()
		#gen.simple2()
		#gen.GIS3SNewsTopic()
		gen.weiboTopic()

if __name__ == "__main__":
	reload(sys)                         # 2
	sys.setdefaultencoding('utf-8')
	type = sys.getfilesystemencoding()

	classifier = ClassifierTest()
	#classifier.knnTest()
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
	classifier.GensimTest()