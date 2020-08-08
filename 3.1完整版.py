"""
    功能：爬取厦门人才网招聘信息
    版本：3.1完整版
    2.0优化功能：降低时间复杂度，缩短爬取时间O(n)toO(1)
    3.0新增优化功能：分三个程序同时运行，有效加快爬取速度，去除同个公司信息
    3.1减少单个程序工作量，避开更新网站信息时断开的情况
    时间：2020/6/18
    作者：山高水远
"""
import requests
from lxml import etree
import xlwt
import time


def main_url():
    res = requests.get('https://www.xmrc.com.cn/')
    return res


def get_company(pa):
    a = pa.xpath('//a[@target="_blank" and @onmouseout="hidetip()"]/text()')
    company_list = []
    for one in a:
        one = one.replace(' ', '')
        one = one.replace('\n', '')
        one = one.replace('\r', '')
        company_list.append(one)
    return company_list


def get_company_2(pa):
    res = requests.get('https://www.xmrc.com.cn')
    res.encoding = 'utf-8'
    pa = etree.HTML(res.text)
    a = pa.xpath('//div/div/a/@title')
    return a


def get_url(pa):
    a = pa.xpath('//a[@target="_blank" and @onmouseout="hidetip()"]/@href')
    url_list = []
    for one in a:
        new = 'https://www.xmrc.com.cn' + one
        url_list.append(new)
    return url_list


def pip_list_info_in_one(ccc_list):
    ccd_list = []

    it_len = len(ccc_list)
    c = ''
    while it_len >= 1:
        for every in ccc_list:
            it_len -= 1
            c = c + every

    if len(ccc_list) == 0:
        c = 'NO'
        ccd_list.append(c)

    ccd_list.append(c)

    ccd_list = list(set(ccd_list))
    return ccd_list


def pip_list(list_a):
    list_b = []
    for ONE in list_a:
        b = ONE[0]
        list_b.append(b)
    return list_b


def pip_phone_info(list_):
    l_list = []
    for ONE in list_:
        if ONE == '招聘联系电话：':
            pass
        elif ONE == '人事代理与档案及其他业务服务电话：12333':
            pass
        elif ONE == '联系电话：(合则约见、谢绝来电)':
            pass



        else:
            l_list.append(ONE)
    l_list = list(set(l_list))
    if len(l_list) == 0:
        l_list.append('NO')

    return l_list


def pip_str(a):
    cc_list = []
    for one in a:
        one = one.replace(' ', '')
        one = one.replace('\n', '')
        one = one.replace('\r', '')
        one = one.replace('\t', '')
        one = one.replace('xa0', '')
        one = one.replace('\xa0', '')
        one = one.replace('\u3000', '')
        one = one.replace('xa-1', '')
        one = one.replace('\u2999', '')
        cc_list.append(one)
    return cc_list


def get_phone(res_xpath):
    a = res_xpath.xpath('//td/text()')
    b = res_xpath.xpath('//p/text()')
    cc_list = pip_str(a)

    dd_list = pip_str(b)
    for i in dd_list:
        cc_list.append(i)

    none_list = []
    for one in cc_list:
        if len(one) <= 25:
            a = ['联系方式', '联系电话', '移动电话', '电话', ' 热线']
            for this in a:
                if this in one:
                    none_list.append(one)
                else:
                    pass

        else:
            pass
    if len(none_list) == 0:
        none_list.append('无')
    none_list = list(set(none_list))
    none_list = pip_phone_info(none_list)
    none_list = pip_list_info_in_one(none_list)
    return none_list


def pip_info(a):
    cc_list = pip_str(a)

    ccc_list = []
    for one in cc_list:
        a = ['联系人', 'hr', 'HR', '女士', '先生', '小姐', '经理']
        for b in a:
            if len(one) > 30:
                pass
            else:
                if b in one:
                    ccc_list.append(one)
                else:
                    pass

    ccc_list = list(set(ccc_list))
    ccd_list = pip_list_info_in_one(ccc_list)

    return ccd_list


def pip_no(list_):
    l_list = []
    for ONE in list_:
        if len(ONE) >= 5:
            ONE = ONE.replace('NO', '')
            l_list.append(ONE)
        else:
            l_list.append(ONE)

    return l_list


def get_name(res_xpath):
    a = res_xpath.xpath('//td/text()')
    b = res_xpath.xpath('//p/text()')

    table_name = pip_info(a)
    txt_name = pip_info(b)

    name_list = []
    for ONE in table_name:
        for one in txt_name:
            if one == ONE:
                name_list.append(one)
            else:
                n = one + ONE
                name_list.append(n)
    name_list = pip_no(name_list)

    return name_list


def get_address(res_xpath):
    a = res_xpath.xpath('*//td/text()')
    b = '联系地址'
    c = []
    for one in a:
        if b in one:
            c.append(one)
        else:
            pass
    if len(c) == 0:
        c.append('NO')

    a = pip_str(c)

    return a


def get_industry_info(res_xpath):
    a = res_xpath.xpath('*//td/text()')
    b = '公司行业'
    c = []
    for one in a:
        if b in one:
            c.append(one)
        else:
            pass
    if len(c) == 0:
        c.append('NO')

    a = pip_str(c)

    return a


def save(a, b, c, d, e, f, name):
    workbook = xlwt.Workbook(encoding=ascii)
    worksheet = workbook.add_sheet(name)
    worksheet.write(0, 0, 'Company')
    worksheet.write(0, 1, 'Phone')
    worksheet.write(0, 2, 'HR')
    worksheet.write(0, 3, 'Address')
    worksheet.write(0, 4, 'industry')
    worksheet.write(0, 5, 'url')
    for i in range(len(a)):
        worksheet.write(i + 1, 0, a[i])
        worksheet.write(i + 1, 1, b[i])
        worksheet.write(i + 1, 2, c[i])
        worksheet.write(i + 1, 3, d[i])
        worksheet.write(i + 1, 4, e[i])
        worksheet.write(i + 1, 5, f[i])

    workbook.save(name + '.xls')
    print('数据已写入Excel表。')


# 用于获取主文字的招聘信息
def main_1():
    res = main_url()
    res.encoding = 'utf-8'
    res_xpath = etree.HTML(res.text)

    print('正在获取首页文字区公司名称')

    company_list = get_company(res_xpath)
    print(company_list)
    print('公司数量', len(company_list))
    print('首页文字区公司名称已获取')

    print('正在获取首页文字区公司招聘信息页面网址')
    url_list = get_url(res_xpath)
    print(url_list)
    print('招聘详情页个数', len(url_list))
    print('首页文字区公司招聘信息网址已获取')

    print('正在获取文字区公司小哥哥小姐姐的联系电话')
    phone_list = []
    name_list = []
    address_list = []
    industry_list = []

    for one_page in url_list:
        res = requests.get(one_page)
        res.encoding = 'utf-8'
        res_xpath = etree.HTML(res.text)

        phone_list.append(get_phone(res_xpath))
        name_list.append(get_name(res_xpath))
        address_list.append(get_address(res_xpath))
        industry_list.append(get_industry_info(res_xpath))

    phone_list = pip_list(phone_list)
    name_list = pip_list(name_list)
    address_list = pip_list(address_list)
    industry_list = pip_list(industry_list)

    print(phone_list)
    print('联系方式数量', len(phone_list))
    print('首页文字区小哥哥小姐姐联系方式已获取完成')

    print('正在获取首页文字区公司小姐姐小哥哥的名字，请稍后')

    print(name_list)
    print('联系人数量', len(name_list))
    print('首页文字区小哥哥小姐姐的名字都获取到啦！')

    print('正在获取他们家的地址，憋住，别说话')

    print(address_list)
    print('地址数量', len(address_list))
    print('地址都获取到啦！')

    print('正在获取行业信息，憋住，别说话')

    print(industry_list)
    print('行业信息数量', len(industry_list))
    print('首页文字区公司行业信息都获取到啦！')

    print('正在写入数据')
    name = '首页文字区公司招聘信息'
    save(company_list, phone_list, name_list, address_list, industry_list, url_list, name)


# 上面为字体招聘信息
#######################################################################################################################
# 下面为图片招聘信息


def for_all_url(a):
    c = []
    b = 'http'
    for one in a:
        if b in one:
            pass
        else:
            one = 'https://www.xmrc.com.cn' + one
            c.append(one)
    return c


def main_2():
    res = main_url()
    res.encoding = 'utf-8'
    res_xpath = etree.HTML(res.text)

    company_list_2 = []
    url_list_2 = []
    print('正在获取首页图片区公司名称')
    ##############################
    # up,left,right三个页面
    # up
    a = res_xpath.xpath(
        '//div[@id="container"]/div[@id="goldIcon"]/div[@class="goldenButton_1"]/a[@target="_blank"]/@title')
    for one in a:
        company_list_2.append(one)

    a = res_xpath.xpath(
        '//div[@id="container"]/div[@id="goldIcon"]/div[@class="goldenButton_1"]/a[@target="_blank"]/@href')

    c = for_all_url(a)
    for one in c:
        url_list_2.append(one)

    # 左
    a = res_xpath.xpath(
        '//div[@id="container"]/div[@id="pageLeft"]/div[@class="companyIcon"]/div[@class="companyButton_1"]/a/@title')
    for one in a:
        company_list_2.append(one)
    a = res_xpath.xpath(
        '//div[@id="container"]/div[@id="pageLeft"]/div[@class="companyIcon"]/div[@class="companyButton_1"]/a/@href')
    c = for_all_url(a)
    for one in c:
        url_list_2.append(one)

    # 右
    a = res_xpath.xpath(
        '//div[@id="container"]/div[@id="pageRight"]/div[@class="companyIcon"]/div[@class="companyButton_1"]/a[@target="_blank"]/@title')
    for one in a:
        company_list_2.append(one)
    a = res_xpath.xpath(
        '//div[@id="container"]/div[@id="pageRight"]/div[@class="companyIcon"]/div[@class="companyButton_1"]/a[@target="_blank"]/@href')
    c = for_all_url(a)
    for one in c:
        url_list_2.append(one)

    print('公司数量', len(company_list_2))
    print('首页图片区公司名称已获取')
    print('详情页网址已获取')
    # print(company_list_2)
    # print(url_list_2)

    print('正在获取图片区公司小哥哥小姐姐的联系电话')
    phone_list_2 = []
    name_list_2 = []
    address_list_2 = []
    industry_list_2 = []

    for one_page in url_list_2:
        res = requests.get(one_page)
        res.encoding = 'utf-8'
        res_xpath = etree.HTML(res.text)

        phone_list_2.append(get_phone(res_xpath))
        name_list_2.append(get_name(res_xpath))
        address_list_2.append(get_address(res_xpath))
        industry_list_2.append(get_industry_info(res_xpath))

    phone_list_2 = pip_list(phone_list_2)
    name_list_2 = pip_list(name_list_2)
    address_list_2 = pip_list(address_list_2)
    industry_list_2 = pip_list(industry_list_2)

    print(phone_list_2)
    print('联系方式数量', len(phone_list_2))
    print('首页图片区公司联系方式已获取完成')

    print('正在获取金牌C站位公司小姐姐小哥哥的名字，请稍后')

    print(name_list_2)
    print('联系人数量', len(name_list_2))
    print('小哥哥小姐姐的名字都获取到啦！')

    print('正在获取他们家的地址，憋住，别说话')

    print(address_list_2)
    print('地址数量', len(address_list_2))
    print('地址都获取到啦！')

    print('正在获取行业信息，憋住，别说话')

    print(industry_list_2)
    print('行业信息数量', len(industry_list_2))
    print('行业信息都获取到啦！')

    print('正在写入数据')
    name = '图片区广告页面招聘公司信息'
    save(company_list_2, phone_list_2, name_list_2, address_list_2, industry_list_2, url_list_2, name)


def get_main_url():
    url = []
    # t = 'https://www.xmrc.com.cn/net/info/resultg.aspx?a=a&g=g&jobtype=&releaseTime=365&searchtype=1&keyword=&sortby=updatetime&ascdesc=Desc'
    for i in range(3100):
        if i == 0:
            pass
        #             i = ''
        #             c = t + i
        #             url.append(c)
        else:
            t = 'https://www.xmrc.com.cn/net/info/resultg.aspx?a=a&g=g&jobtype=&releaseTime=365&searchtype=1&keyword=&sortby=updatetime&ascdesc=Desc&PageIndex='
            c = t + str(i)
            url.append(c)
    return url


# 上面为首页招聘信息
#######################################################################################################################
# 下面为列表页招聘信息


def pip_all(a, b, h):
    A = []
    for i in range(h):
        print(i)
        if b[i] == 'NO':
            pass
        else:
            A.append(a[i])

    return A


def pip_same_company(company_list, list_):
    n = []
    num = 0
    for i in company_list:
        if num == 0:
            n.append(list_[num])
        else:
            if i != company_list[num-1]:
                n.append(list_[num])
            else:
                pass
        num = num + 1
    return n


def main_3():
    u = get_main_url()
    o = 1
    company_list_3 = []
    url_list_3 = []
    for one in u:
        try:
            o += 1
            if o % 50 == 0:
                print('第{}个列表页面已获取公司名和URL(提神醒脑线·······················································)'.format(o))
            if o % 70 == 0:
                print('==========================================故事的小黄花，从出生那年就飘着=========================快猜歌名呀===')
            if o % 500 == 0:
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~快说我是不是最棒最靓的仔·········')
                print('------------------------------------------------------------------bie_shuo_hua,kua_wo-----------')
            if o % 200 == 90:
                print('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\猜猜你的网速会让我跑多久//////////////////////////////////')
            print('正在获取公司名称+30')
            print('正在获取公司招聘页面详情网址+30')
            ##############################
            res = requests.get(one)
            res.encoding = 'utf-8'
            res_xpath = etree.HTML(res.text)

            a = res_xpath.xpath('//a[@class="a4 js_companyName"]/text()')
            b = res_xpath.xpath('//a[@class="a4 js_companyName"]/@href')

            a = pip_str(a)

            for one in a:
                company_list_3.append(one)

            c = for_all_url(b)
            for one in c:
                url_list_3.append(one)
        except:
            time.sleep(300)
            o += 1

    print('公司数量', len(company_list_3))
    print('公司名称已获取')
    print('招聘详情页网址已获取')

    print('正在获取公司小哥哥小姐姐的联系电话')
    print('获取电话中，请稍等')
    print('o。o')
    phone_list_3 = []
    name_list_3 = []
    address_list_3 = []
    industry_list_3 = []

    N = 1
    url_num = 0
    for one_page in url_list_3:
        url_num += 1
        onepage = one_page
        try:
            res = requests.get(url_list_3[url_num-1])
            res.encoding = 'utf-8'
            res_xpath = etree.HTML(res.text)

            N += 1
            if N % 50 == 0:
                print('第{}个公司已获取联系方式(动感光波提神·······················································)'.format(N))
                print('第{}个公司已获取名字(EVERY BODY 嗨起来·······················································)'.format(N))
                print('第{}个公司已获取公司名和URL(今夜我是DJ你会爱我吗·······················································)'.format(N))
                print('第{}个公司已获取行业信息。。。动次打次·······················································)'.format(N))

            phone_list_3.append(get_phone(res_xpath))
            name_list_3.append(get_name(res_xpath))
            address_list_3.append(get_address(res_xpath))
            industry_list_3.append(get_industry_info(res_xpath))

        except:
            time.sleep(300)

            phone_list_3.append(['NO'])
            name_list_3.append(['NO'])
            address_list_3.append(['NO'])
            industry_list_3.append(['NO'])

    phone_list_3 = pip_list(phone_list_3)
    name_list_3 = pip_list(name_list_3)
    address_list_3 = pip_list(address_list_3)
    industry_list_3 = pip_list(industry_list_3)

    print(company_list_3)
    print(url_list_3)

    print(phone_list_3)
    print('联系方式数量', len(phone_list_3))
    print('联系方式已获取完成')

    print(name_list_3)
    print('联系人数量', len(name_list_3))
    print('小哥哥小姐姐的名字都获取到啦！')

    print('正在获取他们家的地址，憋住，别说话')

    print(address_list_3)
    print('地址数量', len(address_list_3))
    print('地址都获取到啦！')

    print('正在获取行业信息，憋住，别说话')

    print(industry_list_3)
    print('行业信息数量', len(industry_list_3))
    print('行业信息都获取到啦！')

    print('正在写入数据')

    # name = '列表区招聘公司信息(all)'
    # save(company_list_3, phone_list_3, name_list_3, address_list_3, industry_list_3, url_list_3, name)

    # 去除无效信息
    h = len(phone_list_3)
    z = phone_list_3
    company_list_3 = pip_all(company_list_3, phone_list_3, h)
    phone_list_3 = pip_all(phone_list_3, z, h)
    name_list_3 = pip_all(name_list_3, z, h)
    address_list_3 = pip_all(address_list_3, z, h)
    industry_list_3 = pip_all(industry_list_3, z, h)
    url_list_3 = pip_all(url_list_3, z, h)

    c = company_list_3

    company_list_3 = pip_same_company(c, company_list_3)
    print(company_list_3)
    phone_list_3 = pip_same_company(c, phone_list_3)
    print(phone_list_3)
    name_list_3 = pip_same_company(c, name_list_3)
    print(name_list_3)
    address_list_3 = pip_same_company(c, address_list_3)
    print(address_list_3)
    industry_list_3 = pip_same_company(c, industry_list_3)
    print(industry_list_3)
    url_list_3 = pip_same_company(c, url_list_3)
    print(url_list_3)

    name = '列表页面3100页93000家公司'
    print('正在写入')
    save(company_list_3, phone_list_3, name_list_3, address_list_3, industry_list_3, url_list_3, name)


first_time = time.time()
time_start = time.time()
main_1()
time_end = time.time()
print('获取首页文字区信息时间', time_end-time_start, '秒')

time_start = time.time()
main_2()
time_end = time.time()
print('获取首页图片区信息时间', time_end-time_start, '秒')

time_start = time.time()
main_3()
time_end = time.time()
last_time = time.time()
print('获取列表区信息时间', time_end-time_start, '秒')
print('本次运行时间', last_time-first_time, '秒')

