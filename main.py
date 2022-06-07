# -*- coding: utf-8 -*-
import json

import Cmd.parameters as parameters
import Common.Conversion as Conversion
import Common.clean_cache as clean_cache
import Plugins.PortScan.Kscan as Kscan
import Plugins.Save_to_xls as Save_to_xls
import Plugins.Subdomian.Aiqicha.Aiqicha as Aiqicha
import Plugins.Subdomian.Analysis.Analysis as Analysis
import Plugins.Subdomian.Ksubdomain.Ksubdomain as Ksubdomain
import Plugins.Subdomian.Subfinder.Subfinder as Subfinder
from Config.log import logger


def subfinder(target):
    """
    调用subfinder插件
    :param target: 目标
    :return:
    """
    if not target or len(target) == 0:
        logger.log('DEBUG', '主域列表为空')
        pass
        return set()
    else:
        output_file = Subfinder.run_subfinder(target)
        with open(output_file, 'r') as f:
            subfinder_set = set()
            for i in f.readlines():
                subfinder_set.add(i.strip('\n'))
            logger.log('ALERT', f'使用subfinder插件获取到子域名数量: {len(subfinder_set)}')
            logger.log('ALERT', f'使用subfinder插件获取到子域名列表: {subfinder_set}')
            clean_cache.delete_cache_file(output_file)
            return subfinder_set


def aiqicha(company_name_list):
    """
    调用爱企查插件
    :param company_name_list: 目标
    :return:
    """
    aiqicha_set = set()
    if not company_name_list or len(company_name_list) == 0:
        logger.log('DEBUG', '公司列表为空')
        pass
        return aiqicha_set
    else:
        for i in company_name_list:
            selficpinfo_infos, invest_infos, holds_infos, branch_infos = Aiqicha.run_aiqicha(i)
            for j in selficpinfo_infos:
                aiqicha_set.add(j['domain'])
            for k in invest_infos:
                aiqicha_set.add(k['icp_info']['domain'])
            for g in holds_infos:
                aiqicha_set.add(g['icp_info']['domain'])
            for m in branch_infos:
                aiqicha_set.add(m['icp_info']['domain'])
        logger.log('ALERT', f'使用爱企查插件获取到子域名数量: {len(aiqicha_set)}')
        logger.log('ALERT', f'使用爱企查插件获取到子域名列表: {aiqicha_set}')
        return aiqicha_set


def is_wildcard(domain):
    """
    判断是否为泛解析
    :param domain: 域名
    :return:
    """
    if Analysis.check_analysis(domain):
        return True
    else:
        return False


def ksubdomain(is_brute, domainlist, dict_path):
    """
    利用Ksubdomain插件获取子域名
    :param is_brute:
    :param domainlist: 主域列表
    :param dict_path: 字典路径
    :return:
    """
    ksubdomain_set = set()
    if is_brute:
        if not domainlist or len(domainlist) == 0:
            logger.log('DEBUG', '主域列表为空')
            exit()
        else:
            ksubdomain_set = Ksubdomain.run_ksubdomain(domainlist, dict_path)
            logger.log('ALERT', f'使用Ksubdomain插件获取到子域名数量: {len(ksubdomain_set)}')
            logger.log('ALERT', f'使用Ksubdomain插件获取到子域名列表: {ksubdomain_set}')
            return ksubdomain_set
    else:
        pass
    return ksubdomain_set


def save_to_file(domain_result, kscan_file_path, filename):
    """
    将结果写入文件
    :param filename:
    :param kscan_file_path:
    :param domain_result: 子域名
    :return:
    """
    with open(kscan_file_path, 'r') as f:
        data = json.loads(f.readline())
    filename = Save_to_xls.run_save_to_xls(domain_result, data, filename)
    return filename


def conversion(domain_ip_company):
    """
    将获取的domain,ip,公司名相互转换
    :param domain_ip_company 子域名
    :return:
    """
    domain_to_ip = list()
    domain_to_company = list()
    if len(domain_ip_company) != 0:
        for i in domain_ip_company:
            domain_to_ip.append(Conversion.domain_to_ip(i))
            domain_to_company.append(Conversion.domain_to_company(i))
        domain_to_ip = set(filter(None, domain_to_ip))
        domain_to_company = set(filter(None, domain_to_company))
    return domain_to_ip, domain_to_company


# logo
logo = f"""
$$$$$$$\   $$$$$$\                                         
$$  __$$\ $$$ __$$\                                        
$$ |  $$ |$$$$\ $$ | $$$$$$$\  $$$$$$$\ $$$$$$\  $$$$$$$\  
$$$$$$$  |$$\$$\$$ |$$  _____|$$  _____|\____$$\ $$  __$$\ 
$$  ____/ $$ \$$$$ |\$$$$$$\  $$ /      $$$$$$$ |$$ |  $$ |
$$ |      $$ |\$$$ | \____$$\ $$ |     $$  __$$ |$$ |  $$ |
$$ |      \$$$$$$  /$$$$$$$  |\$$$$$$$\\$$$$$$$ |$$ |  $$ |
\__|       \______/ \_______/  \_______|\_______|\__|  \__|
"""

if __name__ == '__main__':
    print(logo)
    args = parameters.run_get_args()
    domain_list, ip_list, company_list = args['domain_list'], args['ip_list'], args['company_list']
    domain_ip, domain_company = conversion(domain_list)
    ip_list.update(domain_ip)
    company_list.update(domain_company)
    subfinder_list = subfinder(domain_list)
    print(subfinder_list)
    aiqicha_list = aiqicha(company_list)
    ksubdomain_list = ksubdomain(args['is_brute'], domain_list, args['dictionary_path'])
    domain = subfinder_list.union(aiqicha_list).union(ksubdomain_list)
    port_file = Kscan.run_kscan(ip_list)
    result_file = save_to_file(domain, port_file, args['filename'])
