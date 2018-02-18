#!/usr/bin/python3

# Create Word Cloud
#
# Author: Zhao Zhongwen
#
# Waterfall -v1.0 (2018-02-18T00:22:54+0900)
#
# Copyright 2018 Zhao Zhongwen
#
# Released under the MIT license
#
# http://opensource.org/licenses/MIT
# ===============================================
""" 根据语料库中的词生成词云 """

import re
import jieba
import codecs
import matplotlib

from scipy.misc import imread
from string import punctuation
from wordcloud import WordCloud
from optparse import OptionParser

matplotlib.use('TkAgg')  # `Python is not installed as a framework` 错误时使用
import matplotlib.pyplot as plt


class WordCloudConfig(object):
    """词云配置类

    生成词云时的配置类

    Attributes:
        corpus_path: 语料库路径
        picture_path: 背景图片路径
        font_path: 字体模板路径
    """

    def __init__(self, corpus_path, picture_path, font_path):
        self.corpus_path = corpus_path
        self.picture_path = picture_path
        self.font_path = font_path
        self.corpus = None
        self.back = None

    def open_corpus(self):
        """打开语料库文件"""

        file = codecs.open(self.corpus_path, 'r', encoding='utf-8')
        if not file:
            raise IOError

        corpus = file.read()
        self.corpus = corpus
        file.close()

    def open_picture(self):
        """打开背景图片"""
        self.back = imread(self.picture_path)


def tokenization(corpus_path):
    """生成token

    将语料库中的所有标点符号去除并用半角空格代替。

    Args:
        corpus_path: 语料库路径

    Returns:
        一个存有token的一维数组，每一行是一个字符串

    Raises:
        IOError: 读取文件时发生错误
    """
    punc = (punctuation +  # 中文标点符号
            u'.,;《》？！“”‘’@#￥%…&×（）——+【】{};；●，。&～、|\s:：')
    corpus_clean = []

    file = codecs.open(corpus_path, encoding='utf-8')

    if not file:
        raise IOError

    for line in file:
        line = re.sub(r'[{}]+'.format(punc), ' ', line)  # 正则匹配去除标点
        corpus_clean.append(line + ' ')
    file.close()

    return corpus_clean


def segmant(corpus, except_word=None):
    """中文分词

    利用jieba包进行分词
    可以自由添加不想分割的词

    Args:
        corpus: 语料库列表，每一行一个字符串
        except_word: 不想分分割的词的列表

    Returns:
        一个二维数组，每行是已经分好词的原语料库的内容
        例如：
        [ 'aaa bbb ccc', 'xxx yyy zzz']
    """
    if not except_word:
        except_word = []

    for word in except_word:  # 添加例外词
        jieba.add_word(word)

    segmented_line = []
    generator = jieba.cut(corpus, cut_all=False)  # 分词
    for word in generator:
        segmented_line.append(word)

    return ' '.join(segmented_line)


def create_word_cloud(config):
    """生成词云

    利用wordcloud将已分好词的语料库'
    按照词频绘制成词云图

    Args:
        config: 词云生成器配置类，详见WordCloudConfig

    Returns:
        词云图片，默认文件名: WordCloud.png
    """
    # TODO (Zhao Zhongwen): 这些参数都应该可变
    word_cloud = WordCloud(background_color='white',  # 背景色
                           max_words=300,  # 调取词的最大个数
                           mask=config.back,  # 背景图片
                           max_font_size=200,  # 最大字体
                           font_path=config.font_path  # 字体模板路径（避免中文乱码）
                           )

    word_cloud.generate(config.corpus)  # 核心：生成词云对象

    # 显示词云
    plt.show(word_cloud)
    plt.axis('off')  # 关闭坐标轴
    plt.figure()
    plt.imshow(word_cloud)
    plt.axis('off')
    word_cloud.to_file('WordCloud.png')


def main():
    usage = 'usage: %prog [options] args corpus_path image_path, font_path'
    parser = OptionParser(usage=usage)

    parser.add_option('-t',
                      '--tokenization',
                      action='store_true',
                      dest='token',
                      default=False,
                      help='将语料库中的所有标点符号去除并用半角空格代替')

    (options, args) = parser.parse_args()

    config = WordCloudConfig(args[0], args[1], args[2])
    config.open_corpus()
    config.open_picture()

    # 分词 TODO (Zhao Zhongwen) 加入特定的词
    config.corpus = segmant(config.corpus)
    create_word_cloud(config)


if __name__ == '__main__':
    main()
