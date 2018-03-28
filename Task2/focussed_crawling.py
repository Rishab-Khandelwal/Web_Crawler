from bs4 import BeautifulSoup
import urllib2
import time
import re
from nltk.stem.porter import *
import enchant
# encoding=utf8


d = enchant.Dict("en_US")
stemmer = PorterStemmer()
def webcrawler(url,keywords):
	#page = urllib2.urlopen(url)
	#soup = BeautifulSoup(page)
	pagesToVisit = [url]
	visitedPages = []
	pages_depth = []
	#visitedPages
	urlsCrawled = []
	baseUrl = "https://en.wikipedia.org"
	depth = 0
	FileIndex = 1

	#print(stemmer.stem("running"))
	#print(stemmer.stem("LUNAR"))
	#print(stemmer.stem("MOON"))
	while pagesToVisit and len(visitedPages) < 1000 and depth <= 6  :
		page = pagesToVisit.pop(0)
		print "I reached here" , len(visitedPages)
		print "depth is ", depth
		if page not in visitedPages:
			#time.sleep(1)
			#print "The page to open is ", page

			pageToprocess = urllib2.urlopen(page)
			soup = BeautifulSoup(pageToprocess,"html.parser")
			fileName = 'file_' + str(FileIndex) + '.txt'
			urlFileName = 'Focussed_Urls_list.txt'
			#file = open(fileName,'w')
			file1 = open(urlFileName,'a')
			file1.write(str(FileIndex) + "." + " " + page + "\n")
			#file.write(page.encode("utf-8") + "\n" + soup.prettify().encode("utf-8"))
			FileIndex = FileIndex + 1
			#file.close()
			file1.close()
			soup1 = soup.findAll('div', attrs =  {'id' : 'bodyContent'})
			for div in soup1:
				for link in div.findAll('a',{'href' : re.compile('^/wiki/')}):
					hrefpages = link.get('href')
					anchorText = link.text.encode("utf-8")					
					if ':' in hrefpages:
						continue
					addurl = baseUrl + hrefpages
					if '#' in addurl:
						addurl = addurl[:addurl.index('#')]
					print "the added page is ", addurl
					'''
					flag = False
					for keyword in keywords : 
						regex_link = r'.*' + re.escape(keyword) + r'.*' 
						#print "the regex link is " , regex_link
						link_match = re.search(regex_link, str(addurl) , re.IGNORECASE)
						#print "the link_match is ", link_match
						anchorText_match = re.search(regex_link,anchorText,re.IGNORECASE)
						if (anchorText_match) or (link_match):
							flag = True
'''

					if checkKeyword(addurl, keywords,anchorText) == False:
						continue
					#if flag == False:
					#	continue
					if addurl not in visitedPages:
						pages_depth.append(addurl.encode("utf-8"))	
			visitedPages.append(page)		
		if not pagesToVisit:
			pagesToVisit = pages_depth
			pages_depth = []
			depth += 1
			
	print "depth is ", depth
	print "visitedPages are", len(visitedPages)	
	print "pages to visit" , len(pagesToVisit)	
		
	return visitedPages


def checkKeyword(testurl, keywords,anchorText):
	#response = False
	print "The anchor text is ", anchorText
	'''for keyword in keywords:
		#print "keyword to check is ", keyword

		regex_link = r'.*' + re.escape(keyword) + r'.*' 
		#print "the regex link is " , regex_link
		link_match = re.search(regex_link, str(testurl) , re.IGNORECASE)
		#print "the link_match is ", link_match
		anchorText_match = re.search(regex_link,anchorText,re.IGNORECASE)
		#print "anchor Text matching", anchorText
		
		#print "anchor_Text match is " , anchorText_match
		if (anchorText_match) or (link_match):
			response = True
			return response
	return response'''
	response = False
	arrayoftext = anchorText.split(" ")
	
	print "The test URL is ", testurl
	print "Array of text is ", arrayoftext

	for text in arrayoftext:
		text1 = stemmer.stem(text.decode("utf-8"))
		text1 = text1.lower()
		for keyword in keywords:
			keyword = keyword.lower()
			if text1.startswith(keyword.encode("utf-8")):
				restofText = text1[len(keyword.encode("utf-8")):]
				if len(restofText) == 0 or d.check(restofText):
					return True
			elif text1.endswith(keyword.encode("utf-8")):
				restofText = text1[0:-len(keyword.encode("utf-8"))]
				if len(restofText) == 0 or d.check(restofText):
					return True


	'''for keyword in keywords : 
		regex_link = r'.*' + re.escape(keyword) + r'.*'
		link_match = re.search(regex_link, str(testurl) , re.IGNORECASE)

		if link_match:
			return True

	return False'''

	
	listofStrings = testurl.split("/")
	urlTextCheck = listofStrings[-1]
	ListOfUrlText = urlTextCheck.split("_")
	for textt in ListOfUrlText:
		textt1= stemmer.stem(textt.decode("utf-8"))
		textt1 = textt1.lower()
		for keyword in keywords:
			keyword = keyword.lower() 
			if textt1.startswith(keyword.encode("utf-8")):
				restofText = textt1[len(keyword.encode("utf-8")):]
				if len(restofText) == 0 or d.check(restofText):
					return True
			elif textt1.endswith(keyword.encode("utf-8")):
				restofText = textt1[0:-len(keyword.encode("utf-8"))]
				if len(restofText) == 0 or d.check(restofText):
					return True
					

	return False





keywords = ["Moon", "Lunar"]
crawledpages = webcrawler("https://en.wikipedia.org/wiki/Solar_eclipse",keywords)
print "Crawled pages are" , crawledpages