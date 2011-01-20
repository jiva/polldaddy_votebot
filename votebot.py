#!/usr/bin/env python

# http://polldaddy.com/vote.php?va=40&pt=0&r=1&p=2934942&a=13907341&o=&t=62580&token=36af0d9a1090f413f9e1d840eb599d35
# http://polldaddy.com/community/poll/2934942/

# votebot.py by jiva

import urllib
import re
import time
import random
import sys
import commands

proxies = []
port = {}

def updateproxies():
	global proxies
	global port
	print 'updating proxies'
	proxies =[]
	#urllib.urlcleanup()
	for i in range(1,73):
		if i < 10:
			#fd = urllib.urlopen('http://www.samair.ru/proxy/proxy-0' + str(i) + '.htm')
			addy = 'http://www.samair.ru/proxy/proxy-0' + str(i) + '.htm'
			(status, output) = commands.getstatusoutput('curl -m 20 ' + addy)
		else:
			#fd = urllib.urlopen('http://www.samair.ru/proxy/proxy-' + str(i) + '.htm')
			addy = 'http://www.samair.ru/proxy/proxy-' + str(i) + '.htm'
			(status, output) = commands.getstatusoutput('curl -m 20 ' + addy)
		txt = output
		# get his gay-ass-port-naming scheme
		msx = re.findall(r'(\w=\d;+)', txt)
		if msx:
			port = {}
			for mx in msx:
				port[mx.split(";")[0].split("=")[0]] = mx.split(";")[0].split("=")[1]
		else:
			continue
		
		#get IPs, apply port rules, add to list
		msy = re.findall(r'(\d+\.\d+\.\d+\.\d+).+?write\(...(.+?)\)', txt)
		for (ip, enc) in msy:
			#print ip + '\t' + enc
			enn = enc.split('+')
			portnum = ''
			for en in enn:
				if en != '':
					portnum = portnum + str(port[en])
			#print ip + '\t' + portnum
			proxies.append(ip + ':' + str(portnum))
		time.sleep(1)
	#urllib.urlcleanup()
	#print 'num of proxies from up()' + str(len(proxies))
	vote()

cgood=0
cbad=0
def vote():
	#print 'num of proxies from vote()' + str(len(proxies))
	global proxies
	global cgood
	global cbad
	# for i in range(5):
		# for i in range(len(proxies)):
	while True:
		try:
			time.sleep(random.randint(10,20))
			urllib.urlcleanup()
			fd = urllib.urlopen('http://polldaddy.com/community/poll/2934942/')
			txt = fd.read()
			#(status, output) = commands.getstatusoutput('curl -x ' + proxies[i] + ' -m 20 http://polldaddy.com/community/poll/2934942/')
			#(status, output) = commands.getstatusoutput('curl -x -m 30 http://polldaddy.com/community/poll/2934942/')
			m = re.findall(r'vote\(2934942,0,1,0,40,(\d+),[\'](\w+)[\']', txt)
			if m:
				t = m[0][0]
				token = m[0][1]
				votestring = 'http://polldaddy.com/vote.php?va=40&pt=0&r=1&p=2934942&a=13907341&o=&t=' + str(t) + '&token=' + str(token)
				fd2 = urllib.urlopen(votestring)
				result = fd2.read()
				#(status, output) = commands.getstatusoutput('curl -x ' + proxies[i] + ' -m 20 ' + votestring)
				#(status, output) = commands.getstatusoutput('curl -x -m 30 ' + votestring)
				m2 = re.findall(r'Thank you for voting', result)
				m3 = re.findall(r'Thank you, we have already counted your vote', result)
				if m2:
					cgood = cgood+1
					f = open('out.txt', 'a')
					#print "Vote Good\t" + "good: " + str(cgood) + "\tbad: " + str(cbad)
					f.write("Vote Good\t" + "good: " + str(cgood) + "\tbad: " + str(cbad) + '\n')
					f.close()
				elif m3:
					cbad = cbad+1
					f = open('out.txt', 'a')
					#print "Vote Badd\t" + "good: " + str(cgood) + "\tbad: " + str(cbad)
					f.write("Vote Badd\t" + "good: " + str(cgood) + "\tbad: " + str(cbad) + '\n')
					f.close()
				else:
					f = open('out.txt','a')
					#print "Unknown"
					f.write('Unknown' + '\n')
					f.close()
			else:
				f = open('out.txt','a')
				#print 'Cant find vote()'
				f.write('Cant find vote()' + '\n')
				f.close()
			urllib.urlcleanup()
		except:
			print "Error"
	#updateproxies()

def main():
	# RELEASE THE KRAKEN !!
	#updateproxies()
	vote()

if __name__ == "__main__":
	main()
