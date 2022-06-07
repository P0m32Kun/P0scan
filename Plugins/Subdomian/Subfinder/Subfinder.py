import os

import Common.clean_cache as clean_cache
from Config.log import logger


def run_subfinder(domain_list):
    """
    调用subfinder进行子域名被动收集的入口函数
    :param: domain_file 主域或域名列表
    :param: output_file 输出文件
    :return:
    """
    domain_file = gen_domain_file(domain_list)
    output_file = 'results/subfinder_domain.txt'
    if os.path.exists(domain_file):
        logger.log('ALERT', f'开始使用subfinder被动收集子域名')
        os.system('./Plugins/subfinder -dL {} -o {} -t 20 -s fofa,github,censys,chinaz,securitytrails,threatbook,'
                  'virustotal -nW -silent -config ./Config/subfinder/config.yaml -pc '
                  './Config/subfinder/provider-config.yaml'.format(domain_file, output_file))
        if os.path.exists(output_file):
            logger.log('ALERT', f'使用subfinder被动收集子域名完成, 输出文件: {output_file}')
        else:
            logger.log('ALERT', f'使用subfinder被动收集子域名失败, 无文件输出，请检查subfinder相关配置')
        clean_cache.delete_cache_file(domain_file)
    else:
        logger.log('ALERT', f'主域文件不存在, 请检查主域文件是否存在')
        exit(0)
    return output_file


def gen_domain_file(domain_list):
    """
    生成主域文件
    :param: domain_list 主域列表
    :return:
    """
    domain_list = list(domain_list)
    domain_file = 'results/domain.txt'
    with open(domain_file, 'w') as f:
        for domain in domain_list:
            f.write(domain + '\n')
    logger.log('ALERT', f'生成主域文件: {domain_file}')
    return domain_file
