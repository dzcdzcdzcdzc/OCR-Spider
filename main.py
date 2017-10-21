import os.path
import re
import base64
from bs4 import BeautifulSoup
import urllib.request
from fontTools.ttLib import TTFont
from PIL import Image, ImageFont, ImageDraw
import pytesseract

basedir = os.path.dirname(os.path.realpath(__file__)) + "\\"  # 记录当前脚本目录
data = {}  # 存放映射关系
# 配置tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'  # 设置tesseract安装目录

tessdata_dir_config = r'--tessdata-dir "C:\Program Files (x86)\Tesseract-OCR\tessdata" --psm 10 digits'
r"""
tessdata-dir 设置tessdata路径
psm 10 每张图片仅仅有一个文字
digits 读取tessdata\configs\digits配置 设置图片的内容只为数字 提高正确率
"""


def distinguish(string: str) -> str:
    """
    将字符串中的编码变成数字
    :param string: str
    :return: str
    """
    string = repr(string)[1:-1]
    # 这时string类似为'\ue901\uf81d\uf81d\ue800.\ue800万'的字符串
    arr = re.findall(r"\\u\S{4}", string)  # 正则表达式匹配编码文字
    arr = list(set(arr))  # 去重
    for value in arr:
        if value not in data:  # 不在已知映射表中
            text = bytes(value, 'ascii').decode('unicode_escape')  # 将\ue800这个6位字符串转成一位unicode编码
            im = Image.new("RGB", (25, 50), (255, 255, 255))  # 生成一张25*50白底的图片
            dr = ImageDraw.Draw(im)  # 开始画图
            image_font = ImageFont.truetype(basedir + 'temp.ttf', 50)  # 设置字体文件和大小
            dr.text((0, 0), text, font=image_font, fill="#000000")  # 用设置的字体在0,0的位置插入黑色文字
            text = pytesseract.image_to_string(im, config=tessdata_dir_config)  # 使用pytesseract进行分析
            data[value] = text  # 将映射关系写入映射表中
        string = string.replace(value, data[value])  # 将编码按照映射表进行替换
    return string


with urllib.request.urlopen('http://piaofang.maoyan.com/?ver=normal') as f:  # 爬去地址
    html = BeautifulSoup(f.read(), "html.parser")  # 使用BeautifulSoup用html.parser解析器进行html解析
font = html.find(id="js-nuwa")  # 读取存放字体文件的css内容
font = re.search(r'(?<=,)\S*(?=\))', str(font))  # 用正则表达式找出woff的base64字符串
if not font:
    print('未发现字体')
    exit()
font = base64.b64decode(font.group())  # base64解码成二进制文件
with open(basedir + 'temp.woff', 'wb') as f:
    f.write(font)  # 保存二进制到脚本根目录
font = TTFont(basedir + 'temp.woff', recalcBBoxes=False, recalcTimestamp=False)  # Pillow不支持用woff生成文字图片
font.flavor = None
font.save(basedir + 'temp.ttf', reorderTables=True)  # 将字体文件从woff转换成ttf

for n in html.find_all('ul', 'canTouch'):
    print(
        n.find('li', 'c1').b.string,
        distinguish(n.find('li', 'c1').find('i', 'cs').string),
        distinguish(n.find('li', 'c2').b.i.string),
        distinguish(n.find('li', 'c3').i.string),
        distinguish(n.find('li', 'c4').i.string),
        distinguish(n.find('li', 'c5').span.i.string),
    )
