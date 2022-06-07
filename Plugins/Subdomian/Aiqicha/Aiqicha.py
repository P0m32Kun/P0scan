# -*- coding: utf-8 -*-
import json
import re

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://aiqicha.baidu.com/',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'BAIDUID_BFESS=9B3B2A04BCAF3F00A1749A28EE79A301:FG=1; log_guid=7e65c373969e102f1328a2d7784761ae; _j47_ka8_=57; BAIDUID=F43177C434B64D167BDC8D0BE5F0F64F:FG=1; BDUSS=H5DTDhreUt4Qm9jQ1VteG5EbVd-dHh4R2VubnM1Vm9ZU0t3a35pQUlLOVZyNzlpSVFBQUFBJCQAAAAAAAAAAAEAAAAX8IQhscuwtuzh1OHA4QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFUimGJVIphid; BDUSS_BFESS=H5DTDhreUt4Qm9jQ1VteG5EbVd-dHh4R2VubnM1Vm9ZU0t3a35pQUlLOVZyNzlpSVFBQUFBJCQAAAAAAAAAAAEAAAAX8IQhscuwtuzh1OHA4QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFUimGJVIphid; BDPPN=f20be85e1dd6a0d72fd8797a5a9273b5; _t4z_qc8_=xlTM-TogKuTwheiv5Kf8lQwu9RDjERlFKAmd; ab165413520=262ca04b22da7de933251a28691da75016541374429f5; _s53_d91_=b5e26c8e8effdf053fb0a47a94148130c3f0ae823babd8ddf87fe9c3d20e7601a350bee4dff0d12a15d7848432762bc4e95b6b5dd9e15a5a3ad470ef3dfb3c1b9bc4df8652d23954881a4c7b8ed4af229d958ab9e99a3a8e7fe976a738f1c10d97863be8359557048cae2b0d6dcf58cb01ee9e609373f45b683a166cf6fa92e224016078ae2acfebf9f2e22bdf3d0e9692630e4468d9f232e41b6a3b408394f6a7d7f22f27f73a9fc1a3bee17867284237fa367ce76bccf30f2692166ceef9f52f8e55b79d0de4a92c854bba63e90893; _y18_s21_=394e3085; ab_sr=1.0.1_NmNjMGUzNmJjMGFmYTM1Zjc4MjA0ZWMwYzZlMmZjM2Q3MGY3Y2FlMjIzYjM0NTQxY2I0YmEwM2ZhNTRmYmMyMTA4NWM5MmJmOWUyOTg3NGVkYjlhMzE2ZjMzOWE0OWM1N2VlODZkOTVlMWJmNjFmM2FhYzc0ZTkyMGQ0ZWExN2IyZTQ4MzE5MGFkZjNlYmYyNDMwMjFhMzVmMzE5MWRiNThlNGQ1MGQ4NGUzZjFmMDk0YTNkM2VkZTg0Yzk3Zjc2; RT="z=1&dm=baidu.com&si=pzcfdkgzbt&ss=l3wep8qg&sl=8&tt=5y7&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=w1r&ul=1hv7"',
}

requests_proxies = None

# 网站备案的细节
icpinfo_url = "https://aiqicha.baidu.com/detail/icpinfoajax?p=1&size=20&pid=111111111111"
# 对外投资的细节
invest_url = "https://aiqicha.baidu.com/detail/investajax?p=1&size=20&pid=111111111111"
# 控股企业的细节
hold_url = "https://aiqicha.baidu.com/detail/holdajax?p=1&size=20&pid=111111111111"
# 分支机构的细节
branch_url = "https://aiqicha.baidu.com/detail/branchajax?p=1&size=20&pid=111111111111"

# 每页的条数
size = 10
# 超时
TIMEOUT = 20

invest_infos = []
holds_infos = []
branch_infos = []


# 获取基本信息:公司名、邮箱地址、联系方式
def companyDetail(pid):
    companyDetail_infos = {"emails": "", "telephone": ""}
    try:
        url = "https://aiqicha.baidu.com/company_detail_{}".format(pid)
        res = requests.get(url=url, headers=headers, proxies=requests_proxies, verify=False, timeout=TIMEOUT)
        text = res.text
        # print(text)
        # companyName = re.findall('entName":"(.*?)"', text)[0].encode('utf-8').decode('unicode_escape')
        emails = re.findall(r'email":"(.*?)"', text)
        telephone = re.findall('telephone":"(.*?)"', text)
        # print("公司名、邮箱地址、联系方式")
        # print(companyName[0].encode('utf-8').decode('unicode_escape'), emails, telephone)
        companyDetail_infos = {"emails": emails, "telephone": telephone}
    except Exception as e:
        # print(e.args)
        pass
    # print()
    return companyDetail_infos


# 网站备案信息
def icpinfo(pid, icpinfo_page):
    icpinfo_infos = []
    for i in range(1, icpinfo_page + 1):
        try:
            invest_url = "https://aiqicha.baidu.com/detail/icpinfoajax?p={}&size={}&pid={}".format(i, size, pid)
            res = requests.get(url=invest_url, headers=headers2, proxies=requests_proxies, verify=False,
                               timeout=TIMEOUT)
            text = res.text.encode('utf8').decode('unicode_escape')
            text = json.loads(text)
            data = text["data"]
            # print(data)
            # print("名称、备案域名、备案号")
            for each in data["list"]:
                siteName = each["siteName"]
                # print("收集网站【{}】的备案信息".format(siteName))
                domain = each["domain"]
                icpNo = each["icpNo"]
                # print(siteName, domain, icpNo)
                icpinfo_infos.append({"siteName": siteName, "domain": domain, "icpNo": icpNo})
        except Exception as e:
            # print(e.args)
            pass
    # print()
    return icpinfo_infos


# 对外投资
def invest(pid, invest_page):
    print("开始查询对外投资企业:{}".format(invest_num))

    for i in range(1, invest_page + 1):
        try:
            invest_url = "https://aiqicha.baidu.com/detail/investajax?p={}&size={}&pid={}".format(i, size, pid)
            res = requests.get(url=invest_url, headers=headers2, proxies=requests_proxies, verify=False,
                               timeout=TIMEOUT)
            text = res.text
            text = json.loads(text)
            data = text["data"]
            # print(data)
            # print("被投资企业、投资占比、被投资企业的pid")
            for each in data["list"]:
                # 对外投资企业名称
                entName = each["entName"]
                print("查询对外投资企业【{}】".format(entName))
                # 投资占比
                regRate = each["regRate"]
                # 只保存投资占比大于50%的数据
                regRate_int = int(regRate.replace("%", ""))
                if regRate_int > 49:
                    # 被投资企业的pid
                    invest_pid = each["pid"]
                    # print(entName, regRate, invest_pid)
                    icpinfo_infos = icpinfo(invest_pid, 1)
                    companyDetail_infos = companyDetail(invest_pid)
                    invest_infos.append({"pid": invest_pid, "invest_info": {"entName": entName, "regRate": regRate},
                                         "icp_info": icpinfo_infos, "companyDetail_infos": companyDetail_infos})
                    # invest_info.append({invest_pid: [entName, regRate]})
        except Exception as e:
            # print(e.args)
            pass
    print()


# 控股企业
def holds(pid, holds_page):
    print("开始查询控股企业: {}".format(holds_num))
    for i in range(1, holds_page + 1):
        try:
            holds_url = "https://aiqicha.baidu.com/detail/holdsajax?p={}&size={}&pid={}".format(i, size, pid)
            res = requests.get(url=holds_url, headers=headers2, proxies=requests_proxies, verify=False, timeout=TIMEOUT)
            text = res.text
            text = json.loads(text)
            data = text["data"]
            # print(data)
            # print("控股企业名称、投资占比、控股企业pid")
            for each in data["list"]:
                # print(each)
                # 控股企业名称
                entName = each["entName"]
                print("查询控股企业【{}】".format(entName))
                # 投资占比
                proportion = each["proportion"]
                # 只保存投资占比大于50%的数据
                proportion_int = int(proportion.replace("%", ""))
                print(proportion_int)
                if proportion_int > 49:
                    # 控股企业pid
                    holds_pid = each["pid"]
                    # print(entName, proportion, holds_pid)
                    icpinfo_infos = icpinfo(holds_pid, 1)
                    companyDetail_infos = companyDetail(holds_pid)
                    holds_infos.append({"pid": holds_pid, "holds_info": {"entName": entName, "proportion": proportion},
                                        "icp_info": icpinfo_infos, "companyDetail_infos": companyDetail_infos})
        except Exception as e:
            print(e.args)
    print()


# 分支机构
def branch(pid, branch_page):
    print("开始查询分支机构:{} ".format(branch_num))
    for i in range(1, branch_page + 1):
        try:
            branch_url = "https://aiqicha.baidu.com/detail/branchajax?p={}&size={}&pid={}".format(i, size, pid)
            res = requests.get(url=branch_url, headers=headers2, proxies=requests_proxies, verify=False,
                               timeout=TIMEOUT)
            text = res.text
            text = json.loads(text)
            data = text["data"]
            # print(data)
            # print("分支机构名称、分支机构pid")
            for each in data["list"]:
                # print(each)
                # 分支机构名称
                entName = each["entName"]
                print("查询分支机构【{}】".format(entName))
                # 控股企业pid
                branch_pid = each["pid"]
                # print(entName, branch_pid)
                icpinfo_infos = icpinfo(branch_pid, 1)
                companyDetail_infos = companyDetail(branch_pid)
                branch_infos.append({"pid": branch_pid, "branch_info": {"entName": entName}, "icp_info": icpinfo_infos,
                                     "companyDetail_infos": companyDetail_infos})
        except Exception as e:
            print(e.args)
    print()


def start(searchContent):
    # 获取匹配度最高的pid
    url = 'https://aiqicha.baidu.com/index/suggest'
    data = {"q": searchContent}

    try:
        res = requests.post(url=url, data=data, headers=headers, proxies=requests_proxies, verify=False,
                            timeout=TIMEOUT)
    except Exception as e:
        print(e.args)
        return [], [], [], []

    text = res.text
    # queryStr = re.findall('queryStr":"(.*?)"', text)
    # 取第一个pid，是匹配度最高的
    pids = re.findall('pid":"(.*?)"', text)
    if pids == []:
        print("没有匹配到pids")
        return [], [], [], []

    pid = pids[0]
    print("获取到匹配度最高的pid:{}".format(pid))

    companyDetail(pid)

    global headers2
    # 获取网站备案、对外投资、控股企业、分支机构
    headers2 = {
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'Accept': 'application/json, text/plain, */*',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://aiqicha.baidu.com/company_detail_{}'.format(pid),
        'Zx-Open-Url': 'https://aiqicha.baidu.com/company_detail_{}'.format(pid),
        'Cookie': 'BAIDUID_BFESS=9B3B2A04BCAF3F00A1749A28EE79A301:FG=1; log_guid=7e65c373969e102f1328a2d7784761ae; _j47_ka8_=57; BAIDUID=F43177C434B64D167BDC8D0BE5F0F64F:FG=1; BDUSS=H5DTDhreUt4Qm9jQ1VteG5EbVd-dHh4R2VubnM1Vm9ZU0t3a35pQUlLOVZyNzlpSVFBQUFBJCQAAAAAAAAAAAEAAAAX8IQhscuwtuzh1OHA4QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFUimGJVIphid; BDUSS_BFESS=H5DTDhreUt4Qm9jQ1VteG5EbVd-dHh4R2VubnM1Vm9ZU0t3a35pQUlLOVZyNzlpSVFBQUFBJCQAAAAAAAAAAAEAAAAX8IQhscuwtuzh1OHA4QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFUimGJVIphid; BDPPN=f20be85e1dd6a0d72fd8797a5a9273b5; _t4z_qc8_=xlTM-TogKuTwheiv5Kf8lQwu9RDjERlFKAmd; ab165413520=262ca04b22da7de933251a28691da75016541374429f5; _s53_d91_=b5e26c8e8effdf053fb0a47a94148130c3f0ae823babd8ddf87fe9c3d20e7601a350bee4dff0d12a15d7848432762bc4e95b6b5dd9e15a5a3ad470ef3dfb3c1b9bc4df8652d23954881a4c7b8ed4af229d958ab9e99a3a8e7fe976a738f1c10d97863be8359557048cae2b0d6dcf58cb01ee9e609373f45b683a166cf6fa92e224016078ae2acfebf9f2e22bdf3d0e9692630e4468d9f232e41b6a3b408394f6a7d7f22f27f73a9fc1a3bee17867284237fa367ce76bccf30f2692166ceef9f52f8e55b79d0de4a92c854bba63e90893; _y18_s21_=394e3085; ab_sr=1.0.1_NmNjMGUzNmJjMGFmYTM1Zjc4MjA0ZWMwYzZlMmZjM2Q3MGY3Y2FlMjIzYjM0NTQxY2I0YmEwM2ZhNTRmYmMyMTA4NWM5MmJmOWUyOTg3NGVkYjlhMzE2ZjMzOWE0OWM1N2VlODZkOTVlMWJmNjFmM2FhYzc0ZTkyMGQ0ZWExN2IyZTQ4MzE5MGFkZjNlYmYyNDMwMjFhMzVmMzE5MWRiNThlNGQ1MGQ4NGUzZjFmMDk0YTNkM2VkZTg0Yzk3Zjc2; RT="z=1&dm=baidu.com&si=pzcfdkgzbt&ss=l3wep8qg&sl=8&tt=5y7&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=w1r&ul=1hv7"',
    }
    url = r"https://aiqicha.baidu.com/compdata/navigationListAjax?pid={}".format(pid)
    # print(url)
    res = requests.get(url=url, headers=headers2, proxies=requests_proxies, verify=False, timeout=TIMEOUT)
    text = res.text
    text = text.encode('utf-8').decode('unicode_escape')
    # print(text)
    text_json = json.loads(text)
    basic, certRecord = [], []
    for _ in text_json["data"]:
        if _["id"] == "basic":
            # 基本信息
            basic = _["children"]
        if _["id"] == "certRecord":
            # 知识产权
            certRecord = _["children"]
    # print(basic)
    # print(certRecord)
    global invest_num, holds_num, branch_num, webRecord_num
    invest_num, holds_num, branch_num, webRecord_num = 0, 0, 0, 0
    # 网站备案
    for each in certRecord:
        if each["name"] == "网站备案":
            webRecord_num = each["total"]

    for each in basic:
        if each["name"] == "对外投资":
            invest_num = each["total"]
        if each["name"] == "控股企业":
            holds_num = each["total"]
        if each["name"] == "分支机构":
            branch_num = each["total"]

    print("网站备案:{}\n对外投资:{}\n控股企业:{}\n分支机构:{}\n".format(webRecord_num, invest_num, holds_num, branch_num))

    if branch_num > 200:
        branch_num = 30

    # 页数
    icpinfo_page = webRecord_num // size + 1
    invest_page = invest_num // size + 1
    holds_page = holds_num // size + 1
    branch_page = branch_num // size + 1

    # 备案信息
    selfIcpinfo_infos = icpinfo(pid, icpinfo_page)
    # 对外投资
    invest(pid, invest_page)
    # 控股企业
    holds(pid, holds_page)
    # 分支机构
    branch(pid, branch_page)

    return selfIcpinfo_infos, invest_infos, holds_infos, branch_infos


def run_aiqicha(searchContent):
    selfIcpinfo_infos, invest_infos, holds_infos, branch_infos = start(searchContent)
    print(selfIcpinfo_infos)
    print(invest_infos)
    print(holds_infos)
    print(branch_infos)
    return selfIcpinfo_infos, invest_infos, holds_infos, branch_infos


if __name__ == '__main__':
    searchContent = "四川电力公司"
    run_aiqicha(searchContent)
