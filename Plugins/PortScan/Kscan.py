import os
import time

from Config.log import logger


def run_kscan(ip_list):
    """
    调用kscan进行端口扫描和指纹识别
    :param ip_list:
    :return:
    """
    file = gen_file(ip_list)
    output_file = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()) + '_kscan.txt'
    if os.path.exists(file):
        os.system('Plugins/kscan -t file:{} -oJ {}'.format(file, output_file))
        if os.path.exists(output_file):
            logger.log('ALERT', f'使用kscan进行端口扫描和指纹识别完成, 输出文件: {output_file}')
    return output_file


def gen_file(ip):
    """
    生成ip列表文件
    :return:
    """
    ip_list = list(ip)
    file_name = 'results/ip_list.txt'
    with open(file_name, 'w') as f:
        for i in ip_list:
            f.write(i + '\n')
    return file_name
