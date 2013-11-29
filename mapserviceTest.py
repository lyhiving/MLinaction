# _*_ coding: utf-8 _*_

from hmgis.InfoRetrieval.baidumap.baiduMap import *

## baidumapinfoTest专用于对百度地图的服务进行测试
class baidumapinfoTest:
	def placeTest(self):
		"""
		baiduMapService的四个类用于检索POI
		CBf77b6c299fe052b8d9e869438c6301为用户注册的key
		"""
		baidu = baiduMapService('CBf77b6c299fe052b8d9e869438c6301')
		## 根据范围检索POI
		baidu.getPlaceByNameBounds('银行', '39.915,116.404,39.975,116.414')
		## 根据区域名称检索POI
		baidu.getPlaceByNameRegion('银行', '宁波')
		## 根据位置及半径检索POI
		baidu.getPlaceByNameLocation('银行', '39.915,116.404', 2000)
		## 获得UID指向的具体POI点的详情
		baidu.getPlaceDetail('500bb09a14dfb6ababf7297d')

	def geocodeTest(self):
		"""
		测试百度地图的地理编码和反地理编码
		"""
		baidu = baiduMapService('CBf77b6c299fe052b8d9e869438c6301')
		## 地理编码
		baidu.baiduGeocoder('百度大厦')
		## 反地理编码
		baidu.baiduDecoder('39.983424,116.322987')


if __name__ == "__main__":
	baidu = baidumapinfoTest()
	baidu.placeTest()
	# baidu.geocodeTest()