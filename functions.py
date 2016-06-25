import re
import urllib.request

def saveFile(filename, filecontents):
	f = open(filename, 'wb')
	f.write(bytes(filecontents))
	f.close()

def urlget(site):
	reqq = urllib.request.urlopen(site)
	reqqs = reqq.read()
	return(reqqs)

def linksget(html):
	ex = re.compile(b'<a[^>]*href="([^"]*)"')
	alllinklist = ex.findall(html)
	goodlinklist = [link for link in alllinklist if(link[0:4] !=b"http")]
	return(goodlinklist)
	
def imgget(html):
	ex = re.compile(b'<img[^>]*src="([^"]*)"')
	allimglist = ex.findall(html)
	goodimglist = [img for img in allimglist if(img[0:4] ==b"http")]
	return(goodimglist)