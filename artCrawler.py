import urllib.request
import urllib.error
import urllib.parse

from bs4 import BeautifulSoup

BASE_URL = 'https://grandorder.wiki/Servant_List'
CLASS_LIST = ['Saber', 'Archer', 'Lancer', 'Caster', 'Rider', 'Assassin', 'Ruler', 'Avenger', 'Moon Cancer', 'Alter-Ego', 'Foreigner', 'Berserker', 'Shielder', 'Beast']
SERVANT_NAME_LIST = []

def main():
	# makeServantListHTML() # comment out if HTML creation isn't needed anymore
	soup = makeSoup()
	makeTitleList(soup)

def makeServantListHTML():
	request = urllib.request.Request(BASE_URL, headers = {'User-Agent': 'Mozilla/5.0'})
	response = urllib.request.urlopen(request)
	content = response.read()

	file = open('servantListPage.html', 'wb')
	file.write(content)
	file.close

def makeSoup():
	servantListHTML = open('servantListPage.html', encoding = 'utf-8')
	soup = BeautifulSoup(servantListHTML, features = 'html.parser')
	return soup

def makeTitleList(soup):
	titleList = []
	for link in soup.find_all('a'):
		title = link.get('title')
		if (titleCheck(title) == True):
			titleList.append(title)
	for index in (range(len(titleList) - 1)):
		if (titleList[index] == titleList[index + 1]):
			SERVANT_NAME_LIST.append(titleList[index])
	SERVANT_NAME_LIST.sort(key = str.lower)
	for item in SERVANT_NAME_LIST:
		print(item)

def titleCheck(title):
	if (title is None):
		return False
	if (title in CLASS_LIST):
		return False
	if ('Servants' in title):
		return False
	if ('Friend Points' in title):
		return False
	return True

if __name__ == '__main__':
	main()