#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
	利用tarfile实现Linux上的简易版tar命令
	tar -czvf tarname file1 file2
	tar -xzvf tarname
	tar -cjvf zipfile f1 file2
	tar -xjvf zipfile
	等。参数可以随意组合
'''

import getopt,os.path,os
import sys,tarfile,bz2

rw = fmt = dest_path = tar_name =args =''
show=c= False
def parse_args():
	'''接收命令行参数'''
	global c,show,dest_path,tar_name,rw,fmt,args
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
				if show:
					fullpath = os.path.join(root,f)
					print(fullpath)
				tar.add(f)
	tar.close()

def decompression():
	'''解压缩'''
	print(os.path.join(os.getcwd(),os.path.basename(tar_name).split('.')[0]))
	
	etar = tarfile.open(os.path.join(os.getcwd(),dest_path,tar_name),rw+':'+fmt)
	for tarinfo in etar:
		etar.extract(tarinfo, os.path.basename(tar_name).split('.')[0])	
	etar.close()

def main():
	parse_args()
	if c:
		create_tarfile(os.getcwd())
	else:
		decompression()

if __name__ == '__main__':
	main()
