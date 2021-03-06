#!/usr/bin/env python2
import employees
import json
import sys
import urllib2
import pygame
import time

scoring_host='scoring.csc.uaf.edu'
#scoring_host='127.0.0.1:8081'
database=[]
index=7

def authorize(department,id,issue,flag_id):
	global database
	global scoring_host
	lookup=employees.search(database,[id],True)
	lookup=json.loads(lookup)
	if len(lookup)>0:
		lookup=lookup[0]
		if lookup['Department Number']==department and lookup['ID']==id and id=='224141' and lookup['Issue Number']<=issue:
			print('Welcome '+lookup['Full Name']+'!')
			try:
				urllib2.urlopen('http://'+scoring_host+'/?flag='+flag_id+str(index)).read()
				pygame.mixer.music.load("../sounds/granted.mp3")
				pygame.mixer.music.play()
				time.sleep(2)
			except Exception:
				pass
			return True
	pygame.mixer.music.load("../sounds/denied.mp3")
	pygame.mixer.music.play()
	time.sleep(2)
	return False

if __name__=="__main__":
	pygame.init()
	try:
		database=employees.load_from_csv('names.csv')
		while True:
			print('Enter the ID of the flag you want to get credit through:')
			flag_id=''
			while True:
				ch=sys.stdin.read(1)
				if ch=='\n':
					break
				flag_id+=ch
			line=''
			print('Scan your card: ')
			while True:
				ch=sys.stdin.read(1)
				if ch=='\n':
					break
				line+=ch
			if len(line)==12 and line[0]==';' and line[-1]=='?':
				try:
					line=line[1:-1]
					department=employees.zero_padded_int(line[:2])
					id=line[2:-2]
					issue=employees.zero_padded_int(line[-2:])
					authorize(department,id,issue,flag_id)
				except Exception as error:
					sys.stderr.write(str(error)+'\n')
	except Exception as error:
		sys.stderr.write(str(error)+'\n')
		exit(1)
