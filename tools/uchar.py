# -*- coding: utf-8 -*-

"""判断一个unicode是否是汉字"""


def is_chinese(uchar):
    return u'\u4e00' <= uchar <= u'\u9fa5'


"""判断一个unicode是否是数字"""


def is_number(uchar):
    return u'\u0030' <= uchar <= u'\u0039'


"""判断一个unicode是否是英文字母"""


def is_alphabet(uchar):
    return (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a')


"""判断是否是（汉字，数字和英文字符之外的）其他字符"""


def is_other(uchar):
    return not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar))
