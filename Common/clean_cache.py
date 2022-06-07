import os

from Config.log import logger


def delete_cache_file(file_path):
    """
    删除文件
    :param file_path: 文件路径
    :return:
    """
    if os.path.exists(file_path):
        os.remove(file_path)
        logger.log('ALERT', f'删除文件: {file_path}')
    else:
        logger.log('ALERT', f'文件不存在: {file_path}')
