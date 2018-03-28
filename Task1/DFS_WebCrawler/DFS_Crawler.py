from bs4 import BeautifulSoup
import urllib2
import time
import re




visitedPages = []

def webcrawler(url):
	#page = urllib2.urlopen(url)
	#soup = BeautifulSoup(page)
	pagesToVisit = [url]
	global visitedPages
	pages_depth = []
	#visitedPages
	urlsCrawled = []
	baseUrl = "https://en.wikipedia.org"
	depth = 0
	FileIndex = 1
	while pagesToVisit and len(visitedPages) < 1000:
		page = pagesToVisit.pop(0)
		depth = depth + 1
		#print "I reached here" , len(visitedPages)
		#print "depth is ", depth
		if page not in visitedPages:
			time.sleep(1)
			pos = 0
			#print "The page to open is ", page
			pageToprocess = urllib2.urlopen(page)
			soup = BeautifulSoup(pageToprocess,"html.parser")
			tag =  soup.find('html' , attrs = {'lang':'en'})
			#print "Language of the tpage is " , tag.get('lang')
			# Handling non-english articles
			if (tag.get('lang') != 'en'):
				continue
			#fileName = 'file_' + str(FileIndex) + '.txt'
			urlFileName = 'DFS_Urls_list.txt'
			#print "FileName is \n" , fileName
			#file = open(fileName,'w')
			file1 = open(urlFileName,'a')
			#file1.write(str(FileIndex) + "." + " " + page + "\n")
			file1.write(page + "\n")
			#file.write(page.encode("utf-8") + "\n" + soup.prettify().encode("utf-8"))
			FileIndex = FileIndex + 1
			#file.close()
			file1.close()
			soup = soup.findAll('div', attrs =  {'id' : 'bodyContent'})
			for div in soup:
				for link in div.findAll('a',{'href' : re.compile('^/wiki/')}):
					hrefpages = link.get('href')
					
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
					if '#' in addurl:
						addurl = addurl[:addurl.index('#')]
					#print "the added page is ", addurl
					if depth > 6:
						continue
					pagesToVisit.insert(pos,addurl)
					pos = pos+1
						
				
			visitedPages.append(page)
	print "depth is ", depth
	print "visitedPages are", len(visitedPages)		
		
	return visitedPages



def main():
	start = time.time()
	#print("hello")
	crawledpages = webcrawler("https://en.wikipedia.org/wiki/Solar_eclipse")
	print "Crawled pages are" , crawledpages
	end = time.time()
	print "time elapsed is " , end - start


if __name__ == "__main__" : main()