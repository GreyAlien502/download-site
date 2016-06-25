import re
import urllib.request
import os

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
	goodlinklist = [link.decode("ASCII") for link in alllinklist if(link[0:4] !=b"http")]
	return(goodlinklist)
	
def imgget(html):
	ex = re.compile(b'<img[^>]*src="([^"]*)"')
	allimglist = ex.findall(html)
	goodimglist = [img.decode("ASCII") for img in allimglist if(img[0:4] ==b"http")]
	return(goodimglist)

def siteget(siteurl, ignoreurls):
	print(siteurl)
	[path, filename] = os.path.split(siteurl)
	text = urlget(siteurl)
	saveFile(filename, text)

	linkurls = linksget(text)
	imageurls = imgget(text)

	linkurls = [linkurl for linkurl in linkurls if linkurl not in ignoreurls]
	imageurls = [imageurl for imageurl in imageurls if imageurl not in ignoreurls]
	ignoreurls += linkurls + imageurls

	imagenames = [imageurl[imageurl.find(b"//")+2:] for imageurl in imageurls]
	[os.makedirs(os.path.dirname(imagename), exists_ok=True) for imagename in imagenames]
	[saveFile(imagenames[i], urlget(imageurls[i])) for i in range(0,len(imageurls))]

	for linkurl in linkurls:
		ignoreurls = siteget(path+'/'+linkurl, ignoreurls)

	return ignoreurls
