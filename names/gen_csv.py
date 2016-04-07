#!/usr/bin/env python
#Usage: ./gen_names.py > names.csv

import employees
import sys

if __name__=="__main__":
	try:
		database=employees.gen_from_names('names.txt')
		counts={}
		for ee in database:
			if ee.department.initials not in counts:
				counts[ee.department.initials]=0
			counts[ee.department.initials]+=1
			print(ee.csv())
		for cc in counts:
			sys.stderr.write(cc+'='+str(counts[cc])+'\n')
		exit(0)
	except Exception as error:
		sys.stderr.write(str(error)+'\n')
		exit(1)
