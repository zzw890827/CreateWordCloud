# Create Word Cloud
根据语料库生成词云
## 依赖
* re
* jieba
* scipy
* codecs
* string
* optparse
* wordcloud
* matplotlib

## 用法
1. 基本用法：<br>
准备语料库，背景图片，字体文件。我们提供了一系列方法来处理语料库，但是目前没有提供接口。
2. 基本命令：<br>
`python create_word_cloud.py corpus_path image_path template_path`<br>
将来我们会提供一系options去完善功能
3. 查看文档：<br>
`pydoc create_word_cloud`
4. 查看帮助信息：<br>
`python create_word_cloud.py -h`

## TODO
*[] 提供语料库处理接口
*[] 提供词云生成器控制接口
*[] 添加网络爬虫功能和词频统计功能
