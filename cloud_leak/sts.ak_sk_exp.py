# -*- coding: utf-8 -*-
import oss2
import json

key =''' 
{"code":0,"msg":"访问成功","domain":"http://mars.sharedaka.com","data":{"securityToken":"CAIS8wF1q6Ft5B2yfSjIr5fBD+DynIpMhaGxe3X7sXkdNMRtgb/fhzz2IHBNdXNvCesYvvUxmmFY6PcZlqNvRoRZAFDDbsZ2tn/eW6AzJtivgde8yJBZor/HcDHhJnyW9cvWZPqDP7G5U/yxalfCuzZuyL/hD1uLVECkNpv74vwOLK5gPG+CYCFBGc1dKyZ7tcYeLgGxD/u2NQPwiWeiZygB+CgE0DkutfvnmJHGt0uF3AKmk9V4/dqhfsKWCOB3J4p6XtuP2+h7S7HMyiY46WIRpP4n1vMUommX74/DUgkPsk6cUfDZ+9EqMg51a68qxnDsdXYkW5cagAGdjoZfulBHQ2emNEx8t/LZUbNDRDLy9iFIhuIhiO9X149+oc7VoZGn5M47i/8CxlVkBibVj/AyHGMBbcpsz7OYWz4OnLq/Fu8G8Ecz0CLp+FBFQ7/xmQeOUeEFU0LfLcvkJszDt0fYU3ZdJdGu+aiPczvYIfCOH8fS+k3d30HV9g==","accessKeyId":"STS.NTtDZFqUm2cZySJUyH8KAnzte","accessKeySecret":"4gMcv7qsRTZvhHt1GxaK8htcDpn9ZvuWSGEwvPVrba33","expiration":"2020-01-15T13:42:12Z"},"success":true}
'''
key = json.loads(key)['data']
key = dict((k.lower(), v) for k, v in key.iteritems())

print key
#print key['endpoint']

key['accesskeyid']="STS.NUcGYtZZAJV5Y2pMsczebcB6r"
key['securitytoken']="CAISgwJ1q6Ft5B2yfSjIr5bWDOPAt4Vg/ZTeWxTBqXM2dupOjIedkDz2IHxFf3FoCOEYv/k1nWlU6/oTlqF/TIBDQUvNYZPfW1rifUXzDbDasumZsJYw6vT8a1fxZjf/2MjNGaCbKPrWZvaqbX3diyZ32sGUXD6+XlujQ+Dr6Zl8dYY4UxX6D1tBH8wEAgp5tI1gQhm3D/u2NQPwiWf9FVdhvhEG6Vly8qOi2MaRmHG85R/YsrZJ/tuvecD/MJI3Z8kvC4uPsbYoJvab4kl58ANX8ap6tqtA9Arcs8uVa1sruEnXaLKMo4wxfVIjP/FmRvIVtprnieY9tuiWkJ/s25qImF+BkY61GoABA+IHADC9Bm+Jm9j1wSu0KrewH07tWgCeA59Lvdl05ApG4kmeCIhnzf+X8YL9t6vU59skcLXhVdsu8zMVanhhvCUNZ+eQHiUbjXO8M7/u+9TnS3bLuP0eNS7ZXlhnqixqsq+3bmUHcc6AIFYJla+HeuVpb4A/XQr+UcmEaRivEAI="

endpoint = 'oss-cn-beijing.aliyuncs.com'
auth = oss2.StsAuth(key['accesskeyid'],key['accesskeysecret'],key['securitytoken'])

'''
先上传
'''
service = oss2.Service(auth, 'oss-cn-beijing.aliyuncs.com')
print([b.name for b in oss2.BucketIterator(service)])
bucket = oss2.Bucket(auth, endpoint, 'csdn-dl-data')
bucket.put_object('test.html', 'csdn-dl-data')

'''列文件'''
bucket = oss2.Bucket(auth, endpoint, 'sharedaka')
for obj in oss2.ObjectIterator(bucket,delimiter='/'):
	if obj.is_prefix():
		print ('directory:'+obj.key)
	else:
		print('file:'+obj.key)


exist = bucket.object_exists('test.html')
if exist:
	print u'bucket upload success'
else:
	print u'bucket upload fail'

'''
删除
'''

bucket.delete_object('test.html')
exist = bucket.object_exists('test.html')

if exist:
	print u'find test.html,can\'t del'
else:
	print u'del success!'