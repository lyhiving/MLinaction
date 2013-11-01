# _*_ coding: utf-8 _*_
import sys
from hmgis.Classifier.KNN import *
from hmgis.Classifier.DecisionTree import *
from hmgis.Classifier.Bayesian import *

class ClassifierTest:
	def knnTest(self):
		knn = KNNDemo()
		## 最简单的测试
		knn.knnTest()
		## 加载数据
		datingDataMat, datingLabels = knn.file2matrix('data/knn/datingTestSet2.txt')
		normMat, ranges, minVals = knn.autoNorm(datingDataMat)
		## 二三维可视化
		knn.show2DTest(normMat, datingLabels)
		knn.show3DTest(normMat, datingLabels)
		## 基于数据文件的分类
		knn.knnTest2('data/knn/datingTestSet2.txt')
		knn.knnTestScikit('data/knn/datingTestSet2.txt')
		## 测试笔迹
		knn.handwritingClassTest()

	def dtTest(self):
		dt = DecisionTreeDemo()
		dataMat, labels = dt.createDataset('data/dt/lenses.txt')
		dt.dtTest(dataMat, labels)

	def bayesianTest(self):
		bayesian = Bayesian()
		listOPosts, listClasses = bayesian.loadDataSet()
		## 将数据转化为词袋
		myVocaList = bayesian.createVocabList(listOPosts)
		print myVocaList
		print "第一个文本在词袋中的分布"
		print bayesian.setOfWords2Vec(myVocaList, listOPosts[0])
		## 将两个类型的数据转化为词汇矢量，其值为词汇在文本中的出现次数
		trainMat = []
		for postinDoc in listOPosts:
			trainMat.append(bayesian.setOfWords2Vec(myVocaList, postinDoc))

		## 测试先验概率
		p0V, p1V, pAb = bayesian.trainNB0(trainMat, listClasses)
		print p0V
		print p1V
		print pAb
		## 测试后验概率值
		#bayesian.testingNB()

		## 用一堆文本进行分类测试
		email = emailClassfier()
		#email.spamTest(bayesian)

		## RSS文本测试
		rss = RSSBayesian()
		#rss.SingleClassifier()
		#rss.crossValidClassifier()
		rss.scikitNBClassfier()

if __name__ == "__main__":
	reload(sys)                         # 2
	sys.setdefaultencoding('utf-8')
	type = sys.getfilesystemencoding()

	classifier = ClassifierTest()
	#classifier.knnTest()
	#classifier.dtTest()
	classifier.bayesianTest()