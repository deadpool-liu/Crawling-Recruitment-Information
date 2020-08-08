import requests
from lxml import etree
import re
import xlwt
import time

# 获取列表页面
def get_main_url_1():
    page_url = []
    for i in range(88):
        if i == 0:
            pass
        else:
            url = 'http://www.yingjiesheng.com/xiamenjob/list_' + str(i) + '.html'
            #             print(url)
            page_url.append(url)
    return page_url

# 去除相同信息：
def pip_same(list):
    # list = [11,22,33,22,44,33]
    lis = []                          #创建一个新列表
    for i in list:                    #循环list里的每一个元素
        if i in lis:
            pass
            #判断元素是否存在新列表中，不存在则添加，存在则跳过，以此去重
        else:
            lis.append(i)
    return lis

# 改变指针
def change_list(list):
    li = []
    for i in list:
        li.append(i)
    return li
# 获取列表页面能够看到的信息
def get_main_info(main_url):
    company_list = []
    job_name_list = []
    address_list = []
    info_come_from_list = []
    out_date_list = []
    url_list = []

    n = 0
    for one_page in main_url:
        print(one_page)
        n += 1
        print(n)
        if n % 2 == 0:
            print('伪装浏览中，5秒')
            time.sleep(5)
        res = requests.get(one_page)
        res.encoding = 'gbk'
        res_xpath = etree.HTML(res.text)
        company = res_xpath.xpath('//tr[@class="jobli"]/td[@width="329"]/a[@target="_blank"]/text()')
        #         company = res_xpath.xpath('//div[@class="wrap"]/div[@class="job"]/div[@class="jobdiv"]/table[@id="tb_job_list"]/tbody/tr[@class="jobli"]/td[@width="329"]/a[@target="_blank"]/text()')

        job_name = res_xpath.xpath('//tr[@class="jobli"]/td[@width="253"]/a[@target="_blank"]/text()')

        address = res_xpath.xpath('//tr[@class="jobli"]/td[@width="152"]/span/text()')

        info_come_from = res_xpath.xpath('//tr[@class="jobli"]/td[@width="155"]/span/text()')

        out_date = res_xpath.xpath('//tr[@class="jobli"]/td[@width="92"]/span/text()')

        c_url = res_xpath.xpath('//tr[@class="jobli"]/td[@width="329"]/a[@target="_blank"]/@href')

        for one in company:
            company_list.append(one)
        for one in job_name:
            job_name_list.append(one)
        for one in address:
            address_list.append(one)
        for one in info_come_from:
            info_come_from_list.append(one)
        for one in out_date:
            out_date_list.append(one)
        for one in c_url:
            if 'http' in one:
                url_list.append(one)
            else:
                a = 'http://www.yingjiesheng.com' + one
                url_list.append(a)

        print(len(company_list))
        #         print(company_list)
        print(len(job_name_list))
        #         print(job_name_list)
        print(len(address_list))
        #         print(address_list)
        print(len(info_come_from_list))
        #         print(info_come_from_list)
        print(len(out_date_list))
        #         print(out_date_list)
        print(len(url_list))
    #         print(url_list)
    z = []
    z.append(company_list)
    z.append(job_name_list)
    z.append(address_list)
    z.append(info_come_from_list)
    z.append(out_date_list)
    z.append(url_list)

    return z

# 判断获取的字符串中是否含有数字
def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))

# 查看带数字的字符串的数字长度，并返回10位数字以上的字符串列表
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
            if len(new_num) >= 10:
                c.append(i)
    if len(c) == 0:
        c.append('NO')
    return c

# 去除多余符号
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
        one = one.replace('/', '')
        one = one.replace(',', '')
        one = one.replace('、', '')
        one = one.replace('；', '')

        cc_list.append(one)
    return cc_list

def new_pip_list(lis):
    n_list = []
    lis_ = list(lis)
    print('函数list后', lis_)
    n = ''
    for one in lis_:
        n += '【' + one + '】'
    n_list.append(n)

    print('piplist操作后', n_list)
    return n_list



# 将一个列表中的多个元素合并成一个长字符，并用【】分隔保存
def pip_list(lists):
    print('操作前')
    print(lists)
    n_list = []
    if len(lists) == 1:
        n_list.append(lists[0])
    else:
        n = ''
        for one in lists:
            n += '【' + one + '】'
        n_list.append(n)
    print('操作后', n_list)
    return n_list

# 根据电话号码判断是否保存该条信息
def pip_all(a, b, h):
    A = []
    for i in range(h):
        print(i)
        if b[i] == ['【NO】']:
            pass
        else:
            A.append(a[i])

    return A

# 保存信息至Excel
def save(a, b, c, d, e, f, g, h, I, name):
    workbook = xlwt.Workbook(encoding=ascii)
    worksheet = workbook.add_sheet(name)
    worksheet.write(0, 0, 'Company')
    worksheet.write(0, 1, 'Phone')
    worksheet.write(0, 2, 'Name')
    worksheet.write(0, 3, 'Job_name')
    worksheet.write(0, 4, 'Major')
    worksheet.write(0, 5, 'Address')
    worksheet.write(0, 6, 'Info_come_from')
    worksheet.write(0, 7, 'Out_date')
    worksheet.write(0, 8, 'Url')

    for i in range(len(b)):
        worksheet.write(i + 1, 0, a[i])
        worksheet.write(i + 1, 1, b[i])
        worksheet.write(i + 1, 2, c[i])
        worksheet.write(i + 1, 3, d[i])
        worksheet.write(i + 1, 4, e[i])
        worksheet.write(i + 1, 5, f[i])
        worksheet.write(i + 1, 6, g[i])
        worksheet.write(i + 1, 7, h[i])
        worksheet.write(i + 1, 8, I[i])
    workbook.save(name + '.xls')
    print('实习数据已写入Excel表。')

# 主函数
def main():
    main_url = get_main_url_1()
    z = get_main_info(main_url)
    #     获取联系方式和称呼
    name_list = []
    phone_list = []
    major_list = []
    c = z[5]
    count = 0
    for i in c:
        has_num_list = []
        has_name_list = []
        has_major_list = []
        count += 1
        if count % 60 == 0:
            print('已获取60个公司信息，伪装中，需60秒')
            time.sleep(60)

        try:
            print(i)
            res = requests.get(i)
            res.encoding = 'gbk'
            res_xpath = etree.HTML(res.text)
            print('网页已被浏览')
#######################################################################################################################
            #         for_phone = res_xpath.xpath('//div[@id="wrap"]/div[@id="container"]/div[@class="main mleft"]/div[@id="wordDiv"]/div[@class="job"]/div[@class="jobIntro"]/div[@frag="窗口5"]/div[@class="wp_articlecontent"]/p/p/text()')
            for_phone = res_xpath.xpath('//p/text()')
            #         第一次框架
            for one in for_phone:
                if hasNumbers(one):
                    if 40 >= len(one) >= 11:
                        if '时间' not in one:
                            if '备案' not in one:
                                if '月' not in one:
                                    if '2020' not in one:
                                        if '0000' not in one:
                                            if '2019' not in one:
                                                has_num_list.append(one)

            for_name = for_phone
            usual_name = ['经理', '小姐', '女士', '先生', '总管', '老师']
            for one in for_name:
                if len(one) <= 8:
                    for i in usual_name:
                        if i in one:
                            if '→' not in one:
                                has_name_list.append(one)

            usual_major = ['电子', '数学', '媒体', '新闻', '专业', '科学', '生物', '学科', '学历', '管理', '计算机', '材料',
                           '化学', '制药', '金融', '机械', '物流', '工程', '类', '贸易', '文学', '会计', '英', '语', '艺术']
            # for one in for_major:
            #     if len(one) <= 8:
            #         for i in usual_major:
            #             if i in one:
            #                 has_major_list.append(one)
            # num_1 = 0
            # for i in for_major:
            #     if '专业' in i:
            #         if len(for_major[num_1+1]) <= 8:
            #             has_major_list.append(for_major[num_1+1])
            #         if len(for_major[num_1+2]) <= 8:
            #             has_major_list.append(for_major[num_1+2])
            #     num_1 += 1


            has_num_list = num_long(has_num_list)

########################################################################################################################
                    # 第二次框架
            if has_num_list == ['NO']:
                has_num_list = []
                has_name_list = []
                for_phone = res_xpath.xpath('//span/text()')
                for one in for_phone:
                    if hasNumbers(one):
                        if 40 >= len(one) >= 11:
                            if '时间' not in one:
                                if '备案' not in one:
                                    if '月' not in one:
                                        if '2020' not in one:
                                            if '0000' not in one:
                                                if '2019' not in one:
                                                    has_num_list.append(one)
                has_num_list = num_long(has_num_list)

                for_name = for_phone
                for one in for_name:
                    if len(one) <= 8:
                        for i in usual_name:
                            if i in one:
                                if '→' not in one:
                                    has_name_list.append(one)

            # for_major = res_xpath.xpath('//span/text()')
            # # usual_major = ['专业']
            # for one in for_major:
            #     if len(one) <= 8:
            #         for i in usual_major:
            #             if i in one:
            #                 has_major_list.append(one)
            # num_1 = 0
            # for i in for_major:
            #     if '专业' in i:
            #         if len(for_major[num_1+1]) <= 8:
            #             has_major_list.append(for_major[num_1+1])
            #         if len(for_major[num_1+2]) <= 8:
            #             has_major_list.append(for_major[num_1+2])
            #     num_1 += 1

###############################################################################################################################
                # print('第二次框架')
            #         第三次框架
            if has_num_list == ['NO']:
                has_num_list = []
                has_name_list = []
                for_phone = res_xpath.xpath('//div//div//div/div/text()')
                for one in for_phone:
                    if hasNumbers(one):
                        if 40 >= len(one) >= 11:
                            if '时间' not in one:
                                if '备案' not in one:
                                    if '月' not in one:
                                        if '2020' not in one:
                                            if '0000' not in one:
                                                if '2019' not in one:
                                                    has_num_list.append(one)
                has_num_list = num_long(has_num_list)


                for_name = for_phone
                for one in for_name:
                    if len(one) <= 8:
                        for i in usual_name:
                            if i in one:
                                if '→' not in one:
                                    has_name_list.append(one)

            for_major = res_xpath.xpath('//div//div//div/div//a/text()')
            # usual_major = ['专业']
            for one in for_major:
                if len(one) <= 8:
                    for i in usual_major:
                        if i in one:
                            print('这是即将写入的专业', one)
                            has_major_list.append(one)
            # num_1 = 0
            # for i in for_major:
            #     if '专业' in i:
            #         if len(for_major[num_1 + 1]) <= 8:
            #             has_major_list.append(for_major[num_1 + 1])
            #         if len(for_major[num_1 + 2]) <= 8:
            #             has_major_list.append(for_major[num_1 + 2])
            #     num_1 += 1

                # print('第三次框架')

            has_num_list_ = pip_str(has_num_list)
            print('set去重前', has_num_list_)
            has_num_list_11 = list(set(has_num_list_)).copy()
            print('set去重后', has_num_list_11)
            has_num_list_1 = pip_same(has_num_list_11).copy()
            print('pip去重后', has_num_list_1)
            if len(has_num_list_1) > 5:
                print('已取前5')
                has_num_list_111 = has_num_list_1
                has_num_list_1_ = has_num_list_111.copy()
                print('取前五后', has_num_list_1_)
            else:
                print('取所有')
                has_num_list_1_ = has_num_list_1.copy()
                print('取所有后', has_num_list_1_)
            has_num_list_1_1 = []
            for he in has_num_list_1_:
                has_num_list_1_1.append(he)
            print('重新写入后', has_num_list_1_1)
            # has_num_list_1_1_ = new_pip_list(has_num_list_1_1).copy()
            this = 0
            has_num_list_1_11 = []
            while this <len(has_num_list_1_1):
                has_num_list_1_11.append(has_num_list_1_1[this])
                this += 1
            print('while后', has_num_list_1_1)
            has__num = list(has_num_list_1_1)
            has_num_list_1_1_ = list(new_pip_list(has__num))


            print('去列表复制后', has_num_list_1_1_)
            phone_list.append(has_num_list_1_1_)


            has_name_list_ = pip_str(has_name_list)
            if len(has_name_list_) == 0:
                has_name_list_.append('NO')
            has_name_list_1 = pip_same(has_name_list_).copy()
            print('已去重')

            print(len(has_name_list_1))
            # if len(has_name_list_1) > 5:
            #     print('已取前5')
            #     has_name_list_1 = has_name_list_1[0:5]
            has_name_list_1_ = pip_list(has_name_list_1).copy()
            name_list.append(has_name_list_1_)


            has_major_list = pip_str(has_major_list)

            print('去重前', has_major_list)
            li = list(set(has_major_list)).copy()
            if len(li) == 0:
                li.append('NO')

            print('去重后', li)
            print(len(li))
            if len(li) > 6:
                print('已取前5')
                # lis = li[0:6]
            print('here')
            lis = li.copy()
            lis = pip_list(lis)
            list_ = lis.copy()
            # print(has_major_list)
            print('here2')
            major_list.append(list_)

            print('这是再现身一次')
            print(has_num_list_1_1_)
            print(has_name_list_1_)
            print(list_)
        except:
            print('网络不稳定，等待中')
            time.sleep(300)
            name_list.append('NO')
            phone_list.append('NO')
            major_list.append('NO')

    print(phone_list)
    print(name_list)
    print(major_list)

    company_list = z[0]
    phone_list = phone_list
    name_list = name_list
    job_name_list = z[1]
    address_list = z[2]
    info_come_from_list = z[3]
    out_date_list = z[4]
    url_list = z[5]

    # 塞选有联系方式的公司
    h = len(phone_list)
    z = phone_list
    company_list = pip_all(company_list, z, h)
    phone_list = pip_all(phone_list, z, h)
    name_list = pip_all(name_list, z, h)
    job_name_list = pip_all(job_name_list, z, h)
    major_list = pip_all(major_list, z, h)
    address_list = pip_all(address_list, z, h)
    info_come_from_list = pip_all(info_come_from_list, z, h)
    out_date_list = pip_all(out_date_list, z, h)
    url_list = pip_all(url_list, z, h)
    name = '应届生求职网招聘信息'

    #     z.append(company_list)
    #     z.append(job_name_list)
    #     z.append(address_list)
    #     z.append(info_come_from_list)
    #     z.append(out_date_list)
    #     z.append(url_list)

    save(company_list, phone_list, name_list, job_name_list, major_list, address_list, info_come_from_list, out_date_list, url_list,
         name)
    print('已完成')

# def a():
#     c = ['1','2','3']
#     c = c[-2:]
#     return c


if __name__ == '__main__':
    main()
    # z = ['赣州', '赣州', '江西']
    # z = pip_same(z)
    # print(z)


# l = []
# for i in range(15):
#     l.append(i)
# if len(l) >=10:
#     l = l[0:5]
# print(l)


# m = ['我', '你', '他', '他', '15727787348', '15727787348']
# m = list(set(m))
# print(m)