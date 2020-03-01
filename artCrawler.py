import urllib.request
import urllib.error
import urllib.parse

from bs4 import BeautifulSoup

BASE_URL = 'https://grandorder.wiki/Servant_List'
CLASS_LIST = ['Saber', 'Archer', 'Lancer', 'Caster', 'Rider', 'Assassin', 'Ruler', 'Avenger', 'Moon Cancer', 'Alter-Ego', 'Foreigner', 'Berserker', 'Shielder']
SERVANT_NAME_LIST = []

def main():
	# makeServantListHTML() # comment out if HTML creation isn't needed anymore
	makeSoup()

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
	for link in soup.find_all('a'):
		title = link.get('title')
		if (titleCheck(title) == True):
			SERVANT_NAME_LIST.append(title)

def titleCheck(title):
	return True

if __name__ == '__main__':
	main()