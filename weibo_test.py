'''
1.未登录状态下打开微博，在Network里查看Doc
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
pwencode:rsa2  怎么获取？
rsakv:1330428213  怎么获取？
sp:abd9529bc5aa2ac7e0f2e2c4a5649d7759f36ba18c158fec22b33c588dccc4e7e9a4111bcea9f739fece06102fc6ad0e9c8659d6da24da89857b676a0a8c249acd597c6f3fc91227a232d52341585c3dbb51bffb72b57b9036821d4186996d521fe3f8d57bc8f94f8203c21029a8eec8ee2272f1b316432117377d5089e388e9
  加密的密码
sr:1600*900
encoding:UTF-8
prelt:68
url:http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack
returntype:META


3.未登录状态进入首页，在Network里的JS找到prologin,再输入用户名后点击登录（不要输入密码），此时在JS的最底端会有一个新的prologin，
打开这个新的飘柔login，里面的url打开，就可以找到post需提交的参数

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
su:NzgwNzk0ODQ3JTQwcXEuY29t  用户名被加密
rsakt:mod
checkpin:1  新增的
client:ssologin.js(v1.4.18)
_:1458516105186  server_time发生改变


'''



import requests

u= 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=NzgwNzk0ODQ3JTQwcXEuY29t&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_=1458516105186'
r = requests.get(u)
print(r) #<Response [200]>
print(r.text)#sinaSSOController.preloginCallBack(
# {"retcode":0,
# "servertime":1458517276,服务器时间，用来与用户密码一起扰乱加密
# "pcid":"xd-40c537f3f0a48b3bfe87adedcde3d0dc65b8",
# "nonce":"CL80NS",服务器随机字符串，用来与用户密码一起扰乱加密
# "pubkey":"EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443",
# 客户端使用RSA加密的公钥
# "rsakv":"1330428213",
# "is_openlock":0,
# "showpin":0,
# "exectime":10})
