'''
Created on 2014-12-30

@author: Bernie.xiong
'''

import sys,time
import paramiko
import os.path
import getpass
import os.path

name=pwd=ip=host_str=local=remote =file_name = ''
put = True

def parse_args():
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
        
    name = host_str[0:host_str.index('@')]
    ip = host_str[host_str.index('@') + 1:host_str.index(':')]
    remote= host_str[host_str.index(':') + 1:]
    
    if put:
        if '/' in local:
            file_name = os.path.split(local)[1]
            print(file_name)
        else:
            file_name = local
    else:
        pass
    
  
def progres(size):
    j='#'
    for i in range(1,size+1):
        j += '#'
        sys.stdout.write(str(int((i/size)*100))+'%['+j+']'+"\r" )
        sys.stdout.flush()
        time.sleep(0.5)
    
def exe_cmd():
    global pwd,remote,local,file_name
    print(name,ip,remote,file_name)
    pwd = getpass.getpass('{0}@{1}`s password:'.format(name,ip))
    try:
        scp=paramiko.Transport((ip,22))
        scp.connect(username=name,password=pwd)
        sftp=paramiko.SFTPClient.from_transport(scp)
    except:
        pass
    if put:
        size = os.path.getsize(local)
        #progres(size/1024/1024)
        sftp.put(local,remote+'/'+file_name)
    else:
        sftp.get(remote,local+'/'+file_name)
        
    scp.close()
    sftp.close()
        
if __name__ == '__main__':
    parse_args()
    exe_cmd()
    #print(name,ip,path,pwd)