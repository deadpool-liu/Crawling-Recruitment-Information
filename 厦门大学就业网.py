"""
    功能：获取厦门大学就业网上的招聘信息
    版本：1.0
    时间：2020/6/16
    作者：山高水远
"""
import requests
from lxml import etree
import re
import xlwt


def get_main_url_1():
    page_url = []
    for i in range(9):
        if i == 0:
            pass
        else:
            url = 'https://jyzd.xmu.edu.cn/wxwsxxx/list' + str(i) + '.htm'
            page_url.append(url)
    return page_url


def get_main_url_2():
    page_url = []
    for i in range(281):
        if i <= 1:
            pass
        else:
            url = 'https://jyzd.xmu.edu.cn/wxwxqxx/list' + str(i) + '.htm'
            page_url.append(url)
    return page_url


def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))


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
        one = one.replace('【', '')
        one = one.replace('】', '')
        one = one.replace('：', '')
        one = one.replace(':', '')
        cc_list.append(one)
    return cc_list


def num_long(list):
    c = []

    if len(list) == 0:
        c.append('NO')
    else:
        for i in list:
            new_num = ''
            n = re.findall(r'[1-9]+\.?[0-9]*', i)
            for one in n:
                new_num += one
            if len(new_num) >= 9:
                c.append(i)
    if len(c) == 0:
        c.append('NO')
    return c


def pip_list(lists):
    n_list = []
    for one_list in lists:
        if len(one_list) == 1:
            n_list.append(one_list[0])
        else:
            one_list = list(set(one_list))
            n = ''
            for i in one_list:
                n += n + '【' + i + '】'
            n_list.append(n)
    return n_list


def pip_in_one(lists):
    n_list = []
    if len(lists) == 1:
        n_list.append(lists[0])
    # 太多只取两位
    else:
        n = ''
        for i in lists:
            n = n + '【'+i+'】'
        n_list.append(n)
    return n_list


def pip_all(a, b, h):
    A = []
    for i in range(h):
        print(i)
        if b[i] == 'NO':
            pass
        else:
            A.append(a[i])

    return A


def save(a, b, c, d, name):
    workbook = xlwt.Workbook(encoding=ascii)
    worksheet = workbook.add_sheet(name)
    worksheet.write(0, 0, 'Company')
    worksheet.write(0, 1, 'Phone')
    worksheet.write(0, 2, 'name')
    worksheet.write(0, 3, 'url')

    for i in range(len(b)):
        worksheet.write(i + 1, 0, a[i])
        worksheet.write(i + 1, 1, b[i])
        worksheet.write(i + 1, 2, c[i])
        worksheet.write(i + 1, 3, d[i])

    workbook.save(name + '.xls')
    print('实习数据已写入Excel表。')


def main_1():
    page_url = get_main_url_1()
    company_list_1 = []
    company_url_list_1 = []
    for every in page_url:
        res = requests.get(every)
        res.encoding = 'utf-8'
        res_xpath = etree.HTML(res.text)
        company = res_xpath.xpath('//a[@target="_blank"]/text()')
        for one in company:
            company_list_1.append(one)

        url = res_xpath.xpath('//a[@target="_blank"]/@href')
        for one in url:
            #           去除首页和特殊页面招聘
            if len(one) == 33:
                a_url = 'https://jyzd.xmu.edu.cn' + one
                if a_url == 'https://jyzd.xmu.edu.cn/2020/0422/c18714a400132/page.htm':
                    pass
                else:
                    company_url_list_1.append(a_url)

    print('实习公司名称已获取')
    print(len(company_list_1))
    print('实习公司具体招聘网址已获取')
    print(len(company_url_list_1))
    print(company_url_list_1)

    print('正在获取具体页面的联系方式和联系人')
    phone_list_1 = []
    name_list_1 = []
    for i in company_url_list_1:
        # 联系方式
        has_num_list = []
        res = requests.get(i)
        res.encoding = 'utf-8'
        res_xpath = etree.HTML(res.text)
        info = res_xpath.xpath('//div[@id="container"]/div/div//p//span/text()')

        for one in info:
            if hasNumbers(one):
                if 23 >= len(one) >= 10:
                    if '时间' not in one:
                        has_num_list.append(one)

        has_num_list = pip_str(has_num_list)
        num_list = num_long(has_num_list)
        # num_list = list(set(num_list))
        phone_list_1.append(num_list)

        # 联系人
        usual_name = ['小姐', '先生', '经理', '主管', '秘书', '电话']
        name = []
        for one in info:
            if len(one) <= 23:
                for h in usual_name:
                    if h in one:
                        name.append(one)
        if len(name) == 0:
            name.append('NO')
        # name = list(set(name))
        name_list_1.append(name)

    phone_list_1 = pip_list(phone_list_1)
    name_list_1 = pip_list(name_list_1)

    print('联系方式已获取')
    print(len(phone_list_1))
    print(phone_list_1)
    print('称呼已获取')
    print(len(name_list_1))
    print(name_list_1)

    name = '厦门大学实习招聘信息'
    save(company_list_1, phone_list_1, name_list_1, company_url_list_1, name)


def main_2():
    print('正在获取公司名称')
    print('共280个列表页')
    page_url = get_main_url_2()
    company_list_2 = []
    company_url_list_2 = []
    z = 0
    for every in page_url:
        z += 1
        print(z)
        res = requests.get(every)
        res.encoding = 'utf-8'
        res_xpath = etree.HTML(res.text)
        company = res_xpath.xpath('//a[@target="_blank"]/text()')
        new_company_list = []
        new_url_list = []
        for one in company:
            new_company_list.append(one)
        #             company_list_2.append(one)

        url = res_xpath.xpath('//a[@target="_blank"]/@href')
        for one in url:
            #           去除首页和特殊页面招聘
            if len(one) == 33:
                a_url = 'https://jyzd.xmu.edu.cn' + one
                #                 过滤垃圾网址
                n = 0

                if a_url == 'https://jyzd.xmu.edu.cn/2020/0422/c18714a400132/page.htm':
                    n += 1
                if a_url == 'https://jyzd.xmu.edu.cn/2020/0423/c18713a400152/page.htm':
                    n += 1

                if n == 0:
                    new_url_list.append(a_url)
        #                     company_url_list_2.append(a_url)

        if len(new_company_list) == len(new_url_list):
            for i in new_company_list:
                company_list_2.append(i)
            for i in new_url_list:
                company_url_list_2.append(i)

    print('实习公司名称已获取')
    print(len(company_list_2))
    #     print(company_list_2)
    print('实习公司具体招聘网址已获取')
    print(len(company_url_list_2))
    #     print(company_url_list_2)

    print('正在获取具体页面的联系方式和联系人')
    phone_list_2 = []
    name_list_2 = []
    print('共计', len(company_url_list_2), '个网页')
    z = 0
    for i in company_url_list_2:
        z += 1
        print(z)
        # 联系方式
        has_num_list = []
        res = requests.get(i)
        res.encoding = 'utf-8'
        res_xpath = etree.HTML(res.text)
        info = res_xpath.xpath('//div[@id="container"]/div/div//p//span/text()')

        for one in info:
            if hasNumbers(one):
                if 23 >= len(one) >= 10:
                    if '时间' not in one:
                        if '@' not in one:
                            has_num_list.append(one)

        has_num_list = pip_str(has_num_list)
        num_list = num_long(has_num_list)
        num_list = list(set(num_list))
        print(num_list)
        num_list = pip_in_one(num_list)
        phone_list_2.append(num_list)

        # 联系人
        usual_name = ['小姐', '先生', '经理', '主管', '秘书', '电话']
        name = []
        for one in info:
            if len(one) <= 23:
                for h in usual_name:
                    if h in one:
                        name.append(one)
        if len(name) == 0:
            name.append('NO')
        name = list(set(name))
        print(name)
        name = pip_in_one(name)
        name_list_2.append(name)

    phone_list_2 = pip_list(phone_list_2)
    name_list_2 = pip_list(name_list_2)

    # 塞选有联系方式的公司
    h = len(phone_list_2)
    z = phone_list_2
    company_list_2 = pip_all(company_list_2, phone_list_2, h)
    phone_list_2 = pip_all(phone_list_2, z, h)
    name_list_2 = pip_all(name_list_2, z, h)
    company_url_list_2 = pip_all(company_url_list_2, z, h)


    print('联系方式已获取')
    print(len(phone_list_2))
    print(phone_list_2)
    print('称呼已获取')
    print(len(name_list_2))
    print(name_list_2)

    name = '厦门大学需求招聘信息'

    save(company_list_2, phone_list_2, name_list_2, company_url_list_2, name)
    print('已完成')


if __name__ == '__main__':
    # main_1()
    main_2()
