# -*- coding: utf-8 -*-

import jieba
from tools.uchar import is_other
from typing import List


class Classifier:
    def __init__(self):
        jieba.initialize()

    @staticmethod
    def _merge_two(first, second):
        new = list(first)
        new[0] += second[0]
        new[2] = second[2]
        return tuple(new)

    """
    Returns:
        [(cut_text, start, end)]
    """
    def cut_from_text(self, text: str) -> List[tuple]:
        #  处理标点符号，如：["《","后汉书","》"] -> ["《后汉书》"]，
        #               ['"', '你好'， '"'] -> ['"你好"'],
        #   ['他', '说', '：', '“', '我', '是', '海贼王', '！', '“'] -> ['他', '说：', '“我', '是', '海贼王！“']
        text = text.strip()
        res, last, yin_cnt, dan_cnt = [], None, 0, 0
        start_sign = {'《', '<', '“', '‘', '(', '（', '[', '【'}
        def last_add(last, info):
            if last is None:
                return info
            return self._merge_two(last, info)
        for cut_info in jieba.tokenize(text):
            if len(cut_info[0]) == 1 and is_other(cut_info[0]):     # 处理特殊符号，减少分词量。
                if cut_info[0] == '"': # 处理英文引号
                    yin_cnt += 1
                    if yin_cnt % 2 == 1:
                        last = last_add(last, cut_info)
                        continue
                if cut_info[0] == "'":
                    dan_cnt += 1
                    if dan_cnt % 2 == 1:
                        last = last_add(last, cut_info)
                        continue
                if cut_info[0] in start_sign:
                    # 需要添加在文字前的符号
                    last = last_add(last, cut_info)
                    continue
                elif res:
                    # 需要添加在文字后的符号
                    cut_info = self._merge_two(res.pop(), cut_info)
            if last:
                # 将前缀符号接上
                cut_info = self._merge_two(last, cut_info)
                last = None
            res.append(cut_info)
        return res

    def cut_from_file(self, filename):
        with open(filename, 'r') as f:
            res = f.readlines()
            return self.cut_from_text('\n'.join(res))
