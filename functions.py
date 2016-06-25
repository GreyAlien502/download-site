import requests
import urllib

def saveFile(filename, filecontents):
	f = open(filename, 'w')
	f.write(filecontents)
	f.close()

def urlget(site):
	reqq = urllib.request.urlopen(site)
	reqqs = reqq.read()
	return(reqqs)