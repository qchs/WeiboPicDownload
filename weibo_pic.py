from bs4 import BeautifulSoup
import requests,re,time

#home = 'http://weibo.cn/myhomedeco'
#home = 'http://weibo.cn/u/1989519725'
#home ='http://weibo.cn/williamchanwaiting'
#home='http://weibo.cn/u/5331615519'
# home = 'http://weibo.cn/CNpostoffice'

#folder='d:\黄景瑜\\'
#folder='d:\好好住\\'
#folder='d:\好好住指南\\'


def Soup(url):
    web = requests.get(url,headers = header)
    soup = BeautifulSoup(web.text,'lxml')
    return soup


def get_total_page(soup):
    page_tag  = soup.select('#pagelist > form > div > input[type="hidden"]')
    page = page_tag[0].get('value')
    print('Total page is  :'+ page)
    return int(page)

def is_set_pic(weibo_tag):
    set_pic_num  = re.findall('组图共(.*)张',str(weibo_tag)) #.*贪心算法,将括号内的内容以list类型返回
    return set_pic_num


def get_one_src(weibo_tag):#有的微博没有配图，有的微博转发时删除了
    pic_tag = weibo_tag.find_all('img','ib')
    if pic_tag:
        return   pic_tag[0].get('src').replace('wap180','large') #小图换成原图
    else:
        return []

def get_set_srcs(weibo_tag):
    url_tag = weibo_tag.div(href =re.compile('http://weibo.cn/mblog/picAll/'))  #获得组图链接的标签
    url = url_tag[0].get('href')#获得组图链接的地址
    soup = Soup(url)
    srcs =[]
    pics = soup('img')
    for pic in pics:
        src =pic.get('src').replace('thumb180','large')#小图换成原图
        srcs.append(src)
    return srcs

def get_one_page_pic_srcs(page):
    time.sleep(1)
    each_page_url = pic_home + '&page=%d'%page
    print('\nPage %d'%page +' url is: '+each_page_url)
    soup = Soup(each_page_url)
    weibo_div= soup(id = re.compile('M_'))#筛选出有微博的区域,list
    weibo_nums = len(weibo_div)#一页图片微博里，微博条数一般是10条，有时最后一页不定
    pic_srcs=[]
    for weibo in range(1,weibo_nums+1):#从当前页第一条微博的div标签开始，到最后一条微博
        weibo_tag = weibo_div[weibo-1]#tag属性，可以使用.find_all()
        has_set_pic = is_set_pic(weibo_tag)
        if has_set_pic:   #有组图时，进入组图链接，保存所有组图图片地址
            set_srcs = get_set_srcs(weibo_tag)
            for item in set_srcs:
                pic_srcs.append(item)
        else:         #没有组图时，微博可能有一张图片或是没有图片
            one_src = get_one_src(weibo_tag)
            if one_src:
                pic_srcs.append(one_src)
            else:
                None
    print('The total pic num of page %d'%page+' is %d'%len(pic_srcs)+'.')
    return pic_srcs

def download(page,all_pic_srcs):
    for each_src in all_pic_srcs:
        with open(folder + each_src[-10:],'wb') as f:
            r=requests.get(each_src)
            f.write(r.content)
            f.close()
    # print('page '+str(page) +' download '+str(len(all_pic_srcs))+' pics.')
'..................................................................'
home='http://weibo.cn/hu_ge'
header = {
    'Cookie':'??'
}
folder='d:\胡歌\\'


pic_home = home + '?filter=2'
soup =Soup(pic_home)
page = get_total_page(soup)
total_num = 0
time1 = time.time()
for each_page in range(1,3):
    all_pic_srcs = get_one_page_pic_srcs(each_page)
    num = len(all_pic_srcs)
    total_num = total_num+ num
    download(each_page,all_pic_srcs)
    print('目前已下载%d'%total_num+'张图片。')
time2 = time.time()
time = time2 - time1
print(time)
print('\n Total pic num of this ID is:%d'%total_num)
