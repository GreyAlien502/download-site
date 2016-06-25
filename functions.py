import re
import urllib.request
import urllib.error
import os
import time

def saveFile(filename, filecontents):
	f = open(filename, 'wb')
	f.write(bytes(filecontents))
	f.close()

def urlget(site):
	reqq = urllib.request.urlopen(site)
	reqqs = reqq.read()
	return(reqqs)

def linksget(html):
	ex = re.compile(b'<a href="([^"]*)"')
	alllinklist = ex.findall(html)
	goodlinklist = [link.decode("ASCII") for link in alllinklist if(link[0:4] !=b"http")]
	return(goodlinklist)
	
def imgget(html):
	ex = re.compile(b'<img src="([^"]*)"')
	allimglist = ex.findall(html)
	goodimglist = [img.decode("ASCII") for img in allimglist if(img[0:4] ==b"http")]
	return(goodimglist)

def siteget(siteurl, ignoreurls):
	print(siteurl)
	[path, filename] = os.path.split(siteurl)
	urlgot = False
	while(not urlgot):
		try:
			text = urlget(siteurl)
			urlgot = True
		except urllib.error.HTTPError as exc:
			if exc.code == 508:
				print(508)
				time.sleep(10)
			else:
				print(exc)
				return ignoreurls+[siteurl]
	if(text.find(b"<body>admin area") != -1):
		return ignoreurls+[siteurl]

	saveFile(filename, text)

	linkurls = linksget(text)
	imageurls = imgget(text)

	linkurls = [linkurl for linkurl in linkurls if linkurl not in ignoreurls]
	imageurls = [imageurl for imageurl in imageurls if imageurl not in ignoreurls]
	ignoreurls += linkurls + imageurls

	imagenames = [imageurl[imageurl.find("//")+2:] for imageurl in imageurls]
	for i in range(0,len(imageurls)):
		os.makedirs(os.path.dirname(imagenames[i]), exist_ok=True)
		try:
			saveFile(imagenames[i], urlget(imageurls[i]))
		except:
			print("Could not download "+imageurls[i]+".")

	for linkurl in linkurls:
		ignoreurls = siteget(path+'/'+linkurl, ignoreurls)

	return ignoreurls
