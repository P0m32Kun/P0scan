# -*- coding: utf-8 -*-
import secrets

import dns
import requests

from Common import similarity
from Config.log import logger


def gen_random_subdomain(domain, count):
    """
    生成指定数量的随机子域域名列表
    :param domain: 主域
    :param count: 数量
    :return:
    """
    subdomains = set()
    if count < 1:
        return subdomains
    for _ in range(count):
        token = secrets.token_hex(4)
        subdomains.add(f'{token}.{domain}')
    return subdomains


def query_a_record(subdomain):
    """
    查询子域A记录
    :param subdomain: 子域
    """
    try:
        answer = dns.resolver.resolve(subdomain, 'A')
    except Exception as e:
        logger.log('DEBUG', f'Query {subdomain} wildcard dns record error')
        logger.log('DEBUG', e.args)
        return False
    if answer.rrset is None:
        return False
    ttl = answer.ttl
    name = answer.name
    ips = {item.address for item in answer}
    logger.log('ALERT', f'{subdomain} resolve to: {name} '
                        f'IP: {ips} TTL: {ttl}')
    return True


def all_resolve_success(subdomains):
    """
    判断是否所有子域都解析成功
    :param subdomains: 子域列表
    """
    resolver = dns.resolver.resolve(subdomains)
    resolver.cache = None  # 不使用DNS缓存
    status = set()
    for subdomain in subdomains:
        status.add(query_a_record(subdomain))
    return all(status)


def request_subdomain(subdomains):
    """
    判断是否所有子域都请求成功
    :param subdomains: 子域列表
    """
    results = list()
    req_list = list()
    for subdomain in subdomains:
        url = [r'http://' + subdomain, r'https://' + subdomain]
        for u in url:
            try:
                r = requests.get(u, timeout=5, verify=False)
                if r.status_code == 200:
                    logger.log('ALERT', f'{subdomain} request success')
                    results.append(True)
                    req_list.append(r.text)
                    break
            except Exception as e:
                logger.log('DEBUG', f'{subdomain} request error')
                logger.log('DEBUG', e.args)
                results.append(False)
    return all(results), req_list


def any_similar_requests(html):
    """
    判断是否有相似请求
    :param html: 响应内容列表
    """
    html1, html2, html3 = html[0], html[1], html[2]
    if similarity.is_similar(html1, html2) or similarity.is_similar(html1, html3) or \
            similarity.is_similar(html2, html3):
        return True  # 有相似请求
    return False  # 无相似请求


def check_analysis(domain):
    """
    判断是否可以进行子域分析
    :param domain: 主域
    """
    subdomains = gen_random_subdomain(domain, 3)
    request_result, html = request_subdomain(subdomains)
    if all_resolve_success(subdomains) and request_result and any_similar_requests(html):
        logger.log('ALERT', '{domain}可能存在泛解析，不进行爆破！')
        return True
    else:
        return False
