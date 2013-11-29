# _*_ coding: utf-8 _*_

import psycopg2


def addScore():
	conn = psycopg2.connect('dbname=SNSCity user=postgres password=postgres host=localhost port=54321')
	cur = conn.cursor()
	cur.execute('select * from SNSDP where score is null')
	rows = cur.fetchall()
	for row in rows:
		print row[5]
		score = raw_input('input score: ')
		cur.execute('update SNSDP set score=' + str(score) + ' where id = ' + str(row[0]))
		conn.commit()
	cur.close()
	conn.close()


def autoScore():
	conn = psycopg2.connect('dbname=SNSCity user=postgres password=postgres host=localhost port=54321')
	cur = conn.cursor()
	cur.execute('select * from SNSDP where score is null')
	rows = cur.fetchall()
	for row in rows:
		# pos = ['极差','极其糟糕','非常不行','非常不好','性价比太低','气死人了','太坑人了','超级难吃','火大了','太垃圾','巨差','不会再来','恶心',
		#        '太差','死贵','上当','骗子','下次不会去了','都是假的','不会再去了','强烈鄙视','太恶心','态度恶劣',
		#        '假冒伪劣','想想都恶心','以后都不会来','下次不会再去','不要去了','太脏','太次','难吃','太贵']
		# pos = ['差','糟糕','不行','不好','马马虎虎','怎么说呢','失望','性价比不高','服务很差','不新鲜','无语','店大欺客','真不咋地',
		# '真心不咋地','大家别去','不敢恭维','垃圾','坑爹','无法恭维','不怎么样','混乱']
		# pos = ['一般','还行','普通','差不多','就这样','还算可以','凑活','可以接受','要求不能太高','凑合','可以接受','中规中矩','没有特色','还可以','将就','还算周到']
		pos = ['好', '不错', '挺好的', '喜欢', '比较喜欢', '经常来', '不错', '值了', '也不错', '还不错', '挺划算', '推荐', '很实惠', '会经常光顾',
		       '很舒服', '物有所值', '比较满意', '比较实惠', '名不虚传', '很划算', '物美价廉', '价廉物美']
		# pos = ['非常好','非常棒','非常喜欢','十分喜欢','太棒了','太爽了','超值','超级赞','强烈推荐','大爱','很过瘾','超爱','真过瘾','最爱','非常满意']
		for j in pos:
			if j in row[5]:
				print row[0], row[5], 1
				cur.execute('update SNSDP set score=4 where id = ' + str(row[0]))
				break

	conn.commit()
	cur.close()
	conn.close()


def calculate(datestr):
	conn = psycopg2.connect('dbname=SNSCity user=postgres password=postgres host=localhost port=54321')
	cur = conn.cursor()
	cur.execute("select sum(score) from snsdp where pubdate like '" + datestr + "%' and storetype = '酒店'")
	row = cur.fetchone()
	if row[0] is None:
		print 0.0
	else:
		sumscore = row[0]
		# print sumscore
		cur.execute("select count(score) from snsdp where pubdate like '" + datestr + "%' and storetype = '酒店'")
		row = cur.fetchone()
		countscore = row[0]
		# print countscore
		# print datestr
		print sumscore * 1.0 / countscore


def allcalculate(year):
	year = str(year)
	for i in range(1, 10):
		calculate(year + '-0' + str(i))

	calculate(year + '-10')
	calculate(year + '-11')
	calculate(year + '-12')


def parseCSV(infile):
	texts = [line.split('\r') for line in file(infile)]
	for text in texts[0]:
		records = text.split(';')
		print records[10][:-1] + ","

## 测试python链接postgresql数据库
if __name__ == "__main__":
	# cur.execute("CREATE TABLE SNSDP_JD (id serial PRIMARY KEY, shopid integer, storetype varchar, subtype varchar,pubdate varchar, comment varchar);")
	# # cur.execute("INSERT INTO SNSDP (shopid, comment) VALUES (%s, %s)",(100, "abcd"))
	# addScore()
	# autoScore()
	# years = [2005,2006,2007,2008,2009,2010,2011,2012,2013]
	# for year in years:
	# 	allcalculate(year)
	parseCSV('data/dp/score.csv')