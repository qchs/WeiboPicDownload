'''
1.未登录状态下打开微博，在Network里查看Doc ????
2.登录微博，在Doc里找到post,确定登陆的网址，还有post需提交的表单
Request URL:http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)

Form Data:
entry:weibo
gateway:1
from:
savestate:7
useticket:1
pagerefer:
vsnf:1
su:NzgwNzk0ODQ3JTQwcXEuY29t  加密的用户名
service:miniblog
servertime:1458514147  怎么获取？
nonce:INO2BJ  怎么获取？
pwencode:rsa2
rsakv:1330428213  怎么获取？
sp:abd9529bc5aa2ac7e0f2e2c4a5649d7759f36ba18c158fec22b33c588dccc4e7e9a4111bcea9f739fece06102fc6ad0e9c8659d6da24da89857b676a0a8c249acd597c6f3fc91227a232d52341585c3dbb51bffb72b57b9036821d4186996d521fe3f8d57bc8f94f8203c21029a8eec8ee2272f1b316432117377d5089e388e9
  加密的密码
sr:1600*900
encoding:UTF-8
prelt:68
url:http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack
returntype:META


3.未登录状态进入首页，在Network里的JS找到prologin,再输入用户名后点击登录（不要输入密码），此时在JS的最底端会有一个新的prologin，
打开这个新的prologin，里面的url打开，就可以找到post需提交的参数

Request URL:http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.18)&_=1458515996504
Request URL:http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=NzgwNzk0ODQ3JTQwcXEuY29t&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_=1458516105186

分析
entry:weibo
callback:sinaSSOController.preloginCallBack
su:
rsakt:mod
client:ssologin.js(v1.4.18)
_:1458515996504

entry:weibo
callback:sinaSSOController.preloginCallBack
su:NzgwNzk0ODQ3JTQwcXEuY29t  用户名被编码
rsakt:mod
checkpin:1  新增的
client:ssologin.js(v1.4.18)
_:1458516105186  server_time发生改变


'''
import base64,requests,time,rsa,binascii,re
from urllib.parse import quote_plus

def get_su(username):  #使用Base64解码用户名
    quote_s = quote_plus(username) # 780794847%40qq.com
    # print(quote_s)
    quote_b = quote_s.encode('utf-8')#b'780794847%40qq.com'
    # print(quote_b)
    base64_b = base64.b64encode(quote_b) #NzgwNzk0ODQ3JTQwcXEuY29t
    su_s = base64_b.decode('utf-8')
    # print('get_su(username) is %s'%su_s)#NzgwNzk0ODQ3JTQwcXEuY29t
    return  su_s

def get_data(su):
    # su = get_su(username)#开始还重复调用，浪费

    # http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=NzgwNzk0ODQ3JTQwcXEuY29t&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_=1458516105186
    # 构造这个url，预登陆时只输入用户名，在js里查看
    pre =  'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_='%su
    # print(pre)

    pre3 = pre+str(int(time.time() * 1000))
    # print(pre3)
    # print('pre3 is :%s'%pre3)
    data = s.get(pre3,headers = header)
    print('first cookie is:%s'%data.cookies)
    web = data.text
    # print(web)#sinaSSOController.preloginCallBack({"retcode":0,"servertime":1458556253,"pcid":"xd-f2dcfa807073c0707e3db29f3a5c27908c50","nonce":"QHKUMC",
    # "pubkey":"EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD399
    # 3CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928
    # EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443","rsakv":"1330428213","exectime":11})
    dict = eval(web.replace('sinaSSOController.preloginCallBack',''))
    # print(dict)#{'rsakv': '1330428213', 'servertime': 1458556253, 'nonce': 'QHKUMC', 'pubkey': 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D24
    # 5A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41
    # B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443', 'retcode': 0, 'pcid': 'xd-f2dcfa807073c0707e3db29f3a5c27908c50', 'exectime': 11}
    # print(type(dict)) #<class 'dict'>
    # print(len(dict['pubkey']))#256
    return dict

def get_sp(password,st,nonce,pubkey):
    # dict = get_data()#重复再次调用，时间其实是错的！
    # pubkey = dict['pubkey']
    # nonce = dict['nonce']
    # st = dict['servertime'] #开始用的systetime,错的
    rsakey = int(pubkey,16)
    # a = int('10001',16) #65537
    # print(rsakey,a)
    key = rsa.PublicKey(rsakey,65537)
    # print(key)
    message = str(st)+ '\t' +str(nonce)+ '\n'+password
    # print(message)
    message_b = message.encode('utf-8')
    # print(message_b)
    sp_b = rsa.encrypt(message_b,key)#加密
    # print(sp_b)
    sp_16 = binascii.b2a_hex(sp_b)
    # print(sp_16)
    return sp_16

def get_post_data(dict):
    st = dict['servertime']
    nonce = dict['nonce']
    rsakv = dict["rsakv"]
    pubkey = dict['pubkey']
    sp = get_sp(password,st,nonce,pubkey)
    post_data={
        'entry':'weibo',
        'gateway':'1',
        'from':'',
        'savestate':'7',
        'useticket':'1',
        'pagerefer':'http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl',
        'vsnf':'1',
        'su':su,
        'service':'miniblog',
        'servertime':st,
        'nonce':nonce,
        'pwencode':'rsa2',
        'rsakv':rsakv ,
        'sp':sp,
        'sr':'1366*768',
        'encoding':'UTF-8',
        'prelt':'115',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
       ' returntype':'META'
     }
    # print(post_data)
    return post_data  #这里居然都没有return


# if __name__ = '__main__':
username = '####'  #这个都能写错，我也是醉了
password = '####'
agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
header ={
    'User-Agent':agent
}
s = requests.session()
su = get_su(username)
dict = get_data(su) #在只输入用户名登录，JS里找到地址，构造后取得一些登录时需用到的参数
post=get_post_data(dict) #要一直print检查啊！！！！开始都没有返回值，构造登录时的表单


login_url ='http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'#正常登陆时在DOC里看到的
post_login =s.post(login_url,data = post,headers = header) #登录微博
# print(sign) #<Response [200]>
print('登录的网址l is: %s '%post_login.url)#sign.url is: http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)
# print(sign.encoding)
post_login.encoding ='gbk'
# print(sign.text)
'''
<title>新浪通行证</title>
<script charset="utf-8" src="http://i.sso.sina.com.cn/js/ssologin.js"></script>
</head>
<body>
正在登录 ...
<script>
{location.replace('http://passport.weibo.com/wbsso/login?ssosavestate=1490186002&url=http%3A%2F%2Fweibo.com%2Fajaxlogin.php%3Fframelogin%3D1%26callback%3Dparent
.sinaSSOController.feedBackUrlCallBack&ticket=ST-Mzg3NjQ4Njc0Nw==-1458650002-xd-59DB14C7CE7269AE82F0D4E24BC4736F&retcode=0');});}

'''
cook1 = post_login.cookies#post之后response中的cookies    <RequestsCookieJar
# [<Cookie ALC=ac%3D2%26bt%3D1458617387%26cv%3D5.0%26et%3D1490153387%26uid%3D3876486747%26vf%3D0%26vs%3D0%26vt%3D0%26es%3D18f
                # 9260654a9f580f8ff42bb1efb3eb8 for .login.sina.com.cn/>,
# <Cookie LT=1458617387 for .login.sina.com.cn/>,
# <Cookie tgc=TGT-Mzg3NjQ4Njc0Nw==-1458617387-xd-82BD9E1CCDEFD834DA66D73E393C9BE5 for .login.sina.com.cn/>,
# <Cookie ALF=1490153387 for .sina.com.cn/>,
# <Cookie SUB=_2A2579Mx7DeTxGeVG7FQV-CjLzzuIHXVYg7qzrDV_PUNbuNAPLVbekW9LHeucrU7d4bkF2E8pTglDKiROeF__bg.. for .sina.com.cn/>,
# <Cookie SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWhBT.mk9GzsK9zcsQ9G1YD for .sina.com.cn/>,这个是不变的
# <Cookie SUE=es%3D6f47ac7275f414cc128848948516f87b%26ev%3Dv1%26es2%3D910a22ca2ab45d6554341a8838a2810f%26rs0%3DejdBxZYcfqMpcHcOErHa0jzojaG%252BoWDiPE0NtSneIH4cs
                # nYVMZjbZFNx6crp3PvrUH2Di0%252FNMhlgl6g0VOcNhSbmmqAzdHfvF2L5IhJ%252BPAF2DPYJhZCp5bZFPnwqTTJ14VdYUjfA0%252FxS8PaoyUizfzy6a%252B6xL6qRkjFzC9i5t%252FI%253D%26rv%3D0 for .sina.com.cn/>,
# <Cookie SUP=cv%3D1%26bt%3D1458617387%26et%3D1458703787%26d%3D40c3%26i%3Daad0%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D2%26st%3D0%26lt%3D1%26uid%3D3876486747%26user%3D7
                # 80794847%2540qq.com%26ag%3D4%26name%3D780794847%2540qq.com%26nick%3D%25E5%25B1%25B1%25E5%25B1%25B1%25E6%25B0%25B4%25E6%25B0%25B4%25E5%259B%25AD%25E6%259E%2597%26
                # sex%3D%26ps%3D0%26email%3D%26dob%3D%26ln%3D780794847%2540qq.com%26os%3D%26fmp%3D%26lcp%3D2016-01-31%252017%253A53%253A32 for .sina.com.cn/>,
# <Cookie SUS=SID-3876486747-1458617387-XD-h7lnk-de9b429c7a99784b73a143f814e3aad0 for .sina.com.cn/>,
#  <Cookie sso_info=v02m6alo5qztKWRk5SlkKOEpZCjhKWRk5SlkKOEpZCjhKWRk5ilkKOApZCjkKWRk5ilkKOApZCjkKWRk5SljpSIpZCUkKWRk5iljpSUpY6TnKadlqWkj5OMuI2zmLSOg5i3jYOcwA== for .sina.com.cn/>]>
print('post之后response中的cookies is:%s'%cook1)
# print('sign.request.headers is %s'%sign.request.headers)


next_url = re.findall('location.replace(.*)' ,str(post_login.text))
q = next_url[0]
# print(q)
replace_url = re.findall('\'(.*?)\'',q)
print('location.replace url is :%s'%replace_url)
url = replace_url[0]#('http://passport.weibo.com/wbsso/login?ssosavestate=1490153471&url=http%3A%2F%2Fweibo.com%2Fajaxlogin.php%3Fframelogin%3D1%26callbac
# k%3Dparent.sinaSSOController.feedBackUrlCallBack&ticket=ST-Mzg3NjQ4Njc0Nw==-1458617471-xd-5385FB3BE1CC2410E1DC48D5AAD4472C&retcode=0');});}

ins = s.get(url,headers = header)
print(ins.text)#<html><head><script language='javascript'>parent.sinaSSOController.feedBackUrlCallBack({"result":true,"userinfo":
# {"uniqueid":"3876486747","userid":null,"displayname":null,"userdomain":"?wvr=5&lf=reg"}});</script></head><body></body></html>
cook2 = ins.cookies
print('secone get cookies is :%s'%cook2)#这些是不够的
# secone get cookies is :<RequestsCookieJar[<Cookie TC-Ugrow-G0=e66b2e50a7e7f417f6cc12eec600f517 for weibo.com/>]>

print(type(cook2))

url9 = 'http://weibo.com'#此时的跳转地址为http://weibo.com/u/3876486747/home?wvr=5
webs = s.get(url9)
print('finally the url is: %s'%webs.url)
my_cookies =webs.cookies
print(my_cookies)#<RequestsCookieJar[<Cookie wvr=6 for .weibo.com/>, <Cookie TC-V5-G0=7e5b74ea4beaaa98b5f592db11c2eeb9 for weibo.com/>]>
# print(webs.text)
#
home = 'http://weibo.cn/myhomedeco'
h = requests.get(home,cookies = my_cookies)#试试加上headers,再试试用.join()把所有获得的cookies合并到一起
print('home url is: %s'%h.url)
print(h.text)#还是没登陆上
# print(web.encoding)
# web.encoding = 'utf-8'
# print(web.text)
# # print(web2.content.decode('gb2312'))

