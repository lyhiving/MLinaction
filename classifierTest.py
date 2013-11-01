# _*_ coding: utf-8 _*_
import sys
from hmgis.Test.KNNTest import *
from hmgis.Test.DecisionTreeTest import *
from hmgis.Test.BayesianTest import *
from hmgis.Test.LogisticTest import *
from hmgis.Test.SVMTest import *
from hmgis.Test.AdaBoostTest import *

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
	classifier.adaBoostTest()