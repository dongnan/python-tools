# -*- coding: UTF-8 -*-

import sys
import getopt
import types
import pycurl
import json
import urllib
import StringIO

reload(sys)
sys.setdefaultencoding('utf8')

VERSION = '0.0.1'


def translate(words, showEg):
    c = pycurl.Curl()
    c.setopt(pycurl.URL, 'http://fanyi.baidu.com/v2transapi')
    c.setopt(pycurl.CONNECTTIMEOUT, 3)
    c.setopt(pycurl.TIMEOUT, 5)
    c.setopt(pycurl.USERAGENT,
             'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/50.0.2661.102 Chrome/50.0.2661.102 Safari/537.36')
    c.setopt(pycurl.POSTFIELDS,
             urllib.urlencode({"from": "en", "to": "zh", "simple_means_flag": "3", "query": words}))
    c.fp = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, c.fp.write)
    c.perform()
    c.close()
    data = json.loads(c.fp.getvalue())
    if 'dict_result' in data.keys():
        if 'simple_means' in data['dict_result'].keys():
            if 'symbols' in data['dict_result']['simple_means'].keys():
                if len(data['dict_result']['simple_means']['symbols']):
                    ps = '[读音]'
                    if 'ph_am' in data['dict_result']['simple_means']['symbols'][0].keys():
                        ps += " [美]:" + data['dict_result']['simple_means']['symbols'][0]['ph_am']
                    if 'ph_en' in data['dict_result']['simple_means']['symbols'][0].keys():
                        ps += " [英]:" + data['dict_result']['simple_means']['symbols'][0]['ph_en']
                    if 'ph_other' in data['dict_result']['simple_means']['symbols'][0].keys():
                        ps += ' ' + data['dict_result']['simple_means']['symbols'][0]['ph_other']
                    print ps
                    if 'parts' in data['dict_result']['simple_means']['symbols'][0].keys() and isinstance(
                            data['dict_result']['simple_means']['symbols'][0]['parts'], types.ListType):
                        for part in data['dict_result']['simple_means']['symbols'][0]['parts']:
                            if 'part' in part and 'means' in part:
                                print part['part'], ';'.join(part['means'])
        if showEg:
            if 'collins' in data['dict_result'].keys():
                if 'entry' in data['dict_result']['collins'].keys() and isinstance(
                        data['dict_result']['collins']['entry'],
                        types.ListType):
                    for entry in data['dict_result']['collins']['entry']:
                        if 'value' in entry.keys() and len(entry['value']):
                            for value in entry['value']:
                                if 'tran' in value.keys() and 'def' in value.keys() and 'mean_type' in value.keys() and len(
                                        value['mean_type']):
                                    print ' - ' + value['tran']
                                    print '   ' + value['def']
                                    print '   例句:'
                                    for mean in value['mean_type']:
                                        if 'example' in mean.keys():
                                            for example in mean['example']:
                                                if 'tran' in example.keys() and 'ex' in example.keys():
                                                    print '        ' + example['tran']
                                                    print '        ' + example['ex']
            else:
                print ' 没有查询到相关例句.'


def usage():
    print "translate 是一个命令行翻译脚本,通过百度翻译接口获取翻译结果,并友好的输出"
    print "使用方法: python translate.py hello 或 python translate.py 'What\'s your name' "
    print "  -h,  --help       显示帮助信息"
    print "  -v,  --version    显示版本"
    print "  -e,  --example    显示例句"


opts, args = getopt.getopt(sys.argv[1:], "hve", ["help", "version", "example"])

if len(args):
    showEg = True
    for op, value in opts:
        if op == "-h" or op == "--help":
            usage()
            sys.exit()
        elif op == "-v" or op == "--version":
            print "translate 当前版本:" + VERSION
            sys.exit()
        elif op == "-e" or op == "--example":
            showEg = True
    translate(args[0], showEg)
else:
    print '缺少要翻译的单词或语句'
