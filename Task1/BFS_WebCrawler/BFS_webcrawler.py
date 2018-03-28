from bs4 import BeautifulSoup
import urllib2
import time
import re


#Following is the code for web crawling using the BFS approach
def webcrawler(url):
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
	while pagesToVisit and depth <= 6 and len(visitedPages) < 1000:
		page = pagesToVisit.pop(0)
		#print "I reached here" , len(visitedPages)
		#print "depth is ", depth
		if page not in visitedPages:
			#delay of 1 second due to politeness policy
			time.sleep(1)
			#print "The page to open is ", page
			pageToprocess = urllib2.urlopen(page)
			soup = BeautifulSoup(pageToprocess,"html.parser")
			tag =  soup.find('html' , attrs = {'lang':'en'})
			#print "Language of the tpage is " , tag.get('lang')
			# Handling non-english articles
			if (tag.get('lang') != 'en'):
				continue
			fileName = 'file_' + str(FileIndex) + '.txt'
			urlFileName = 'BFS_Urls_list.txt'
			#print "FileName is \n" , fileName
			file = open(fileName,'w')
			file1 = open(urlFileName,'a')
			
			#file1.write(str(FileIndex) + "." + " " + page + "\n")
			file1.write(page + "\n")
			
			file.write(page.encode("utf-8") + "\n" + soup.prettify().encode("utf-8"))
			FileIndex = FileIndex + 1
			file.close()
			file1.close()
			# crawling only the body content and ignoring the the links which are outside the body content

			soup1 = soup.findAll('div', attrs =  {'id' : 'bodyContent'})
			for div in soup1:
				for link in div.findAll('a',{'href' : re.compile('^/wiki/')}):
					hrefpages = link.get('href')
					# avoiding the administrative links containing ':''.
					# also avoiding the image links and non textiual links
					if ':' in hrefpages:
						continue
					if 'Main_Page' in hrefpages:
						continue
					if '.jpeg' in hrefpages: 
						continue
					if '.png' in hrefpages:
						continue	
					if '.jpg' in hrefpages: 
						continue
					if '.gif' in hrefpages: 
						continue 
					if '.tif' in hrefpages: 
						continue 
					if  '.txt' in hrefpages:
						continue
					'''if ':' in hrefpages:
						continue
					addurl = baseUrl + hrefpages
					
					print "the added url is" , addurl
					if addurl is not  None:'''
					addurl = baseUrl + hrefpages
					# handling urls which containing # which are sections within the same page
					if '#' in addurl:
						addurl = addurl[:addurl.index('#')]
					#print "the added page is ", addurl
					pages_depth.append(addurl)
					
					if not pagesToVisit:
						pagesToVisit = pages_depth
						pages_depth = []
						depth = depth + 1
						print "depth is ", depth
			visitedPages.append(page)
	print "depth is ", depth
	print "visitedPages are", len(visitedPages)		
		
	return visitedPages


start = time.time()
	#print("hello")
crawledpages = webcrawler("https://en.wikipedia.org/wiki/Solar_eclipse")
print "Crawled pages are" , crawledpages
end = time.time()
print "time elapsed is " , end - start

