#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Created on 2014-12-30
在windows上实现linux的scp功能，利用paramiko提供的SSH
@author: Bernie.xiong
'''

import sys,time
import paramiko
import getpass
import os.path
#import threading,multiprocessing
import thread

ssh=sftp=name=pwd=ip=host_str=local=remote =file_name = ''
put = True

def parse_args():
    '''解析命令行参数'''
    #TODO 还需考虑到目录
    global name,ip,remote,host_str,put,local,file_name
    if len(sys.argv) == 3:
        if '@' in sys.argv[1]:
            put = False
            host_str = sys.argv[1]
            local = sys.argv[2]
        elif '@' in sys.argv[2]:
            host_str= sys.argv[2]
            local = sys.argv[1]
    else:
        print('''The input format error Please input:  scp localpath remotepath''')
        return
        
    name = host_str[0:host_str.index('@')]
    ip = host_str[host_str.index('@') + 1:host_str.index(':')]
    remote= host_str[host_str.index(':') + 1:]
    
    if put:
        if '/' in local:
            file_name = os.path.split(local)[1]
        else:
            file_name = local
    else:
        file_name = os.path.split(remote)[1]

def exe_cmd():
    '''利用paramiko实现scp功能'''
    global pwd,remote,local,file_name,ssh,sftp
    pwd = getpass.getpass('{0}@{1}`s password:'.format(name,ip))
    try:
        ssh,sftp,scp = ssh_login(pwd)
    except:
        print('Permission denied, please try again.')
        return
    if put:
        size = os.path.getsize(local)
        thread.start_new_thread(sftp.put,(local,remote+'/'+file_name))
        while(1):
            time.sleep(1)
            stdin,stdout,stderr=ssh.exec_command('du -s '+remote+'/'+file_name)
            n=stdout.readlines()[0].split()[0]
            bili=float(n)/float(size/1024)*100
            view_bar(bili,100,bar_word="#")
            if int(bili) == 100:
                break
        print('finish.')
        #sftp.put(local,remote+'/'+file_name)
    else:
        #sftp.get(remote,local+'/'+file_name)
        thread.start_new_thread(sftp.get,(remote,local+'/'+file_name))
        while(True):
            time.sleep(1)
            n = os.path.getsize(local+'/'+file_name)
            stdin,stdout,stderr=ssh.exec_command('du -s '+remote)
            size=stdout.readlines()[0].split()[0]
            bili=float(n/1024)/float(size)*100
            view_bar(bili,100,bar_word="#")
            if int(bili) == 100:
                break
        print('finish.')
        
    scp.close()
    sftp.close()
        
'''
def progress(src_path,dest_path,fun,src_size,dest_size):
    thread.start_new_thread(fun,(src_path,dest_path))
    while(1):
        time.sleep(1)
        bili=float(src_size)/float(dest_size)*100
        view_bar(bili,100,bar_word="#")
        if int(bili) == 100:
            break
    print('finish.')
'''
      
def view_bar(num=1, sum=100, bar_word=":"):
    rate= float(num) / float(sum)
    rate_num = int(rate * 100)
    print '\r%d%% :' %(rate_num),
    for i in range(int(num)/5):
        os.write(1, bar_word)
    sys.stdout.flush()
    
    
def ssh_login(pwd):
    client = paramiko.SSHClient()  
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
    client.connect(ip, 22, name, pwd)
    
    scp=paramiko.Transport((ip,22))
    scp.connect(username=name,password=pwd)
    sftp=paramiko.SFTPClient.from_transport(scp)
    return client,sftp,scp  
        
def main():
    parse_args()
    exe_cmd()
    
    
if __name__ == '__main__':
    main()
