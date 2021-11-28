from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from urllib.error import HTTPError
import re
from selenium import webdriver
import time
# import requests as rq
import os

from datetime import datetime

def CreateDirectory(path = None):
	fullpath = os.getcwd()
	if (path is None): # use current time
		path = datetime.now().strftime("%Y%m%d_%H%M%S")
	fullpath = fullpath + "/" + path
	print(fullpath)
	try:
		os.mkdir(fullpath)
	except OSError:
		print("Creation of the directory %s failed" % path)
		return False, None
	else:
		print("Successfully created the directory %s " % path)
		return True, fullpath


def LoadTiltText(url):
	strTitle = url.find("div", {"id": "subtitle"}).text
	# print(strTitle)
	strText = url.find("div", {"id": "text"})
	strText = str(strText).replace("\n", "").replace("<br/>", "\n")
	strText = soup(strText, "html.parser").find("div", {"id": "text"}).text
	# print(strText)
	return strTitle, strText


def LoadStaticUrl(url):
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	try:
			html = urlopen(req).read()
	except HTTPError as e:
		# return null, break, or do some other "Plan B"
		print("except HTTPError as e:")
		return False, None
	if (html is None):
		return False, None
	page_soup = soup(html, "html.parser")
	# print(page_soup)
	return True, page_soup


def LoadDaynamicUrl(url):
	options = webdriver.ChromeOptions()
	options.add_argument('--headless')
	driver = webdriver.Chrome(options=options)
	driver.get(url)
	time.sleep(1)
	htmlSource = driver.page_source
	page_soup = soup(htmlSource, 'html.parser')
	# print(page_soup)
	return True, page_soup


def GetAllLinks(url):
	links = url.find_all('a', href=re.compile("/read/101904/"))
	listToReturn =[]
	for link in links:
		listToReturn.append("https://www.8book.com" + str(link['href']))
		# print(listToReturn[len(listToReturn) - 1])
	return listToReturn


def WriteFile(folder, strTitle, strText):
	file = folder + "/" + strTitle + ".txt"
	f = open(file, "a")
	f.write(strText)
	f.close
	return True


def main():
	url = "https://www.8book.com/novelbooks/101904/"
	bSuccess, webpage = LoadStaticUrl(url)
	if (not bSuccess):
		print("FAIL LoadStaticUrl(url)")
		return
	bSuccess, folder = CreateDirectory()
	if (not bSuccess):
		return
	urls = GetAllLinks(webpage)
	if (len(urls) <= 0):
		print("len(urls) <= 0)")
		return
	for url in urls:
		print(url)
		bSuccess, webpage = LoadDaynamicUrl(url)
		# print(webpage)
		if (not bSuccess):
			print("FAIL bSuccess, webpage = LoadStaticUrl(url)")
			return
		strTitle, strText = LoadTiltText(webpage)
		bSuccess = WriteFile(folder, strTitle, strText)
		time.sleep(60)
	print("DONE")


if __name__ == '__main__':
	main()