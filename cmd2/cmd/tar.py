#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
	利用tarfile实现Linux上的简易版tar命令,主要实现 压缩，解压，列举三个功能
	tar -czvf tarname file1 file2
	tar -xzvf tarname
	tar -tzvf tarname
	tar -cjvf zipfile f1 file2
	tar -xjvf zipfile
	等。参数可以随意组合
'''

import getopt,os.path,os
import sys,tarfile,bz2

rw = fmt = dest_path = tar_name =args = ''
show=c=ls= False
def parse_args():
	'''接收命令行参数'''
	global c,show,dest_path,tar_name,rw,fmt,args,ls
	try:
	    opts, args = getopt.getopt(sys.argv[1:],"cxzvjtf:",["create","extract","gz","view","bzip2","list","file="])
	except getopt.GetoptError, err:
	    # print help information and exit:
	    usage()
	    sys.exit(2)
	for o,a in opts:
		if o in ('-c','--create'):
			rw = 'w'
			c = True
		elif o in ('-x','--extract'):
			rw = 'r'
		elif o in ('-v','--view'):
			show = True
		elif o in ('-z','--gz'):
			fmt = 'gz'
		elif o in ('-j','--bzip2'):
			fmt = 'bz2'	
		elif o in ('-t','--list'):
			ls = True
		elif o in ('-f','--file'):
			if '/' or '\\' in a:
				dest_path,tar_name = os.path.split(a)
			else:
				dest_path = tar_name = a

def create_tarfile(src_path):
	'''创建压缩包'''
	tar = tarfile.open(os.path.join(dest_path,tar_name),rw+':'+fmt)
	for root,dirs,files in os.walk(src_path):
		for f in files:
			if f in args:
				fullpath = os.path.join(root,f)
				if show:
					print(fullpath)
				tar.add(f)
		for d in dirs:
			if d in args:
				fullpath = os.path.join(root,d)
				if show:
					print(fullpath)
				tar.add(d)
	tar.close()

def decompression():
	'''解压缩'''
	etar = tarfile.open(os.path.join(os.getcwd(),dest_path,tar_name),rw+':'+fmt)
	for tarinfo in etar:
		import time
		timeArray = time.localtime(tarinfo.mtime)
		d = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
		if show:
			print('{0}k  {1}  {2}'.format(str(tarinfo.size).rjust(5),d,tarinfo.name))
		if not ls:
			etar.extract(tarinfo, os.path.basename(tar_name).split('.')[0])	
	
	if not ls:
		print('\ndecompression to:%s' %os.path.join(os.getcwd(),os.path.basename(tar_name).split('.')[0]))
	etar.close()


def main():
	parse_args()
	if c:
		create_tarfile(os.getcwd())
	else:
		decompression()

if __name__ == '__main__':
	main()
