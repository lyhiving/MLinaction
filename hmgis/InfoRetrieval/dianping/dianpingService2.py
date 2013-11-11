# _*_ coding: utf-8 _*_
import sys
import urllib2
import cookielib
from BeautifulSoup import *
from  pymongo import Connection
from hmgis.InfoRetrieval.dianping.dianpingService import *


class dianpingService2:
	def parseDianPing(self, shopID):
		###登录页的url
		lgurl = 'http://www.dianping.com/shop/' + shopID
		###用cookielib模块创建一个对象，再用urlllib2模块创建一个cookie的handler
		cookie = cookielib.CookieJar()
		cookie_handler = urllib2.HTTPCookieProcessor(cookie)
		###有些网站反爬虫，这里用headers把程序伪装成浏览器
		hds = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'}

		req = urllib2.Request(url=lgurl, headers=hds) #伪装成浏览器，访问该页面，并POST表单数据，这里并没有实际访问，只是创建了一个有该功能的对象
		opener = urllib2.build_opener(cookie_handler) #绑定handler，创建一个自定义的opener
		response = opener.open(req)#请求网页，返回句柄
		page = response.read()#读取并返回网页内容

		shopinfo = '{'
		# print page #打印到终端显示
		print '-----------------------------------'
		soup = BeautifulSoup(page)
		shopName = soup.find('div', {'class': 'shop-name'}).find('h1', {'class': 'shop-title'})
		## 新建存储文件
		# f = open('data/dp/dp_comment_'+ shopID +'_'+ shopName.text +'.dat', "w")
		## 全部点评数量
		commentInfo = soup.find(name="div", attrs={"class": "comment-tab"}).find('div', {'class': 'tabs'}).findAll(
			'span')
		commentCount = int((commentInfo[-1].text)[5:-1]) / 20 + 2
		## 商户位置信息
		dp = dianpingService('60599581', '23eaa6c4d310401b8fd788074a740873')
		shopinfo += dp.getSingleBusiness(shopID)
		## 点评评分
		comment_star = soup.find(name="div", attrs={"class": "comment-star"}).findAll('em', {'class': 'col-exp'})
		comment_stars_text = ',"Stars":{'
		comment_stars_text += '"All":' + (comment_star[0].text)[1:-1] + ',"5s":' + (comment_star[1]).text[
		                                                                           1:-1] + ',"4s":' + \
		                      (comment_star[2]).text[1:-1] + ',"3s":' + (comment_star[3]).text[1:-1] + ',"2s":' + (
		                                                                                                          comment_star[
			                                                                                                          4]).text[
		                                                                                                          1:-1] + \
		                      ',"1s":' + (comment_star[5]).text[1:-1] + '}'
		shopinfo += comment_stars_text
		## 地址信息
		address1 = soup.find('span', {'class': 'region'})
		address2 = soup.find('span', {'itemprop': 'street-address'})
		tel = soup.find('span', {'class': 'call'})
		address_info = ',"Region":"' + address1.text + '","BusinessName":"' + shopName.text + '","Address":"' + \
		               address2.text + '","tel":"' + str(tel.text) + '"'
		shopinfo += address_info

		## 类型信息
		typeinfo = soup.find(name="div", attrs={"class": "breadcrumb"}).findAll('span', {'class': 'bread-name'})
		type_info = ',"BusinessType":"' + typeinfo[0].text + '","Region2":"' + typeinfo[1].text + '","SubRegion":"' + \
		            typeinfo[2].text + '","SalesType":"' + typeinfo[-1].text + '"'

		shopinfo += type_info
		# f.write(shopinfo)

		shopinfo += ', "comments":{"comments_count":' + (commentInfo[-1].text)[5:-1] + ', "items":['
		for a in range(1, commentCount):
			lgurl2 = 'http://www.dianping.com/shop/' + shopID + '/review_more?pageno=' + str(a)
			req = urllib2.Request(url=lgurl2, headers=hds) #伪装成浏览器，访问该页面，并POST表单数据，这里并没有实际访问，只是创建了一个有该功能的对象
			opener = urllib2.build_opener(cookie_handler) #绑定handler，创建一个自定义的opener
			response = opener.open(req)#请求网页，返回句柄
			page = response.read()#读取并返回网页内容
			soup = BeautifulSoup(page)
			a = soup.findAll(name="div", attrs={"class": "J_brief-cont"})
			for s in a:
				shopinfo += '"' + s.text.strip() + '",'

		shopinfotion = shopinfo[:-1] + ']}}'
		# f.write(shopinfotion)
		# f.close()

		con = Connection()
		db = con.Dianping
		posts = db.NB
		c = eval(shopinfotion)
		posts.insert(c, safe=True)
		print '---', shopName.text, '数据导入MongoDB成功---'


if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')
	dp = dianpingService2()
	dp.parseDianPing('2401360')