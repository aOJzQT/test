#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import ConfigParser
import logging
import json
import re

# 粘贴需要转换的GoAgent格式的ip到3个单引号(''')中
ip_goagent = '''

1.1.1.85|1.1.1.115|
1.1.1.112|

1.1.1.152
'''


# 粘贴需要转换的GoProxy格式的ip到3个单引号(''')中
ip_goproxy = '''


"1.1.1.85","1.1.1.115","1.1.1.152",

"1.1.1.112",
'''

# 转换方式
GOAGENT_TO_GOPROXY = 1  # GoAgent ip -> GoProxy ip
GOPROXY_TO_GOAGENT = 2  # GoProxy ip -> GoAgent ip

# 增加日志输出
logging.basicConfig(format="%(asctime)s - [%(levelname)s] %(message)s ",
                    # datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.DEBUG)


def convert_ip(ip_goagent, ip_goproxy, action=GOAGENT_TO_GOPROXY, auto_read=True):
    """GoAgent ip <--> GoProxy ip 转换

    ip_goagent: GoAgent ip
    ip_goproxy: GoProxy ip
    action:     转换方式/方向
    auto_read:  是否自动从配置文件<proxy.ini/iplist.json>中读取google_hk的ip (默认True)
    """
    ip_result = set()
    if action not in(GOAGENT_TO_GOPROXY, GOPROXY_TO_GOAGENT):
        raise Exception("invalid prompt, exit!")

    if action == GOAGENT_TO_GOPROXY:
        config_filename = "proxy.ini"
        if auto_read:
            logging.debug("reading from [%s]" % config_filename)
            config = ConfigParser.ConfigParser()
            config.read(config_filename)
            options = config.options("iplist")
            for option in options:
                if option == "google_hk":
                    ip_goagent = config.get("iplist", option)
                    ip_list = ip_goagent.strip(os.linesep).strip('|').split('|')
        else:
            # 从手动输入的ip中读取
            ip_list = ip_goagent.strip(os.linesep).strip('|').split('|')

        bracket = '"'
    elif action == GOPROXY_TO_GOAGENT:
        config_filename = "iplist.json"
        if auto_read:
            logging.debug("reading from [%s]" % config_filename)
            with open(config_filename, "r") as json_file:
                raw_data = json_file.read()
                # iplist.json可能含有非标准格式的注释，会导致解析会出错(http://jsonlint.com/)
                # 需要remove掉所有注释再解析
                pattern = re.compile(r"//.*")
                raw_data = pattern.sub("", raw_data)
                json_data = json.loads(raw_data)
                ip_goproxy = ",".join(json_data['iplist']['google_hk'])
                ip_list = ip_goproxy.replace('"', '').split(',')
        else:
            # 从手动输入的ip中读取
            ip_list = ip_goproxy.replace('"', '').split(',')

        bracket = ''

    # 将ip加到set中
    for i in ip_list:
        ip_formated = "{0}{1}{0}".format(bracket, i.strip(os.linesep))
        ip_result.add(ip_formated)

    ip_result = sorted(ip_result)
    return "|".join(ip_result) if action == GOPROXY_TO_GOAGENT else ",".join(ip_result)


def main():
    prompt = raw_input("""
    请指定转换方式:
    1. GoAgent --> GoProxy
    2. GoProxy --> GoAgent

    """)
    auto_prompt = raw_input("""
    请指定自动/手动转换方式:
    1. 自动转换（自动读取GoAgent或GoProxy的配置文件）
    2. 手动转换 (需要自行粘贴ip到本脚本中）

    * 默认为自动转换
    * 执行以后会在脚本当前目录生成NewIP-xx.txt文件
    """)
    flag = -1
    auto_read = True
    if prompt == "1":
        flag = GOAGENT_TO_GOPROXY
    elif prompt == "2":
        flag = GOPROXY_TO_GOAGENT
    else:
        err_msg = "无效的转换方式, exit!"
        logging.error(err_msg)
        raise Exception(err_msg)

    if auto_prompt == "1":
        auto_read = True
    elif auto_prompt == "2":
        auto_read = False

    result = convert_ip(ip_goagent, ip_goproxy, flag, auto_read=auto_read)
    filename = r"NewIP-{0}.txt".format(time.strftime("%H_%M_%S", time.localtime()))
    with open(filename, "w") as out:
        out.write(result)
        logging.info("转换完成, 请打开文件[{0}]查看".format(filename))


if __name__ == '__main__':
    main()
