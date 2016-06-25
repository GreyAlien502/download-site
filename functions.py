import requests
import urllib

def saveFile(filename, filecontents):
	f = open(filename, 'wb')
	f.write(bytes(filecontents))
	f.close()

def urlget(site):
	reqq = urllib.request.urlopen(site)
	reqqs = reqq.read()
	return(reqqs)
