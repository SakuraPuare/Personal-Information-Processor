# 个人信息处理脚本

**本项目仅供学习参考！！！**

## 介绍

自己写的一个处理微信聊天记录的脚本，将聊天记录中出现的人名，车牌号，及其他信息进行处理，配合自定义的黑名单，能精准的识别信息并输出到文件中。

**本脚本只适用于只有个人信息的聊天记录，若有群友的各种吹逼那当然是无法识别的**

本项目基于[jieba](https://github.com/fxsjy/jieba)分词，特性在于自己基于经验写的人肉正则匹配。

> “结巴”中文分词：做最好的 Python 中文分词组件

## 运行

`pip install -r requirements.txt`

`python fenci.py`

## 配置

使用此脚本，您需要充分理解本人写的垃圾代码，并懂得如何修改。

需要自己配置`black_list_pre`和`black_list_lte`来达到匹配的效果。

## 聊天记录提取方法

将微信聊天记录合并转发，再收藏。在收藏中打开，右上角转换为笔记，退出得到纯文字版本。

## 效果演示

以下信息涉及个人隐私，已用`*`脱敏

**防喝茶**