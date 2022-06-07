# -*- coding:utf-8 -*-
import os

from Config.log import logger


class Dictionary:
    """
    字典管理
    """

    def __init__(self):
        self.dict_path = './Plugins/Dict/'  # 字典路径
        self.domain_list = []  # 域名列表
        self.subdomain_list = []  # 子域名列表
        self.history_domain_list = []  # 历史域名列表
        self.dict_name = 'small_subdomain.txt'  # 字典文件名
        self.dict_key_dict = 'dict_key.txt'  # 字典key值文件名
        self.domain_history = 'domain_history.txt'  # 历史域名文件名
        self.dict_num_file = 'dict_num.txt'  # 字典累计爆破域名计数文件名
        self.dict_num = 0  # 字典累计爆破域名计数
        self.dict_dict = []  # 字典列表
        self.dict_key_dict_dict = {str: int}  # 字典key值字典
        self.dict_load()

    def dict_update(self):
        """
        更新字典
        :return:
        """
        # 判断是否有历史域名文件
        his_file_path = self.dict_path + self.domain_history
        self.is_history_domain(his_file_path)
        # 获取新子域名列表与新域名个数
        new_subdomain, domain_num = self.get_new_domain_and_num()
        # 判断是否有字典权值文件
        self.dict_key_dict_dict = self.dict_key_dict_load()
        # 根据子域名结果更新字典权值
        self.update_key(new_subdomain)
        # 更新字典按照值排序
        self.dict_key_dict_dict = sorted(self.dict_key_dict_dict.items(), key=lambda item: item[1], reverse=True)
        # 判断累计爆破域名计数文件是否存在
        if os.path.exists((self.dict_path + self.dict_num_file)):
            pass
        else:
            # 新建累计爆破域名计数文件
            with open(self.dict_path + self.dict_num_file, 'w') as f:
                f.write('0')
        # 获取累计爆破域名计数
        with open(self.dict_path + self.dict_num_file, 'r') as f:
            self.dict_num = int(f.read())
        # 判断累计次数是否大于20次
        if self.dict_num + domain_num > 20:
            # 更新字典
            self.update_dict()
            # 更新累计爆破域名计数清空
            os.unlink(self.dict_path + self.dict_num_file)
            os.unlink(self.dict_path + self.dict_key_dict)
        else:
            # 更新字典计数
            self.dict_num += domain_num
            with open(self.dict_path + self.dict_num_file, 'w') as f:
                f.write(str(self.dict_num))
            # 更新字典key值文件
            with open(self.dict_path + self.dict_key_dict, 'w') as f:
                for i in self.dict_key_dict_dict:
                    f.write(i + ':' + str(self.dict_key_dict_dict[i]) + '\n')
        # 更新历史域名文件
        with open(self.dict_path + self.domain_history, 'a') as history_file:
            for new in new_subdomain:
                history_file.write(new + '\n')
        logger.log('INFO', '字典更新完成')

    def is_history_domain(self, path):
        """
        判断是否有历史域名文件
        :return:
        """
        if os.path.exists(path):
            with open(path, 'r') as f:
                for line in f.readlines():
                    self.history_domain_list.append(line.strip())
        else:
            # 新建历史域名文件
            self.history_domain_list = []

    def get_new_domain_and_num(self):
        """
        获取新域名
        :return:
        """
        domain_num = 0
        new_domain = []
        new_subdomain = []
        for i in self.domain_list:
            if i not in self.history_domain_list:
                new_domain.append(i)
                domain_num += 1
            else:
                pass
        if domain_num != 0:
            new_subdomain = []
            for j in self.subdomain_list:
                j_list = j.split('.')[1]
                if j_list in new_domain:
                    new_subdomain.append(j.split('.')[0])
        return new_subdomain, domain_num

    def dict_load(self):
        """
        加载字典
        :return:
        """
        path = self.dict_path + self.dict_name
        with open(path, 'r') as f:
            self.dict_dict = f.readlines()

    def dict_key_dict_load(self):
        """
        加载字典权值
        :return:
        """
        key_file_path = self.dict_path + self.dict_key_dict
        if os.path.exists(key_file_path):
            pass
        else:
            # 新建字典权值文件
            with open(key_file_path, 'w') as f:
                for i in self.dict_dict:
                    f.write(i + ':0' + '\n')
        with open(key_file_path, 'r') as f:
            for line in f.readlines():
                self.dict_key_dict_dict.update({line.split(':')[0]: int(line.split(':')[1].strip())})
            return self.dict_key_dict_dict

    def update_key(self, new_subdomain):
        """
        更新字典权值
        :return:
        """
        for key in self.dict_key_dict_dict:
            for i in new_subdomain:
                if key == i:
                    self.dict_key_dict_dict[key] += 1

    def update_dict(self):
        """
        更新字典
        :return:
        """
        new_list = set()
        for i in self.dict_key_dict_dict:
            new_list.add(i)
        new_list = new_list[:4501]
        # 读取big_subdomian.txt内容添加到new——list
        with open(self.dict_path + 'big_subdomain.txt', 'r') as f:
            big_list = f.readlines()
            for line in f.readlines():
                new_list.add(line.strip())
                big_list.remove(line)
                if len(new_list) == 5000:
                    break
        # 写入big_subdomain.txt
        with open(self.dict_path + 'big_subdomain.txt', 'w') as f_b:
            big_list = set(big_list)
            for i in iter(big_list):
                f_b.write(i)
        # 写入新字典
        with open(self.dict_path + self.dict_name, 'w') as f_s:
            for i in iter(new_list):
                f_s.write(i)
