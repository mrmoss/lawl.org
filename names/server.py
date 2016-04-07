#!/usr/bin/env python
import SimpleHTTPServer
import BaseHTTPServer
import re
import sys
import urllib
import urlparse

database=[]

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		try:
			global database
			query_str=urlparse.urlparse(self.path).query

			if len(query_str)==0:
				file=open('web/index.html','r')
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				self.wfile.write(file.read())
				self.wfile.close()
			else:
				for query in query_str.split('&'):
					query=query.split('=')
					if len(query)>1:
						key=query[0]
						val=urllib.unquote(query[1])
						if key=='search':
							found=[]
							val=re.sub('[^0-9a-zA-Z]+',' ',val).lower().split(' ')

							for ii in val:
								if len(ii)>3:
									for jj in range(0,len(database)):
										for kk in range(0,len(database[jj])):
											if kk!=1 and ii in database[jj][kk].lower():
												found.append(database[jj][2:])
												break
							self.send_response(200)
							self.send_header('Content-type','text/html')
							self.end_headers()
							self.wfile.write(str(found))
							self.wfile.close()
		except Exception as error:
			sys.stderr.write(str(error)+'\n')
			pass

try:
	file=open('names_out.txt','r')
	for line in file:
		line=line.strip()
		line=line.split(',')
		if len(line)==6:
			database.append(line)
	Handler=MyHandler
	server=BaseHTTPServer.HTTPServer(('127.0.0.1',8080),MyHandler)
	server.serve_forever()
except Exception as error:
	sys.stderr.write(str(error)+'\n')
	exit(1)