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
            if 'symbols' in data['dict_result']['simple_means'].keys() and isinstance(data['dict_result']['simple_means']['symbols'], types.ListType):
                for symbols in data['dict_result']['simple_means']['symbols']:
                    print '\n   "' + words + '"'
                    ps = ' - [读音]'
                    if 'ph_am' in symbols.keys() and symbols['ph_am'] is not None:
                        ps += "  [美]:" + symbols['ph_am']
                    if 'ph_en' in symbols.keys() and symbols['ph_en'] is not None:
                        ps += "  [英]:" + symbols['ph_en']
                    if 'ph_other' in symbols.keys() and symbols['ph_other'] is not None:
                        ps += '  ' + symbols['ph_other']
                    print ps
                    if 'parts' in symbols.keys() and isinstance(symbols['parts'], types.ListType):
                        for part in symbols['parts']:
                            if 'part' in part.keys() and 'means' in part.keys():
                                print '   ' + part['part'], ';'.join(part['means'])
        if showEg:
            if 'collins' in data['dict_result'].keys() and data['dict_result']['collins'] is not None:
                if 'entry' in data['dict_result']['collins'].keys() and isinstance(
                        data['dict_result']['collins']['entry'],
                        types.ListType):
                    print "\n - - 例句 - -\n"
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
                                    print ''
            else:
                print "\n - 没有查询到相关例句.\n"


def usage():
    print ""
    print "translate 是一个命令行翻译脚本,通过百度翻译接口获取翻译结果,并友好的输出"
    print "使用方法: python translate.py hello 或 python translate.py \"What's your name\" "
    print "  -h,  --help       显示帮助信息"
    print "  -v,  --version    显示版本"
    print "  -e,  --example    显示例句"
    print ""

opts, args = getopt.getopt(sys.argv[1:], "hve", ["help", "version", "example"])

showEg = False
for op, value in opts:
    if op == "-h" or op == "--help":
        usage()
        sys.exit()
    elif op == "-v" or op == "--version":
        print "translate 当前版本:" + VERSION
        sys.exit()
    elif op == "-e" or op == "--example":
        showEg = True
if len(args):
    translate(args[0], showEg)
else:
    print '缺少要翻译的单词或语句'

