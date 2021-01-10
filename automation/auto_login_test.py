#!/bin/bash

# 压测脚本模板中设定的压测时间应为300秒
import os,time
import platform

def report_time():
    report_time=time.strftime('%Y_%m_%d_%H_%M',time.localtime())
    return report_time

def test_windows_demo():
    '''windows下执行jmeter'''
    jmx_template="login"
    suffix=".jmx"
    jmx_template_filename=jmx_template+suffix

    # 需要在系统变量中定义jmeter根目录的位置，如下
    # export jmeter_path="/your jmeter path/"

    print( "自动化压测开始")

    # 压测并发数列表
    thread_time=60
    thread_number_array=[10, 20, 40, 80, 150, 300]
    get_report_time=report_time()
    for num in thread_number_array:
        # 生成对应压测线程的jmx文件
        jmx_filename="{}_{}{}".format(jmx_template,num,suffix)
        jtl_filename="test_{}.jtl".format(num)
        web_report_path_name="{}_report_concurrent{}".format(get_report_time,num)

        os.system('del {} {}'.format(jmx_filename,jtl_filename))

        os.system('copy {} {}'.format(jmx_template_filename,jmx_filename))

        print( "生成jmx压测脚本 {}".format(jmx_filename))
        with open(jmx_filename,'r',encoding='utf-8') as f:
            text=f.read()
            test1=text.replace('thread_num', str(num),1)
            test2=test1.replace('thread_time',str(thread_time),1)
        with open(jmx_filename,'w',encoding='utf-8') as f:
            f.write(test2)

        # JMeter 静默压测
        os.system('jmeter -n -t {} -l {}'.format(jmx_filename,jtl_filename))

        # 生成Web压测报告
        os.system('jmeter -g {} -e -o {}'.format(jtl_filename,web_report_path_name))

        os.system('del {} {}'.format(jmx_filename,jtl_filename))

    print( "自动化压测全部结束")

def test_linux_demo():
    '''linux下执行jmeter脚本'''
    os.system('/bin/bash auto_login_test.sh')

def test_jmeter():
    sys=platform.system()
    if sys=="Windows":
        test_windows_demo()
    else:
        test_linux_demo()



if __name__ == '__main__':
   test_jmeter()

