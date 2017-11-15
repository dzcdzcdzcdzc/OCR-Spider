# 基于OCR文字识别的爬虫项目

<!-- BADGES/ -->
![Python Version](https://img.shields.io/badge/python-3.6-blue.svg)
<!-- /BADGES -->

## 介绍
爬取http://piaofang.maoyan.com/?ver=normal中的票房信息。使用了tesseract来识别css自定义字体中的数字。

项目博客地址：http://www.dzc.me/2017/10/%E5%9F%BA%E4%BA%8Eocr%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB%E7%9A%84%E7%88%AC%E8%99%AB%E9%A1%B9%E7%9B%AE/

## 依赖
语言：python3.6

python包：

beautifulsoup4 (4.6.0) 用于html解析

fonttools (3.17.0) 字体文件格式转换

Pillow (4.3.0) 用于文字图片的生成

pytesseract (0.1.7) 对tesseract的封装

依赖程序：

tesseract3.05 google出品的字体识别软件