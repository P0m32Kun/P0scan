import socket

import requests

from Config.log import logger


def domain_to_ip(domain):
    """
    域名转ip
    :return:
    """
    try:
        ip = socket.gethostbyname(domain.strip())
        return ip
    except Exception as e:
        logger.log('DEBUG', '获取域名转ip失败，原因：{}'.format(e))
        return ''


def domain_to_company(domain):
    """
    域名转企业名称
    :return:
    """
    company = ''
    http = ['http://www.', 'https://www.']
    for i in http:
        try:
            domain_http = i + domain
            req = requests.get(domain_http, timeout=5)
            if req.status_code == 200:
                text = req.text
                company = text.split('<title>')[1].split('</title>')[0]
                continue
        except Exception as e:
            logger.log('DEBUG', '获取域名转企业名称失败，原因：{}'.format(e))
    return company
