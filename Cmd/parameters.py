# -*- coding: utf-8 -*-
import argparse
import os.path
import re

from Config.log import logger


def is_valid_domain(target):
    """
    判断字符串是否为域名
    :param target: 目标字符串
    :return: True or False
    """
    pattern = re.compile(
        r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.'
        r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
    )
    if pattern.match(target):
        return True
    else:
        return False


def is_valid_ip(target):
    """
    判断字符串是否为ip
    :param target: 目标字符串
    :return:
    """
    pattern = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if pattern.match(target):
        return True
    else:
        return False


def is_valid_company_name(target):
    """
    判断字符串是否为企业名称
    :param target: 目标字符串
    :return:
    """
    if not target.isalnum():
        return True
    else:
        return False


def get_target(target_list):
    """
    获取目标
    :param target_list: 目标列表
    :return:
    """
    ip_list, domain_list, company_list = set(), set(), set()
    for i in target_list:
        if is_valid_ip(i):
            ip_list.add(i)
        elif is_valid_domain(i):
            domain_list.add(i)
        elif is_valid_company_name(i):
            company_list.add(i)
        else:
            logger.log('ERROR', '输入的目标不合法,给我改！')
    return ip_list, domain_list, company_list


def get_args():
    """
    获取命令行参数
    :return: arg
    """
    parser = argparse.ArgumentParser(description='')
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument('-t', '--target', type=str, default='', help='测试目标，可以是ip、域名、企业名称')
    group1.add_argument('-f', '--file', type=str, default='', help='目标列表文件')
    group1.add_argument('-b', '--brute', type=bool, default='', help='是否进行域名爆破')
    group1.add_argument('-d', '--dictionary', type=str, default='', help='域名爆破字典路径')
    group1.add_argument('-o', '--output', type=str, default='', help='结果保存到文件名，保存格式为xlsx')
    args = parser.parse_args()
    arg = {
        'single_target': args.target,
        'target_file': args.file,
        'is_brute': args.brute,
        'dictionary_path': args.dictionary,
        'output_file': args.output
    }
    return arg


def run_get_args():
    """
    获取命令行参数函数入口
    :return:
    """
    arg = {
        'single_target': '',
        'target_file': '',
        'is_brute': False,
        'dictionary_path': '',
        'ip_list': set(),
        'domain_list': set(),
        'company_list': set(),
        'output_file': ''
    }
    args = get_args()
    arg['ip_list'], arg['domain_list'], arg['company_list'] = \
        get_target_list(args['single_target'], args['target_file'])
    arg['is_brute'] = is_brute(args['is_brute'], args['dictionary_path'])
    arg['output_file'] = args['output_file']
    if arg['output_file'] != '':
        # 判断字符串后5位是否为.xlsx
        if arg['output_file'][-5:] != '.xlsx':
            arg['output_file'] = arg['output_file'] + '.xlsx'
    return arg


def get_target_list(single_target, target_file):
    """
    获取域名、ip、企业名称列表
    :return:
    """
    ip_list, domain_list, company_list = set(), set(), set()
    if single_target == '' and target_file == '':
        logger.log('DEBUG', '请输入目标或者目标列表文件')
        exit()
    elif single_target != '':
        single_target = single_target.replace(' ', ',')
        target_list = single_target.split(',')
        target_list = list(filter(None, target_list))
        target_list = list(set(target_list))
        ip_list, domain_list, company_list = get_target(target_list)
    elif os.path.exists(target_file):
        with open(target_file, 'r') as f:
            target_list = f.readlines()
        ip_list, domain_list, company_list = get_target(target_list)
    else:
        logger.log('DEBUG', '目标列表文件不存在')
        exit()
    logger.log('INFO', '获取参数完成')
    return ip_list, domain_list, company_list


def is_brute(can_brute, dictionary_path):
    """
    判断是否进行子域名爆破
    :param can_brute:
    :param dictionary_path:
    :return:
    """
    if can_brute:
        if dictionary_path == '':
            logger.log('ALERT', '未指定字典，将使用ksubdomain默认字典')
        elif not os.path.exists(dictionary_path):
            logger.log('DEBUG', '字典不存在')
    else:
        return False


# 入口
if __name__ == '__main__':
    get_args()
