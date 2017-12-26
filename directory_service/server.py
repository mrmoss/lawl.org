#!/usr/bin/env python2
import SimpleHTTPServer
import BaseHTTPServer
import employees
import os
import mimetypes
import re
import sys
import urllib
import urlparse

database=[]

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		try:
			global database
			self.path=self.path.split('?')
			query_str='?'.join(self.path[1:])
			if len(query_str)>0:
				print(query_str)
				for query in query_str.split('&'):
					query=query.split('=')
					if len(query)>1:
						key=query[0]
						val=urllib.unquote(query[1])
						if key=='search':
							val=re.sub('[^0-9a-zA-Z]+',' ',val).lower().split(' ')
							self.send_response(200)
							self.send_header('Content-type','text/html')
							self.end_headers()
							self.wfile.write(str(employees.search(database,val,False,True)))
							self.wfile.close()
							return
			self.path=self.path[0]
			if len(self.path)>0 and self.path[-1]=='/':
				self.path+='index.html'
			cwd=os.getcwd()+'/web/'
			self.path=os.path.abspath(cwd+self.path)
			if self.path.find(cwd)!=0 or not os.path.isfile(self.path):
				self.send_response(404)
				self.end_headers()
				return
			file=open(self.path,'r')
			self.send_response(200)
			mime=mimetypes.guess_type(self.path)
			if len(mime)>0:
				mime=mime[0]
			else:
				mime='text/plain'
			print(mime+' '+self.path)
			self.send_header('Content-type',mime)
			self.end_headers()
			self.wfile.write(file.read())
			self.wfile.close()
		except Exception as error:
			print(error)
			self.send_response(401)

if __name__=="__main__":
	try:
		database=employees.load_from_csv('names.csv')
		Handler=MyHandler
		server=BaseHTTPServer.HTTPServer(('0.0.0.0',8081),MyHandler)
		server.serve_forever()
	except Exception as error:
		sys.stderr.write(str(error)+'\n')
		exit(1)
