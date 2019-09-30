#web_scraping_prototype

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
from time import sleep
from text_sum import make_summary
from bs4 import BeautifulSoup
import bs4

def bbc_search(phrase):
	#while True:
	#search = input("Enter an item to search: ")
	search = phrase
	search = '+'.join(search.split())
	url = "https://www.bbc.co.uk/search?q="+search+"&filter=news"

	#print(url)
	page = requests.get(url)
	#print(page.text[:1000])
	soup = BeautifulSoup(page.text, 'html5lib')
	#print(soup)
	#soup = soup.prettify()
	page_urls = soup.find_all('h1',attrs={'itemprop':"headline"})

	links = []
	for page_url in page_urls:
		children = page_url.findChildren("a" , recursive=False)
		#print(children)
		links.append(children[0]['href'])
	print(links)
	get_content(links[2])

def bbc_webpage_to_text(link):
	print(link)
	page = requests.get(link)
	#print(page.text[:1000])
	soup = BeautifulSoup(page.text, 'html5lib')

	body_content = soup.find_all('div',attrs={'property':"articleBody"})

	#print(body_content)

	sentence_list = body_content[0].find_all('p')
	print(sentence_list)
	video_check = soup.find_all('video')
	print(video_check)
	if len(video_check)>0:
		print("This is a video based article")
		quit()

	text = []
	for sentence in sentence_list:
		text.append(sentence.contents[0])

	print(text)
	text= ''.join(text)

	print(text,'\n\n\n')
	#make_summary(text)

def start_browser():

	dir = os.path.dirname(__file__)
	chrome_driver_path = dir + "/chromedriver.exe"
	chrome_options = Options()
	#"https://www.aljazeera.com/Search/?q="+searchchrome_options.add_argument("--headless")
	#chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'
	# create a new Chrome session

	return webdriver.Chrome(options=chrome_options)

def cnn_search(phrase):

	driver = start_browser()

	search = phrase
	search = '+'.join(search.split())

	driver.get("https://www.aljazeera.com/Search/?q="+search)
	sleep(20)
	articles = driver.find_elements_by_xpath("//div[@class='row topics-sec-item   ']")

	article_links = []

	for article in articles:
		#print(article.text)
		exact_article = article.find_element_by_xpath("div[@class='col-sm-7 topics-sec-item-cont']")
		article_link = exact_article.find_element_by_xpath("a")
		# print(exact_article.text)
		print(article_link.get_attribute('href'))
		if phrase in article_link.text.lower():
			article_links.append(article_link.get_attribute('href'))

	driver.close()

	#print(article_links)

	for article_link in article_links:
		cnn_webpage_to_text(article_link)

	# cnn_webpage_to_text(article_links[0])

def cnn_webpage_to_text(link):

	#print('a')
	page = requests.get(link)
	#print(page.text[:1000])
	soup = BeautifulSoup(page.text, 'html5lib')

	body_content = soup.find('div',attrs={'class':"article-p-wrapper"})

	sentence_list = body_content.find_all('p')

	text = []
	for sentence in sentence_list:
		#print(sentence)
		if isinstance(sentence.contents[0],bs4.element.NavigableString):
			text.append(sentence.contents[0])

	# print(text)
	text= ''.join(text)

	try:
		print(text,'\n')
	except Exception as e:
		print('error')
		pass

if __name__ == '__main__':
	cnn_search('huawei')