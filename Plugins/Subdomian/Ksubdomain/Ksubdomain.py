import os
import time

from Config.log import logger
from Plugins.Dict.Dict import Dictionary

ksubdomain_list = set()
domain_list = list()


def run_ksubdomain(domain_list, path):
    """
    入口函数，调用ksubdomain插件
    :param path: 字典路径
    :param domain_list:域名列表
    :return:
    """
    dict_path = path
    os.path.exists('./results/domain.txt')
    domain_file = gen_domain_file(domain_list)
    logger.log('ALERT', f'开始使用ksubdomain进行子域名爆破')
    output_file = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()) + '_ksubdomain_domain.txt'
    if dict_path:
        os.system('./Plugins/ksubdomain e --dl {} -o {} -f {}'
                  ' --od --skip-wild --silent'.format(domain_file, output_file, dict_path))
    else:
        os.system('./Plugins/ksubdomain e --dl {} -o {} -f {} --od --skip-wild'
                  ' --silent'.format(domain_file, output_file, "./Plugins/Dict/small_subdomain.txt"))
    if os.path.exists(output_file):
        v_output_file = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()) + '_ksubdomain.txt'
        os.system('./Plugins/ksubdomain v -f {} -o {} --silent --od'.format(output_file, v_output_file))
        if os.path.exists(v_output_file):
            logger.log('ALERT', f'使用ksubdomain进行子域名爆破完成, 输出文件: {v_output_file}')
            with open(v_output_file, 'r') as f:
                for line in f.readlines():
                    ksubdomain_list.add(line.strip())
        # 删除临时文件
        os.unlink(v_output_file)
    os.unlink(output_file)
    update_dict()
    return ksubdomain_list


def gen_domain_file(domain_l):
    """
    生成主域文件
    :param: domain_l 主域列表
    :return:
    """
    domain_list = list(domain_l)
    if len(domain_list) == 0:
        logger.log('DEBUG', '主域列表为空')
        exit(0)
    domain_file = os.path.join(os.getcwd(), 'results', 'domain.txt')
    with open(domain_file, 'w') as f:
        for domain in domain_list:
            f.write(domain + '\n')
    logger.log('ALERT', f'生成主域文件: {domain_file}')
    return domain_file


def update_dict():
    """
    更新字典
    :return:
    """
    dict_obj = Dictionary()
    dict_obj.domain_list = domain_list
    dict_obj.subdomain_list = list(ksubdomain_list)
    dict_obj.dict_update()
