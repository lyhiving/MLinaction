# _*_ coding: utf-8 _*_
import sys

from hmgis.InfoRetrieval.sinaweibo.sinaweiboClient import *


class sinaweiboTest:
	def getMyselfComment(self):
		"""
		获得自己发出的评论信息
		"""
		APP_KEY = "4150821454"
		APP_SECRET = "8480193faebfbb17566427b4e8d2f773"
		CALLBACK_URL = "http://127.0.0.1/library/Rcitylearning/doc/callback.html"
		sw = sinaweiboClient()
		client = sw.getClient(APP_KEY, APP_SECRET, CALLBACK_URL)
		sw.getMyselfInfo(client, 'data/weibo/jiangbt_comment.txt')

	def getMyselfPost(self):
		"""
		获得自己发出的信息
		"""
		APP_KEY = "4150821454"
		APP_SECRET = "8480193faebfbb17566427b4e8d2f773"
		CALLBACK_URL = "http://127.0.0.1/library/Rcitylearning/doc/callback.html"
		sw = sinaweiboClient()
		client = sw.getClient(APP_KEY, APP_SECRET, CALLBACK_URL)
		sw.getMyselfPost(client, 'data/weibo/jiangbt_post.txt')

	def updateMyWeibo(self):
		"""
		获得自己发出的信息
		"""
		APP_KEY = "4150821454"
		APP_SECRET = "8480193faebfbb17566427b4e8d2f773"
		CALLBACK_URL = "http://127.0.0.1/library/Rcitylearning/doc/callback.html"
		sw = sinaweiboClient()
		client = sw.getClient(APP_KEY, APP_SECRET, CALLBACK_URL)
		sw.updateWeibo(client)

	def getInfo(self):
		"""
		获得朋友发出的信息
		"""
		APP_KEY = "4150821454"
		APP_SECRET = "8480193faebfbb17566427b4e8d2f773"
		CALLBACK_URL = "http://127.0.0.1/library/Rcitylearning/doc/callback.html"
		sw = sinaweiboClient()
		client = sw.getClient(APP_KEY, APP_SECRET, CALLBACK_URL)
		sw.getFriendsInfo(client)

	def drawGraph(self):
		APP_KEY = "4150821454"
		APP_SECRET = "8480193faebfbb17566427b4e8d2f773"
		CALLBACK_URL = "http://127.0.0.1/library/Rcitylearning/doc/callback.html"
		sw = sinaweiboClient()
		client = sw.getClient(APP_KEY, APP_SECRET, CALLBACK_URL)
		snsg = snsGraph()
		edges = snsg.get_edges(client, 3609326415433045)
		snsg.generate_dot("data/weibo/demo", edges)

	def getPOIbyPlacename(self):
		"""
		查询地名

		"""
		APP_KEY = "4150821454"
		APP_SECRET = "8480193faebfbb17566427b4e8d2f773"
		CALLBACK_URL = "http://127.0.0.1/library/Rcitylearning/doc/callback.html"
		sw = sinaweiboClient()
		client = sw.getClient(APP_KEY, APP_SECRET, CALLBACK_URL)
		sw.getPOIFromPlacename(client, '理想国际')

	def getPOIIDbyPoiname(self):
		"""
		查询地名

		"""
		APP_KEY = "4150821454"
		APP_SECRET = "8480193faebfbb17566427b4e8d2f773"
		CALLBACK_URL = "http://127.0.0.1/library/Rcitylearning/doc/callback.html"
		sw = sinaweiboClient()
		client = sw.getClient(APP_KEY, APP_SECRET, CALLBACK_URL)
		sw.getPOIIDFromPoiname(client, '理想国际')

	def getPoiInfo(self):
		"""
		查询地名

		"""
		APP_KEY = "4150821454"
		APP_SECRET = "8480193faebfbb17566427b4e8d2f773"
		CALLBACK_URL = "http://127.0.0.1/library/Rcitylearning/doc/callback.html"
		sw = sinaweiboClient()
		client = sw.getClient(APP_KEY, APP_SECRET, CALLBACK_URL)
		sw.getPoiinfo(client, 'B2094654D16CABFE419E')


if __name__ == "__main__":
## 确保提取出来的数据以utf-8格式进行存储
	reload(sys)
	sys.setdefaultencoding('utf-8')
	sinaweibo = sinaweiboTest()
	# sinaweibo.getMyselfPost()
	# sinaweibo.updateMyWeibo()
	# sinaweibo.getInfo()
	# sinaweibo.drawGraph()
	# sinaweibo.getPOIbyPlacename()
	# sinaweibo.getPOIIDbyPoiname()
	sinaweibo.getPoiInfo()