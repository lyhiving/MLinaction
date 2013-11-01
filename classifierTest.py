# _*_ coding: utf-8 _*_
import sys
from hmgis.Test.KNNTest import *
from hmgis.Test.DecisionTreeTest import *
from hmgis.Test.BayesianTest import *
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

if __name__ == "__main__":
	reload(sys)                         # 2
	sys.setdefaultencoding('utf-8')
	type = sys.getfilesystemencoding()

	classifier = ClassifierTest()
	#classifier.knnTest()
	#classifier.dtTest()
	classifier.bayesianTest()