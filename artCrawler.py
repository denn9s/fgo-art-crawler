import urllib.request
import urllib.error
import urllib.parse

import os

from bs4 import BeautifulSoup

from collections import defaultdict


MAIN_PAGE = 'https://grandorder.wiki'
BASE_URL = 'https://grandorder.wiki/Servant_List'
BASE_IMAGE_DIR = 'ServantImages/'
CLASS_LIST = ['Saber', 'Archer', 'Lancer', 'Caster', 'Rider', 'Assassin', 'Ruler', 'Avenger', 'Moon Cancer', 'Alter-Ego', 'Foreigner', 'Berserker', 'Shielder', 'Beast']
EXTRA_CHARACTER_LIST = ['Beast', 'Solomon']
SERVANT_NAME_LIST = []
SERVANT_LINK_LIST = []
SERVANT_DICTIONARY = {} # key = servant name, value = link
SERVANT_IMAGE_DICTIONARY = defaultdict(list) # key = servant name, value = list of links
SERVANT_IMAGE_DICTIONARY_DIRECT = defaultdict(list) # key = servant name, value = list of direct image links

def main():

	opener = urllib.request.build_opener()
	opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
	urllib.request.install_opener(opener)

	# createServantListHTML() # comment out if HTML creation isn't needed anymore
	soup = createSoup()
	createTitleList(soup)
	createServantPageLinks()
	createServantPageLinksHTML() # comment out if no need to update servant link .txt file
	importServantList()
	for servant in SERVANT_DICTIONARY:
		createServantImageLinks(servant)
		createImagePages(servant)
		generateFolder(servant)
		downloadImages(servant)

def createServantListHTML():
	request = urllib.request.Request(BASE_URL, headers = {'User-Agent': 'Mozilla/5.0'})
	response = urllib.request.urlopen(request)
	content = response.read()

	file = open('servantListPage.html', 'wb')
	file.write(content)
	file.close

def createSoup():
	servantListHTML = open('servantListPage.html', encoding = 'utf-8')
	soup = BeautifulSoup(servantListHTML, features = 'html.parser')
	return soup

def createTitleList(soup):
	titleList = []
	for link in soup.find_all('a'):
		title = link.get('title')
		if (checkTitle(title) == True):
			titleList.append(title)
	for index in (range(len(titleList) - 1)):
		if (titleList[index] == titleList[index + 1]):
			SERVANT_NAME_LIST.append(titleList[index])
	SERVANT_NAME_LIST.sort(key = str.lower)

def checkTitle(title):
	if (title is None):
		return False
	if (title in CLASS_LIST):
		return False
	if ('Servants' in title):
		return False
	if ('Friend Points' in title):
		return False
	for character in EXTRA_CHARACTER_LIST:
		if (character in title):
			return False
	return True

def createServantPageLinks():
	for servantName in SERVANT_NAME_LIST:
		underscoreName = servantName.replace(' ', '_')
		baseLink = 'https://grandorder.wiki/'
		servantLink = baseLink + underscoreName
		SERVANT_LINK_LIST.append(servantName)
		SERVANT_LINK_LIST.append(servantLink)

def createServantPageLinksHTML():
	file = open('servantLinks.txt', 'w', encoding = 'utf-8')
	for servant in SERVANT_LINK_LIST:
		file.write('%s\n' % servant)

def importServantList():
	file = open('servantLinks.txt', 'r', encoding = 'utf-8')
	keyValueList = [line.rstrip('\n') for line in file]
	for keyValue in range(len(keyValueList) - 1):
		if (keyValue == 0 or keyValue % 2 == 0):
			SERVANT_DICTIONARY[keyValueList[keyValue]] = keyValueList[keyValue + 1]

def createServantImageLinks(servantName):
	imagePrefix = 'Portrait_Servant_'
	servantLink = SERVANT_DICTIONARY[servantName]
	servantLink = modifyUnicodeURL(servantLink)
	request = urllib.request.Request(servantLink, headers = {'User-Agent': 'Mozilla/5.0'})
	response = urllib.request.urlopen(request)
	content = response.read()
	soup = BeautifulSoup(content, features = 'html.parser')
	for img in soup.find_all('a'):
		href = img.get('href')
		if (href != None):
			if (imagePrefix in href):
				SERVANT_IMAGE_DICTIONARY[servantName].append(MAIN_PAGE + href)

def modifyUnicodeURL(inputURL):
	url = inputURL
	url = urllib.parse.urlsplit(url)
	url = list(url)
	url[2] = urllib.parse.quote(url[2])
	url = urllib.parse.urlunsplit(url)
	return url

def createImagePages(servantName):
	links = SERVANT_IMAGE_DICTIONARY[servantName]
	for link in links:
		request = urllib.request.Request(link, headers = {'User-Agent': 'Mozilla/5.0'})
		response = urllib.request.urlopen(request)
		content = response.read()
		soup = BeautifulSoup(content, features = 'html.parser')
		for img in soup.find_all('div', {'class': 'fullImageLink'}, limit = None):
			aTag = img.find('a')
			linkSuffix = aTag.get('href')
			SERVANT_IMAGE_DICTIONARY_DIRECT[servantName].append(MAIN_PAGE + linkSuffix)

def generateFolder(servantName):
	os.makedirs(BASE_IMAGE_DIR + servantName)

def downloadImages(servantName):
	print(servantName)
	total = len(SERVANT_IMAGE_DICTIONARY_DIRECT[servantName])
	imageCounter = 0
	for imageLink in SERVANT_IMAGE_DICTIONARY_DIRECT[servantName]:
		imageCounter += 1
		underscoreName = servantName
		underscoreName = underscoreName.replace(' ', '_')
		if (imageCounter == 5):
			urllib.request.urlretrieve(imageLink, BASE_IMAGE_DIR + servantName + '/' + underscoreName + '_AF' + '.jpg')
		elif (imageCounter == 6):
			urllib.request.urlretrieve(imageLink, BASE_IMAGE_DIR + servantName + '/' + underscoreName + '_SC' + '.jpg')
		else:
			urllib.request.urlretrieve(imageLink, BASE_IMAGE_DIR + servantName + '/' + underscoreName + '_' + str(imageCounter) + '.jpg')

if __name__ == '__main__':
	main()