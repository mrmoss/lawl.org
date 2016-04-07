#!/usr/bin/env python
import employees
import json
import sys

database=[]

def authorize(department,id,issue):
	global database
	lookup=employees.search(database,[id])
	lookup=json.loads(lookup)
	if len(lookup)>0:
		print('Welcome '+lookup[0]['Full Name']+'!')
		return True
	return False

if __name__=="__main__":
	database=employees.load_from_csv('names.csv')
	while True:
		line=''
		while True:
			ch=sys.stdin.read(1)
			if ch=='\n':
				break
			line+=ch
		if len(line)==14 and line[0]==';' and line[-1]=='?':
			line=line[1:-1]
			department=line[:2]
			id=line[2:-2]
			issue=line[-2:]
			authorize(department,id,issue)