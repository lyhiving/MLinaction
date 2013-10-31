# _*_ coding: utf-8 _*_

from numpy import *
from numpy import linalg as la


class SVD:
	def loadExData(self):
		return [[0, 0, 0, 2, 2],
		        [0, 0, 0, 3, 3],
		        [0, 0, 0, 1, 1],
		        [1, 1, 1, 0, 0],
		        [2, 2, 2, 0, 0],
		        [5, 5, 5, 0, 0],
		        [1, 1, 1, 0, 0]]

	def loadExData2(self):
		return [[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
		        [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
		        [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
		        [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
		        [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
		        [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
		        [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
		        [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
		        [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
		        [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
		        [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]]

	## SVD第一个测试，可以看出SIGMA的值有5项，但前2项远大于后3项
	## 这样实际上原始矩阵Data = Um2*Sigma22*VT2n来表示
	def svdTest1(self):
		data = self.loadExData()
		U, Sigma, VT = la.svd(data)
		print U
		print Sigma
		print VT
		## 将Sigma的主要值提取出来
		print '--------------------------------------'
		Sig3 = mat([[Sigma[0], 0], [0, Sigma[1]]])
		## 下面这个矩阵和原矩阵非常类似
		print data
		print U[:, :2] * Sig3 * VT[:2, :]

	## 计算缩减的sigma，可以获得表示90%量的
	def svdTest2(self):
		data = self.loadExData2()
		print mat(data).A
		U, Sigma, VT = la.svd(data)
		print mat(U).A
		print mat(Sigma).A
		print mat(VT).A
		sig2 = Sigma ** 2
		print "--------------------"
		print "sigma值总量", sum(sig2)
		print "sigma值90%", sum(sig2)*0.9
		##
		print sum(sig2[:2])
		print sum(sig2[:3])

class Recommend:
	## 欧式距离
	def ecludSim(self, inA, inB):
		return 1.0 / (1.0 + la.norm(inA - inB))

	## 皮尔逊距离
	def pearsSim(self, inA, inB):
		if len(inA) < 3: return 1.0
		return 0.5 + 0.5 * corrcoef(inA, inB, rowvar=0)[0][1]

	## COS距离
	def cosSim(self, inA, inB):
		num = float(inA.T * inB)
		denom = la.norm(inA) * la.norm(inB)
		return 0.5 + 0.5 * (num / denom)

	def standEst(self, dataMat, user, simMeas, item):
		n = shape(dataMat)[1]
		simTotal = 0.0;
		ratSimTotal = 0.0
		for j in range(n):
			userRating = dataMat[user, j]
			if userRating == 0: continue
			overLap = nonzero(logical_and(dataMat[:, item].A > 0, \
			                              dataMat[:, j].A > 0))[0]
			if len(overLap) == 0:
				similarity = 0
			else:
				similarity = simMeas(dataMat[overLap, item], \
				                     dataMat[overLap, j])
			print 'the %d and %d similarity is: %f' % (item, j, similarity)
			simTotal += similarity
			ratSimTotal += similarity * userRating
		if simTotal == 0:
			return 0
		else:
			return ratSimTotal / simTotal

	def svdEst(self, dataMat, user, simMeas, item):
		n = shape(dataMat)[1]
		simTotal = 0.0;
		ratSimTotal = 0.0
		U, Sigma, VT = la.svd(dataMat)
		Sig4 = mat(eye(4) * Sigma[:4]) #arrange Sig4 into a diagonal matrix
		xformedItems = dataMat.T * U[:, :4] * Sig4.I  #create transformed items
		print xformedItems
		for j in range(n):
			userRating = dataMat[user, j]
			if userRating == 0 or j == item: continue
			similarity = simMeas(xformedItems[item, :].T, \
			                     xformedItems[j, :].T)
			print 'the %d and %d similarity is: %f' % (item, j, similarity)
			simTotal += similarity
			ratSimTotal += similarity * userRating
		if simTotal == 0:
			return 0
		else:
			return ratSimTotal / simTotal

	def recommend(self, dataMat, user, N=3, simMeas=cosSim, estMethod=standEst):
		## 找出用户对哪些物品没有进行过打分
		unratedItems = nonzero(dataMat[user, :].A == 0)[1]#find unrated items
		if len(unratedItems) == 0: return 'you rated everything'
		itemScores = []
		for item in unratedItems:
			estimatedScore = estMethod(dataMat, user, simMeas, item)
			itemScores.append((item, estimatedScore))
		return sorted(itemScores, key=lambda jj: jj[1], reverse=True)[:N]

	def printMat(self, inMat, thresh=0.8):
		for i in range(32):
			for k in range(32):
				if float(inMat[i, k]) > thresh:
					print 1,
				else:
					print 0,
			print ''

	## 基于物品相似度的推荐
	def recommendTest(self):
		svd = SVD()
		myMat = mat(svd.loadExData())
		print myMat
		myMat[0, 1] = myMat[0, 0] = myMat[1, 0] = myMat[2, 0] = 4
		myMat[3, 3] = 2
		print myMat
		## 第一个参数为数据，第二个参数为用户，第三个参数为数量
		## 结果为[(2, 2.5), (1, 2.0243290220056256)]，表示用户对第1和2项的估计评分
		print self.recommend(myMat, 2, 5, self.cosSim, self.standEst)

	def recommendTest2(self):
		svd = SVD()
		myMat = mat(svd.loadExData2())
		## 第一个参数为数据，第二个参数为用户，第三个参数为数量
		## 结果为[(2, 2.5), (1, 2.0243290220056256)]，表示用户对第1和2项的估计评分
		print self.recommend(myMat, 2, 8, self.cosSim, self.svdEst)
		print self.recommend(myMat, 2, 8, self.cosSim, self.standEst)

if __name__ == "__main__":
	svd = SVD()
	svd.svdTest2()

	recom = Recommend()
	#recom.recommendTest()
	#recom.recommendTest2()