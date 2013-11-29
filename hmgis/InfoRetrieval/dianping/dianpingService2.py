# _*_ coding: utf-8 _*_
import sys
import urllib2
import cookielib
from pymongo import *
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
			##如果是美食和生活，最后应该为shop.contents[1].attrs[0][1][6:]，否则为4
			shopinfo = typename + '\t' + type + '\t' + shop.contents[1].text + '\t' + shop.contents[1].attrs[0][1][6:]
			print shopinfo
			f.write(shopinfo + '\n')
		f.close()

	## 获得具体商店的信息并将数据保存到postgresql
	def parseDianPing(self, conn, shopID, businessSubtype, filename):
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

		## 判断是否有点评信息
		hasComment = True
		if soup.find(name="div", attrs={"class": "comment-tab"}) == None:
			hasComment = False

		# print page #打印到终端显示
		print '-----------------------------------'
		shopinfo = '{'
		shopName = soup.find('div', {'class': 'shop-name'}).find('h1', {'class': 'shop-title'})
		## 新建存储文件
		# f = open('data//dp/dp_comment_'+ shopID +'_'+ shopName.text +'.dat', "w")
		f = open(filename, "a")

		ds = dianpingService('60599581', '23eaa6c4d310401b8fd788074a740873')
		businessInfo = ds.getSingleBusiness(shopID)
		if businessInfo == '':
			return
		else:
			shopinfo += businessInfo

		if hasComment:
			## 全部点评数量
			commentInfo = soup.find(name="div", attrs={"class": "comment-tab"}).find('div', {'class': 'tabs'}).findAll(
				'span')
			commentCount = int((commentInfo[-1].text)[5:-1]) / 20 + 2
			## 商户位置信息

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
		else:
			shopinfo += ',"count":0,"Stars":{"All":0,"5s":0,"4s":0,"3s":0,"2s":0,"1s":0}'

		## 地址信息
		address1 = soup.find('span', {'class': 'region'})
		address2 = soup.find('span', {'itemprop': 'street-address'})
		tel = soup.find('span', {'class': 'call'})
		if tel == None:
			address_info = ',"Region":"' + address1.text + '","BusinessName":"' + shopName.text + '","Address":"' + \
			               address2.text + '","tel":""'
		else:
			address_info = ',"Region":"' + address1.text + '","BusinessName":"' + shopName.text + '","Address":"' + \
			               address2.text + '","tel":"' + str(tel.text) + '"'
		shopinfo += address_info

		## 类型信息
		typeinfo = soup.find(name="div", attrs={"class": "breadcrumb"}).findAll('span', {'class': 'bread-name'})
		type_info = ',"BusinessType":"' + typeinfo[
			0].text + '","BusinessSubtype":"' + businessSubtype + '","Region2":"' + typeinfo[
			            1].text + '","SubRegion":"' + \
		            typeinfo[2].text + '","SalesType":"' + typeinfo[-1].text + '"'

		shopinfo += type_info
		## postgresql数据库
		cur = conn.cursor()
		if hasComment:
			shopinfo += ', "comments":{"comments_count":' + (commentInfo[-1].text)[5:-1] + ', "items":['
			tmpComment = ''
			for a in range(1, commentCount):
			# for a in range(1, 2):
				lgurl2 = 'http://www.dianping.com/shop/' + shopID + '/review_more?pageno=' + str(a)
				req = urllib2.Request(url=lgurl2, headers=hds) #伪装成浏览器，访问该页面，并POST表单数据，这里并没有实际访问，只是创建了一个有该功能的对象
				opener = urllib2.build_opener(cookie_handler) #绑定handler，创建一个自定义的opener
				response = opener.open(req)#请求网页，返回句柄
				page = response.read()#读取并返回网页内容
				soup = BeautifulSoup(page)
				# a = soup.findAll(name="div", attrs={"class": "J_brief-cont"})
				a = soup.findAll(name="div", attrs={"class": "content"})
				for s in a:
					# shopinfo += '"' + s.text.strip() + '",'
					tmpComment = s.contents[3].text.strip()
					pubdate = s.contents[-2].contents[1].text.strip()
					if len(pubdate) == 5:
						pubdate = '2013-' + pubdate
					elif len(pubdate) > 8:
						pubdate = '2013-' + pubdate[0:5]
					elif len(pubdate) == 8:
						pubdate = '20' + pubdate

					cur.execute(
						"INSERT INTO SNSDP_jd (shopid, storetype, subtype, pubdate, comment) VALUES (%s, %s, %s, %s, %s)",
						(shopID, '酒店', businessSubtype, pubdate, s.contents[3].text.strip()))
				# shopinfo += '"' + a[0].text.strip() + '",'
			shopinfo += '"' + tmpComment + '",'
			conn.commit()
			cur.close()
		else:
			shopinfo += ',"comments":{"comments_count":0, "items":[}'

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

	## 获得具体商店的信息
	def parseDianPing2(self, shopID, businessSubtype, filename):
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

		## 判断是否有点评信息
		hasComment = True
		if soup.find(name="div", attrs={"class": "comment-tab"}) == None:
			hasComment = False

		# print page #打印到终端显示
		print '-----------------------------------'
		shopinfo = '{'
		shopName = soup.find('div', {'class': 'shop-name'}).find('h1', {'class': 'shop-title'})
		## 新建存储文件
		# f = open('data//dp/dp_comment_'+ shopID +'_'+ shopName.text +'.dat', "w")
		f = open(filename, "a")

		ds = dianpingService('60599581', '23eaa6c4d310401b8fd788074a740873')
		businessInfo = ds.getSingleBusiness(shopID)
		if businessInfo == '':
			return
		else:
			shopinfo += businessInfo

		if hasComment:
			## 全部点评数量
			commentInfo = soup.find(name="div", attrs={"class": "comment-tab"}).find('div', {'class': 'tabs'}).findAll(
				'span')
			commentCount = int((commentInfo[-1].text)[5:-1]) / 20 + 2
			## 商户位置信息

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
		else:
			shopinfo += ',"count":0,"Stars":{"All":0,"5s":0,"4s":0,"3s":0,"2s":0,"1s":0}'

		## 地址信息
		address1 = soup.find('span', {'class': 'region'})
		address2 = soup.find('span', {'itemprop': 'street-address'})
		tel = soup.find('span', {'class': 'call'})
		if tel == None:
			address_info = ',"Region":"' + address1.text + '","BusinessName":"' + shopName.text + '","Address":"' + \
			               address2.text + '","tel":""'
		else:
			address_info = ',"Region":"' + address1.text + '","BusinessName":"' + shopName.text + '","Address":"' + \
			               address2.text + '","tel":"' + str(tel.text) + '"'
		shopinfo += address_info

		## 类型信息
		typeinfo = soup.find(name="div", attrs={"class": "breadcrumb"}).findAll('span', {'class': 'bread-name'})
		if (len(typeinfo) > 2):
			type_info = ',"BusinessType":"' + typeinfo[
				0].text + '","BusinessSubtype":"' + businessSubtype + '","Region2":"' + typeinfo[
				            1].text + '","SubRegion":"' + \
			            typeinfo[2].text + '","SalesType":"' + typeinfo[-1].text + '"'
		else:
			type_info = ',"BusinessType":"' + typeinfo[
				0].text + '","BusinessSubtype":"' + businessSubtype + '","Region2":"' + typeinfo[
				            1].text + '","SubRegion":"","SalesType":"' + typeinfo[-1].text + '"'

		shopinfo += type_info
		shopinfo2 = shopinfo

		if hasComment:
			shopinfo += ', "comments":{"comments_count":' + (commentInfo[-1].text)[5:-1] + ', "items":['
			shopinfo2 += ', "comments":{"comments_count":' + (commentInfo[-1].text)[5:-1] + ', "items":['
			tmpComment = ''
			for a in range(1, commentCount):
			# for a in range(1, 2):
				lgurl2 = 'http://www.dianping.com/shop/' + shopID + '/review_more?pageno=' + str(a)
				req = urllib2.Request(url=lgurl2, headers=hds) #伪装成浏览器，访问该页面，并POST表单数据，这里并没有实际访问，只是创建了一个有该功能的对象
				opener = urllib2.build_opener(cookie_handler) #绑定handler，创建一个自定义的opener
				response = opener.open(req)#请求网页，返回句柄
				page = response.read()#读取并返回网页内容
				soup = BeautifulSoup(page)
				a = soup.findAll(name="div", attrs={"class": "J_brief-cont"})
				for s in a:
					shopinfo2 += '"' + s.text.strip().replace('\\', '') + '",'
					tmpComment = s.text.strip().replace('\\', '')
			shopinfo += '"' + tmpComment + '",'
		else:
			shopinfo += ',"comments":{"comments_count":0, "items":[""}'
			shopinfo2 += ',"comments":{"comments_count":0, "items":[""}'

		shopinfotion = shopinfo[:-1] + ']}}'
		shopinfotion2 = shopinfo2[:-1] + ']}}'
		f.write(shopinfotion + ',\n')
		f.close()

		## 输出到mongodb中，如果没有开启Mongodb将这段代码注释
		con = Connection()
		db = con.SNSCity
		posts = db.SNSDP
		c = eval(shopinfotion2)
		posts.insert(c, safe=True)
		print '---', shopName.text, '数据导入MongoDB成功---'


class dianpingTest:
	## 获得一个区域类所有的点评信息
	def getShopsTest(self):
		dp = dianpingService2()
		## fooddic的id为10
		fooddic = {'小吃快餐': '112', '其它美食': '118', '川菜': '102', '火锅': '110', '北京菜': '311', '面包甜点': '117', '湘菜': '104',
		           '西餐': '116', '东北菜': '106', '韩国料理': '114', '日本料理': '113', '清真食品': '108', '西北菜': '26481', '粤菜': '103',
		           '自助餐': '111', '江浙菜': '101', '云南菜': '248', '湖北菜': '246', '海鲜': '251', '鲁菜': '26483', '新疆菜': '3243',
		           '贵州菜': '105', '素菜': '109'}
		## lifedic的id为80
		lifedic = {'其它': '26491', '银行': '237', '培训': '196', '小区': '26465', '商务楼': '26466', '学校': '260', '干洗店': '6120',
		           '照相': '4607', '宠物': '194', '旅行社': '197', '牙医': '182', '室内装修': '4606', '家政': '195', '医院': '181',
		           '团购网站': '26119'}
		## shoppingdic的id为20
		shoppingdic = {'超市便利店': '187n2', '服饰鞋包': '120n2', '食品茶酒': '184n2', '其它': '131n2', '家居建材': '126n2',
		               '药店': '235n2',
		               '运动户外': '121n2',
		               '数码家电': '124n2', '化妆品': '123n2', '眼镜店': '128n2', '综合商城': '119n2', '亲子购物': '125n2',
		               '花店': '26085n2',
		               '珠宝饰品': '122n2', '书店': '127n2', '特色集市': '129n2', '品牌折扣店': '130n2'}
		## beautydic的id为50
		beautydic = {'美容SPA': '158n2', '美发': '157n2', '化妆品': '123n2', '瑜伽': '148n2', '齿科': '182n2', '舞蹈': '149n2',
		             '美甲': '160n2', '个性写真': '6700n2', '瘦身纤体': '159n2', '整形': '183n2'}
		## cardic的id为65
		cardic = {'停车场': '180n2', '维修保养': '176n2', '4S店': '175n2', '配件车饰': '177n2', '加油站': '236n2', '汽车租赁': '178n2',
		          '驾校': '179n2'}
		## xxdic的id为30
		xxdic = {'足底按摩': '141n2', '咖啡厅': '132n2', '洗浴': '140n2', '其它休闲娱乐': '26490n2', 'KTV': '135n2', '茶馆': '134n2',
		         '文化艺术': '142n2', '台球': '156n2', '公园': '138n2', '景点郊游': '139n2', '酒吧': '133n2',
		         '电影院': '136n2', 'DIY手工坊': '144n2', '游乐游艺': '137n2', '桌面游戏': '6694n2'}
		## babydic的id为70
		babydic = {'幼儿教育': '188n2', '亲子游乐': '161n2', '亲子购物': '125n2', '亲子摄影': '193n2', '孕产护理': '258n2',
		           '其它亲子服务': '27769n2'}
		## sportdic的id为45
		sportdic = {'健身中心': '147n2', '瑜伽': '148n2', '武术场馆': '6701n2', '其它运动设施': '145n2', '舞蹈': '149n2', '台球馆': '156n2',
		            '羽毛球馆': '152n2', '游泳馆': '151n2', '网球场': '153n2', '篮球场': '146n2', '足球场': '6702n2',
		            '高尔夫球场': '154n2', '兵乓球馆': '6712n2', '体育场馆': '150n2'}
		## hoteldic的id为60
		hoteldic = {'其他酒店': '174n2', '经济型酒店': '171n2', '三星级酒店': '170n2', '公寓式酒店': '6693n2', '青年旅社': '172n2',
		            '四星级酒店': '169n2',
		            '五星级酒店': '168n2', '度假村': '173n2', '农家院': '6858n2'}
		## marrydic的id为55
		marrydic = {'婚宴酒店': '165n2', '婚纱礼服': '162n2', '婚纱摄影': '163n2', '婚庆公司': '167n2', '个性写真': '6700n2',
		            '彩妆造型': '166n2',
		            '婚介首饰': '191n2', '婚房装修': '6844n2', '更多婚礼服务': '25410n2'}
		for t in lifedic:
			for i in range(1, 20):
				dp.getDistrictFoodShop('生活设施', t, '80', str('g' + lifedic[t]), str(i))

	## 根据shopid号获得一个店的具体信息，并将点评数据保存到postgresql数据库中
	def getShopInfoPostgresql(self):
		dp = dianpingService2()
		shops = [shop.replace('\n', '') for shop in file('data/dp/dp_shops_酒店.dat')]
		import psycopg2

		conn = psycopg2.connect('dbname=SNSCity user=postgres password=postgres host=localhost port=54321')

		for s in shops:
			s1 = s.split('\t')
			print s1[3]
			dp.parseDianPing(conn, s1[3], s1[0], 'data/dp/dp_comments_酒店1.dat')

		conn.close()

	## 根据shopid号获得一个店的具体信息，并将点评数据保存到mongodb数据库中
	def getShopInfoMongodb(self):
		dp = dianpingService2()
		shops = [shop.replace('\n', '') for shop in file('data/dp/dp_shops_酒店.dat')]
		for s in shops:
			s1 = s.split('\t')
			print s1[3]
			dp.parseDianPing2(s1[3], s1[0], 'data/dp/dp_comments_酒店.dat')


	def convertJSONtoCSV(self):
		type = ['丽人', '亲子', '休闲娱乐', '商业设施', '婚庆', '汽车', '生活设施', '美食', '运动', '酒店']
		for t in type:
			info = [poi.replace('\n', '') for poi in file('data/dp/dp_comments_' + t + '.dat')]
			f = open('data/dp/dp_comment_All.dat', 'a')
			for s in info:
				m = eval(s[:-1])
				t = str(m['business_id']) + '\t' + m['BusinessName'] + '\t' + m['BusinessSubtype'] + '\t' + str(
					m['lat']) + '\t' + str(m['lng']) + '\t' + str(m['avg_rating']) + '\t' + str(
					m['Stars']['All']) + '\t' + m['Region'] + '\t' + m['Address']
				print t
				f.write(t + '\n')


if __name__ == "__main__":
	reload(sys)
	sys.setdefaultencoding('utf-8')
	## 获取某个区域类全部类型POI的方法
	test = dianpingTest()
	# test.getShopsTest()
	test.getShopInfoPostgresql()
	# test.getShopInfoMongodb()
	# test.convertJSONtoCSV()