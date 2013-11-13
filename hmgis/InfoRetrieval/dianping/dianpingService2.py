# _*_ coding: utf-8 _*_
import sys
import urllib2
import cookielib
from BeautifulSoup import *
from hmgis.InfoRetrieval.dianping.dianpingService import *


class dianpingService2:
	## 将点评网中不同类型的商店名称及其ID保存到文件
	## 由于点评限制，每个类型最多750个商店
	## 唯一没有输入的参数是‘%E4%B8%8A%E5%9C%B0’，代表‘上地’
	def getDistrictFoodShop(self, shoptype, typename, port, type, pages):
		lgurl = 'http://www.dianping.com/search/keyword/2/' + port + '_%E4%B8%8A%E5%9C%B0/' + type + 'p' + pages
		cookie = cookielib.CookieJar()
		cookie_handler = urllib2.HTTPCookieProcessor(cookie)
		###有些网站反爬虫，这里用headers把程序伪装成浏览器
		hds = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'}

		req = urllib2.Request(url=lgurl, headers=hds) #伪装成浏览器，访问该页面，并POST表单数据，这里并没有实际访问，只是创建了一个有该功能的对象
		opener = urllib2.build_opener(cookie_handler) #绑定handler，创建一个自定义的opener
		response = opener.open(req)#请求网页，返回句柄
		page = response.read()#读取并返回网页内容
		# print page
		print '--------------' + str(pages)
		f = open('data/dp/dp_shops_' + shoptype + '.dat', "a")
		soup = BeautifulSoup(page)
		shops = soup.findAll('li', {'class': 'shopname'})
		if len(shops) == 0: return
		for shop in shops:
			shopinfo = typename + '\t' + type + '\t' + shop.contents[1].text + '\t' + shop.contents[1].attrs[0][1][6:]
			print shopinfo
			f.write(shopinfo + '\n')
		f.close()

	## 获得具体商店的信息
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
		soup = BeautifulSoup(page)
		if soup.find(name="div", attrs={"class": "comment-tab"}) == None:
			return

		# print page #打印到终端显示
		print '-----------------------------------'
		shopinfo = '{'
		shopName = soup.find('div', {'class': 'shop-name'}).find('h1', {'class': 'shop-title'})
		## 新建存储文件
		# f = open('data//dp/dp_comment_'+ shopID +'_'+ shopName.text +'.dat', "w")
		f = open('data//dp/dp_comment_.dat', "a")

		## 全部点评数量
		commentInfo = soup.find(name="div", attrs={"class": "comment-tab"}).find('div', {'class': 'tabs'}).findAll(
			'span')
		commentCount = int((commentInfo[-1].text)[5:-1]) / 20 + 2
		## 商户位置信息
		dp = dianpingService('60599581', '23eaa6c4d310401b8fd788074a740873')
		shopinfo += dp.getSingleBusiness(shopID)
		## 点评评分
		comment_star = soup.find(name="div", attrs={"class": "comment-star"}).findAll('em', {'class': 'col-exp'})
		comment_stars_text = ',"count":' + (comment_star[0].text)[1:-1] + ',"Stars":{'
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
		f.write(shopinfotion + ',\n')
		f.close()

		## 输出到mongodb中，如果没有开启Mongodb将这段代码注释
		# con = Connection()
		# db = con.Dianping
		# posts = db.NB
		# c = eval(shopinfotion)
		# posts.insert(c, safe=True)
		print '---', shopName.text, '数据导入MongoDB成功---'


if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')
	dp = dianpingService2()
	# shop = ['4671805', '5398973','4127737','5463893','3190924','14192246']
	# for s in shop:
	# 	dp.parseDianPing(s)
	##--------------------------------------------------
	## lifedic的id为80
	lifedic = {'其它': '26491', '银行': '237', '培训': '196', '小区': '26465', '商务楼': '26466', '学校': '260', '干洗店': '6120',
	           '照相': '4607', '宠物': '194', '旅行社': '197', '牙医': '182', '室内装修': '4606', '家政': '195', '医院': '181',
	           '团购网站': '26119'}
	## shoppingdic的id为20
	shoppingdic = {'超市便利店': '187n2', '服饰鞋包': '120n2', '食品茶酒': '184n2', '其它': '131n2', '家居建材': '126n2', '药店': '235n2',
	               '运动户外': '121n2',
	               '数码家电': '124n2', '化妆品': '123n2', '眼镜店': '128n2', '综合商城': '119n2', '亲子购物': '125n2', '花店': '26085n2',
	               '珠宝饰品': '122n2', '书店': '127n2', '特色集市': '129n2', '品牌折扣店': '130n2'}
	## beautydic的id为50
	beautydic = {'美容SPA': '158n2', '美发': '157n2', '化妆品': '123n2', '瑜伽': '148n2', '齿科': '182n2', '舞蹈': '149n2',
	             '美甲': '160n2',
	             '个性写真': '6700n2', '瘦身纤体': '159n2', '整形': '183n2'}
	## cardic的id为65
	cardic = {'停车场': '180n2', '维修保养': '176n2', '4S店': '175n2', '配件车饰': '177n2', '加油站': '236n2', '汽车租赁': '178n2',
	          '驾校': '179n2'}
	for t in cardic:
		for i in range(1, 10):
			dp.getDistrictFoodShop('汽车', t, '65', str('g' + cardic[t]), str(i))
			# for i in range(1, 50):
			# 	dp.getDistrictShop('结婚','55', str(i))
			## 输出结果
			# {
			# "location": {
			#    "business_id": 2408020,
			#    "latitude": 40.03254,
			#    "longitude": 116.34711,
			#    "avg_rating": 3.5
			# },
			# "Stars": {
			#    "All": 89,
			#    "5s": 13,
			#    "4s": 33,
			#    "3s": 24,
			#    "2s": 8,
			#    "1s": 11
			# },
			# "Region": "海淀区",
			# "BusinessName": "必胜客(清河店)",
			# "Address": "清河一街60号清泽酒店底商(清河站东)",
			# "tel": "010-62992767",
			# "BusinessType": "北京餐厅",
			# "Region2": "海淀区",
			# "SubRegion": "清河",
			# "SalesType": "比萨",
			# "comments": {
			#    "comments_count": 159,
			#    "items": [
			#        "烂到家了，谁去谁倒霉呀！卫生，口味，服务，没有一样像样的，居然还有人去吃！",
			#        "卫生条件真够差的，杯子都没洗干净就敢给顾客用，服务很一般。。味道更一般。不会再来了。"
			#        ]
			#     }
			# }