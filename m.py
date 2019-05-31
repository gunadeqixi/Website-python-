import urllib.request
import re

qishiweizhi = ['2479845950',0,0]		#起始位置，这个就是抓去图片的起点
num = 0			#抓取总数
no = 1 			#抓取次数
huaban = 19702139			#爬取的画板编号	37194897阿瑟 	16602532待归类采集	19702139……
# 定义一个字符串匹配函数，用于匹配删除无关字符串
def is_paqv(n):
	return n.find('爬取')

# 服务器返回的内容处理函数，利用正则表达式取得有意义的字符串
def jokeCrawler(url,num,no):


	# result是文件中保存了的已采集图片的链接列表
	# divsList是单纯的图片MD5的列表
	# List是带有链接的列表


	headers = ("User-Agent","Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45")
	opener = urllib.request.build_opener()
	opener.addheaders = [headers]
	HTML = opener.open(url).read().decode("utf-8")

	pat1 = '"key":"(.*?)",'
	re_joke = re.compile(pat1,re.S)
	divsList = re_joke.findall(HTML)

	pat2 = '"pin_id":(.*?),'
	# pat2 = '"pin_id":1662270693'
	re_joke2 = re.compile(pat2,re.S)
	divsList2 = re_joke2.findall(HTML)

	# print(len(divsList))
	# print(len(divsList2))
	# print(divsList)
	# print(divsList2)
	List = []
	zuihou = ''
	for i in range(len(divsList)):		#全部都建立在这个i的情况下

		List.append('hbimg.huabanimg.com/'+ str(divsList[i]) +'_fw658')
		if List[i] in result:
			continue			#跳出本次循环

		with open('E:\Python\imgurl.txt','a',encoding='utf-8') as f:
			f.write(List[i]+'\n')                 #将字符串写入文件中
			result.append(List[i])
			# print(divsList2[i])
			
			
			zuihou = divsList2[-1]			#这里还有很多事情要做！！！！！！
			num = num + 1
			# print(List[i])


	if zuihou:
		with open('E:\Python\imgurl.txt','a',encoding='utf-8') as f:
			f.write('\n' + '第' + str(no) + '次爬取结束！' + '\n')
	return [zuihou,num]


# 读取文件成为列表,用于对比除重
result = []
f = open('E:\Python\imgurl.txt','r',encoding='utf-8')
get = f.read()
result = get.split('\n')
f.close()


#循环发送请求获取链接，写入文件，并统计数据
while qishiweizhi[0] != '':

	# zhuyeurl = "https://huaban.com/boards/19702139/?jvjhc2nl&max=" + str(qishiweizhi[0]) + "&limit=20&wfl=1"
	zhuyeurl = "https://huaban.com/boards/" + str(huaban) + "/?jvj7tvx0&max=" + str(qishiweizhi[0]) + "limit=10&wfl=1"	#起始网址

	chuanchu = jokeCrawler(zhuyeurl,num,no)
	qishiweizhi[0] = chuanchu[0]
	qishiweizhi[1] = int(chuanchu[1]) + int(qishiweizhi[1])
	no = no + 1

	if qishiweizhi[1] > 1000:
		exit()

else:
	# print('没有足够的数据量，爬取结束')
	with open('E:\Python\imgurl.txt','a',encoding='utf-8') as f:
		f.write('\n爬取截止，共爬取' + str(qishiweizhi[1]) + '条数据\n')

print('链接库完成，开始下载……')


# ----------------------组建链接库部分结束，接下来是下载部分------------------------


# 读取文件中的链接成为列表，并去除无关字符串
# 读取文件成为列表
result = []
f = open('E:\Python\imgurl.txt','r',encoding='utf-8')
get = f.read()
result = get.split('\n')
f.close()


# 读取文件中的链接成为列表，并去除无关字符串

result[0] = result[0][1:]				#过滤存在在最前面的a字符，截取从第2个字符后的全部字符
result = list(filter(None, result))		#过滤空字符串
result = list(filter(is_paqv, result))		#过滤带有‘爬取’字眼的字符串
list(result)			#filter返回一个迭代式，使用list函数列表化结果
# result.sort()			#重新排列数组







# 将获取到的图片写入硬盘，格式为jpg
nn = 0		#下载失败计数
for i in range(1,len(result)):
	downurl = 'https://' + str(result[i])
	headers = ("User-Agent","Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45")
	opener = urllib.request.build_opener()
	opener.addheaders = [headers]
	# zhuangtaima = opener.open(downurl).getcode()		#获取状态码，200为成功
	
	#异常处理，在爬虫程序中非常重要
	try:
		HTML = opener.open(downurl).read()
		HTML.decode('utf8','ignore')

		with open('E:/Python/img/'+ str(i) +'.jpg','wb') as f:     
			f.write(HTML)
		print("正在写入第"+ str(i) +"张")
	# except BaseException:				#这个是所有异常类的处理方法，但同时会忽略我的ctrl+c的中断操作
	except urllib.error.HTTPError:		#当出现urllib.error.HTTPError类型错误时，执行nn = nn + 1
		nn = nn + 1
	except UnicodeEncodeError:
		nn = nn + 1




print('下载完成，共' + str(len(result) - nn) + '张图片')