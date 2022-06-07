"""
根据返回页面的text相似度判断页面是否相同，没有找到更好的办法解决这个问题
"""
import difflib


def is_similar(text1, text2):
    """
    判断两个页面是否相似
    :param text1:
    :param text2:
    :return:
    """
    return difflib.SequenceMatcher(None, text1, text2).quick_ratio() > 0.8
