# _*_ coding: utf-8 _*_
import math
import json

from hmgis.InfoRetrieval.sinaweibo.initClient import util
from hmgis.InfoRetrieval.sinaweibo.initClient.initclient import get_client


class sinaweiboClient:
	def getClient(self, APP_KEY, APP_SECRET, CALLBACK_URL):
		return get_client(APP_KEY, APP_SECRET, CALLBACK_URL)

	def getMyselfInfo(self, client, saveFile):
		## 获取用户1725839343,也就是我自己的发出的全部评论
		"""

		:param client:
		:param saveFile:
		"""
		## 获取用户1725839343发出的全部评论
		total_number2 = client.comments.by_me.get()["total_number"]
		page_number2 = int(math.ceil(total_number2 / 100))
		comments = []
		if page_number2 > 1:
			for i in range(0, 10):
				comments += client.comments.by_me.get(count=100, page=i + 1)['comments']

		my_info = open(saveFile, "w")
		my_info.writelines("Text\tCreateTime\tlat\tlng\tUserName\tLocation\n")
		i = 1
		for comment in comments:
			print json.dumps(comment, sort_keys=True, indent=1)
			weibo_info = comment["text"] + "\t" + util.calDate(comment["created_at"]) + "\t";
			## 添加地理位置
			if (not comment["status"]["geo"]):
				weibo_info = weibo_info + " \t \t"
			else:
				geo = comment["status"]["geo"]["coordinates"]
				weibo_info = weibo_info + str(geo[0]) + "\t" + str(geo[1]) + "\t"
			## 添加发出微博的用户名和位置
			info = weibo_info + comment["user"]["name"] + "\t" + comment["user"]["location"] + "\n"
			my_info.writelines(info)
			i = i + 1
		#    for comment in comments:
		#        print str(i) +":" + comment["text"]
		#        my_info.writelines(comment["text"]+ "\n")
		#        i = i+1
		my_info.close()

	def getMyselfPost(self, client, saveFile):
		## 获取用户1725839343发出的全部微博
		r = client.statuses.user_timeline.get(uid=1725839343)
		## print json.dumps(r, sort_keys=True, indent=1)
		total_number = r["total_number"]
		page_number = int(math.ceil(total_number / 100))
		## 获得全部的post数据
		reposts = []
		if page_number > 1:
			for i in range(0, 10):
				reposts += client.statuses.user_timeline.get(uid=1725839343, count=200, page=i + 1)['statuses']

		my_info = open(saveFile, "w")
		my_info.writelines("Text\tCreateTime\tlat\tlng\tUserName\tLocation\n")
		i = 1
		for repost in reposts:
			##print json.dumps(repost, sort_keys=True, indent=1)
			weibo_info = repost["text"] + "\t" + util.calDate(repost["created_at"]) + "\t";
			## 添加地理位置
			if (not repost["geo"]):
				weibo_info = weibo_info + " \t \t"
			else:
				geo = repost["geo"]["coordinates"]
				weibo_info = weibo_info + str(geo[0]) + "\t" + str(geo[1]) + "\t"
			## 添加发出微博的用户名和位置
			my_info.writelines(weibo_info + repost["user"]["name"] + "\t" + repost["user"]["location"] + "\n")
			i = i + 1
		my_info.close()

	def updateWeibo(self, client):
		if not client:
			return
		#根据用户输入内容发微博
		while True:
			print "Ready! Do you want to send a new weiboinfo.txt?(y/n)"
			choice = raw_input()
			if choice == 'y' or choice == 'Y':
				content = raw_input('input the your new weiboinfo.txt content : ')
				if content:
					client.statuses.update.post(status=content)
					print "Send succesfully!"
					break;
				else:
					print "Error! Empty content!"
			if choice == 'n' or choice == 'N':
				break

	## 获取微博信息
	def getFriendsInfo(self, client):
		r0 = client.friendships.friends.bilateral.ids.get(uid=1725839343)
		print '双方互为好友的数量'
		print(r0)

		print '公众事件信息'
		timeline = client.statuses.public_timeline.get()
		# print json.dumps(timeline, sort_keys=True, indent=1)
		for st in timeline.statuses:
			print st["user"]["name"], '发出的信息', st["text"]
		print "--------------------------------------"

		searchResult = client.statuses__friends_timeline()
		# print(json.dumps(searchResult, sort_keys=True, indent=1))
		for st in searchResult.statuses:
			print st["user"]["name"], '发出的信息', st["text"]


class snsGraph:
	def get_edges(self, client, post_id):
		edges = {}
		total_number = client.statuses.repost_timeline.get(id=post_id, count=200)['total_number']
		##    print 'Total Number:',total_number
		reposts = []
		page_reposts = client.statuses.repost_timeline.get(id=post_id, count=200)['reposts']
		reposts += page_reposts
		page_number = int(math.ceil(total_number / 200))
		##    print 'Total Page Number:',page_number
		if page_number > 1:
			for i in range(page_number):
			##            print 'page_number:',i
				reposts += client.statuses.repost_timeline.get(id=post_id, count=200, page=i + 2)['reposts']
		reposts = [repost for repost in reposts if repost.has_key('reposts_count')]##有些微博是删除的
		##    print 'Total Reposts:',len(reposts)
		reposted = client.statuses.show.get(id=post_id)['user']['screen_name']
		if reposted == '':
			reposted = str(client.statuses.show.get(id=post_id)['user']['id'])##存在Screen_name为空的情况
		for repost in reposts:
			if repost['user']['screen_name'] == '':
				edges[repost['id']] = {'poster': str(repost['user']['id']), 'reposted': reposted,
				                       'content': repost['text'], 'created_at': repost['created_at'],
				                       'reposts': repost['reposts_count'], 'comments': repost['comments_count']}
			else:
				edges[repost['id']] = {'poster': repost['user']['screen_name'], 'reposted': reposted,
				                       'content': repost['text'], 'created_at': repost['created_at'],
				                       'reposts': repost['reposts_count'],
				                       'comments': repost['comments_count']}##存在Screen_name为空的情况
		reposts = [repost for repost in reposts if repost['reposts_count'] > 0]
		for repost in reposts:
			self.get_edges(client, repost['id'])
		return edges


	def generate_dot(self, file_name, edges):
		OUT = file_name + ".dot"
		dot = ['"%s" -> "%s" [weibo_id=%s]' % (
		edges[weibo_id]['reposted'].encode('gbk', 'ignore'), edges[weibo_id]['poster'].encode('gbk', 'ignore'),
		weibo_id) for weibo_id in edges.keys()]
		with open(OUT, 'w') as f:
			f.write('strict digraph {\nnode [fontname="STHeiti"]\n%s\n}' % (';\n'.join(dot),))
			print 'dot file export'

