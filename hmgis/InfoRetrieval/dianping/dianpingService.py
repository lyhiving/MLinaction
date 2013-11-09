# _*_ coding: utf-8 _*_
from urllib import *
import json
import hashlib


class dianpingService:
	def __init__(self, appkey, appsecret):
		self.appkey = appkey
		self.appsecret = appsecret

	def createRequestUrl(self, paramSet, apiUrl):
		#参数排序与拼接
		paramMap = {}
		for pair in paramSet:
			paramMap[pair[0]] = pair[1]

		codec = self.appkey
		for key in sorted(paramMap.iterkeys()):
			codec += key + paramMap[key]

		codec += self.appsecret
		#签名计算
		sign = (hashlib.sha1(codec).hexdigest()).upper()
		#拼接访问的URL
		url_trail = "appkey=" + self.appkey + "&sign=" + sign
		for pair in paramSet:
			url_trail += "&" + pair[0] + "=" + pair[1]

		requestUrl = apiUrl + "?" + url_trail
		return requestUrl

	def get_categories_with_businesses(self):
		paramSet = []
		url = 'http://api.dianping.com/v1/metadata/get_categories_with_businesses'
		url = self.createRequestUrl(paramSet, url)
		req = urlopen(url).read()
		# print req
		res = json.loads(req)
		categories = res['categories']
		for category in categories:
			print category["category_name"]
			for sub_category in category["subcategories"]:
				print "\t" + sub_category["category_name"]
				for sub_sub_category in sub_category["subcategories"]:
					print "\t\t" + sub_sub_category
		return categories

	def find_businesses(self):
		paramSet = []
		paramSet.append(("format", "json"))
		paramSet.append(("city", "上海"))
		paramSet.append(("latitude", "31.21524"))
		paramSet.append(("longitude", "121.420033"))
		paramSet.append(("category", "美食"))
		paramSet.append(("region", "长宁区"))
		paramSet.append(("limit", "20"))
		paramSet.append(("radius", "2000"))
		paramSet.append(("offset_type", "0"))
		paramSet.append(("has_coupon", "1"))
		paramSet.append(("has_deal", "1"))
		paramSet.append(("keyword", "菜"))
		paramSet.append(("sort", "7"))
		url = 'http://api.dianping.com/v1/business/find_businesses'
		url = self.createRequestUrl(paramSet, url)
		# print url
		req = urlopen(url).read()
		# print req
		res = json.loads(req)
		for business in res["businesses"]:
			print str(business["business_id"]) + '\t' + business["name"] + '\t' + business["branch_name"]


if __name__ == "__main__":
	dianping = dianpingService('60599581', '23eaa6c4d310401b8fd788074a740873')
	dianping.get_categories_with_businesses()
	dianping.find_businesses()