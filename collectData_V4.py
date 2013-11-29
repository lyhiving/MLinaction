# coding: utf-8
import sys
import urllib
import urllib2
import os
import time
import datetime
import random
import logging

from lxml import etree


class CollectData():
	def __init__(self, keyword, startTime, region, savedir, interval, fileNum='0', flag=True,
	             begin_url_per="http://s.weibo.com/weibo/"):
		self.logger = self.initlog()
		self.begin_url_per = begin_url_per
		self.setKeyword(keyword)
		self.setStartTimescope(startTime)
		self.setRegion(region)
		self.setSave_dir(savedir)
		self.setInterval(interval)
		self.setFileNum(fileNum)
		self.setFlag(flag)

	def setKeyword(self, keyword):
		self.keyword = keyword.decode('GBK').encode("utf-8")
		print 'twice encode:', self.getKeyWord()

	def setStartTimescope(self, startTime):
		start_datetime_1 = datetime.datetime.fromtimestamp(time.mktime(time.strptime(startTime, "%Y-%m-%d-%H")))
		start_new_datetime_1 = start_datetime_1 - datetime.timedelta(seconds=3600)
		start_str_1 = start_new_datetime_1.strftime("%Y-%m-%d-%H")
		self.timescope = start_str_1 + ":" + start_str_1

	def setRegion(self, region):
		self.region = region

	def setSave_dir(self, save_dir):
		self.save_dir = save_dir

	def setInterval(self, interval):
		self.interval = int(interval)

	def setFileNum(self, fileNum):
		self.fileNum = int(fileNum)

	def setFlag(self, flag):
		self.flag = flag

	def initlog(self):
		logger = logging.getLogger()
		logFile = './collect.log'
		filehandler = logging.FileHandler(logFile)
		formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
		filehandler.setFormatter(formatter)
		logger.addHandler(filehandler)
		logger.setLevel(logging.NOTSET)
		return logger

	def getURL(self):
		return self.begin_url_per + self.getKeyWord() + "&region=custom:" + self.region + "&xsort=time&timescope=custom:" + self.timescope + "&nodup=1&page="

	def getKeyWord(self):
		once = urllib.urlencode({"kw": self.keyword})[3:]
		return urllib.urlencode({"kw": once})[3:]

	def download(self, url, fileNum, frompid=1, maxTryNum=4):
		if not os.path.exists(self.save_dir):
			os.mkdir(self.save_dir)
		i = frompid
		content = open(self.save_dir + os.sep + str(fileNum) + ".txt", "w")
		hasMore = True
		mid_filter = set([]);
		isCaught = False
		while hasMore and i < 51 and (not isCaught):
			source_url = url + str(i)
			data = ''
			goon = True
			for tryNum in range(maxTryNum):
				try:
					data = urllib2.urlopen(source_url).read()
					break
				except:
					if tryNum < (maxTryNum - 1):
						time.sleep(10)
						continue
					else:
						print 'Internet Connect Error!'
						self.logger.error('Internet Connect Error!')
						self.logger.info('url: ' + source_url)
						self.logger.info('fileNum: ' + str(fileNum))
						self.logger.info('page: ' + str(i))
						self.flag = False
						goon = False
						break
			if goon:
				lines = data.splitlines()
				isCaught = True
				for line in lines:
					if line.startswith('<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_weibo_feedlist"'):
						isCaught = False;
						n = line.find('html":"')
						if n > 0:
							j = line[n + 7: -12].encode("utf-8").decode('unicode_escape').encode("utf-8").replace("\\",
							                                                                                      "")
							if (j.find('<div class="pl_noresult">') > 0):
								hasMore = False
							else:
								page = etree.HTML(j)
								dls = page.xpath(u"//dl")
								for dl in dls:
									mid = str(dl.attrib.get('mid'))
									if (mid != 'None' and mid not in mid_filter):
										mid_filter.add(mid)
										content.write(mid)
										content.write('\n')
				lines = None
				if isCaught:
					print 'Be Caught!'
					self.logger.error('Be Caught Error!')
					self.logger.info('url: ' + source_url)
					self.logger.info('fileNum: ' + str(fileNum))
					self.logger.info('page:' + str(i))
					data = None
					self.flag = False
					break
				if not hasMore:
					print 'No More Results!'
					time.sleep(20)
					data = None
					break
				i += 1
				#设置随机休眠时间
				sleeptime_one = random.randint(self.interval - 30, self.interval - 10)
				sleeptime_two = random.randint(self.interval + 10, self.interval + 30)
				if i % 2 == 0:
					sleeptime = sleeptime_two
				else:
					sleeptime = sleeptime_one
				print sleeptime
				time.sleep(sleeptime)
			else:
				break
		content.close()
		content = None

	def getTimescope(self, perTimescope, hours):
		times_list = perTimescope.split(':')
		start_datetime = datetime.datetime.fromtimestamp(time.mktime(time.strptime(times_list[-1], "%Y-%m-%d-%H")))
		start_new_datetime = start_datetime + datetime.timedelta(seconds=3600)
		end_new_datetime = start_new_datetime + datetime.timedelta(seconds=3600 * (hours - 1))
		start_str = start_new_datetime.strftime("%Y-%m-%d-%H")
		end_str = end_new_datetime.strftime("%Y-%m-%d-%H")
		return start_str + ":" + end_str


while True:
	keyword = raw_input('Enter the keyword(type \'quit\' to exit ):')
	if keyword == 'quit':
		sys.exit()
	startTime = raw_input('Enter the start time(Format:YYYY-mm-dd-HH):')
	##region = raw_input('Enter the region([',unicode('北京',"gb2312"),']11:1000,[',unicode('上海',"gb2312"),']31:1000,[',unicode('广州',"gb2312"),']44:1,[',unicode('成都',"gb2312"),']51:1):')
	##region = raw_input('Enter the region([',unicode('北京',"utf8"),']11:1000,[',unicode('上海',"utf8"),']31:1000,[',unicode('广州',"utf8"),']44:1,[',unicode('成都',"utf8"),']51:1):')
	##region = raw_input('Enter the region(['+u'北京'.decode('utf-8').encode("GBK")+']11:1000,['+u'上海'.decode('utf-8').encode("GBK")+']31:1000,['+u'广州'.decode('utf-8').encode("GBK")+']44:1,['+u'成都'.decode('utf-8').encode("GBK")+']51:1):')
	region = raw_input('Enter the region([BJ]11:1000,[SH]31:1000,[GZ]44:1,[CD]51:1):')
	savedir = raw_input('Enter the save directory(Like C://data//):')
	interval = raw_input('Enter the time interval( >30 and deafult:50):')
	fileNum = raw_input('Enter the file number(Just integer):')
	cd = CollectData(keyword, startTime, region, savedir, interval, fileNum)
	while cd.flag:
		cd.timescope = cd.getTimescope(cd.timescope, 1)
		cd.fileNum += 1
		print cd.timescope
		print cd.fileNum
		cd.logger.info(cd.timescope)
		cd.logger.info(cd.fileNum)
		url = cd.getURL()
		##    print url
		cd.download(url, cd.fileNum)
	else:
		del (cd)
		cd = None
		print '-----------------------------------------------------'
		print '-----------------------------------------------------'
