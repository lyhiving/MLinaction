# _*_ coding: utf-8 _*_

from hmgis.InfoRetrieval.baidumap.baiduMap import *


class baidumapinfoTest:
	def placeTest(self):
		baidu = baiduMapService('CBf77b6c299fe052b8d9e869438c6301')
		baidu.getPlaceByNameBounds('银行', '39.915,116.404,39.975,116.414')
		baidu.getPlaceByNameRegion('银行', '宁波')
		baidu.getPlaceByNameLocation('银行', '39.915,116.404', 2000)
		baidu.getPlaceDetail('500bb09a14dfb6ababf7297d')

	def geocodeTest(self):
		baidu = baiduMapService('CBf77b6c299fe052b8d9e869438c6301')
		baidu.baiduGeocoder('百度大厦')
		baidu.baiduDecoder('39.983424,116.322987')


if __name__ == "__main__":
	baidu = baidumapinfoTest()
	baidu.placeTest()
	baidu.geocodeTest()