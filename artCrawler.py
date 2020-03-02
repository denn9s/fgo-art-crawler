import urllib.request
import urllib.error
import urllib.parse

from bs4 import BeautifulSoup

BASE_URL = 'https://grandorder.wiki/Servant_List'
CLASS_LIST = ['Saber', 'Archer', 'Lancer', 'Caster', 'Rider', 'Assassin', 'Ruler', 'Avenger', 'Moon Cancer', 'Alter-Ego', 'Foreigner', 'Berserker', 'Shielder', 'Beast']
EXTRA_CHARACTER_LIST = ['Beast', 'Solomon']
SERVANT_NAME_LIST = []
SERVANT_LINK_LIST = []

def main():
	# createServantListHTML() # comment out if HTML creation isn't needed anymore
	soup = createSoup()
	createTitleList(soup)
	createServantPageLinks()
	# createServantPageLinksHTML() # comment out if no need to update servant link .txt file

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
		SERVANT_LINK_LIST.append(servantLink)

def createServantPageLinksHTML():
	file = open('servantLinks.txt', 'w', encoding = 'utf-8')
	for servant in SERVANT_LINK_LIST:
		file.write('%s\n' % servant)

if __name__ == '__main__':
	main()