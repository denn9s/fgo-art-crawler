import urllib.request
import urllib.error
import urllib.parse

BASE_URL = 'https://grandorder.wiki/Servant_List'

def main():
	makeServantList() # comment out if HTML creation isn't needed anymore

def makeServantList():
	request = urllib.request.Request(BASE_URL, headers = {'User-Agent': 'Mozilla/5.0'})
	response = urllib.request.urlopen(request)
	content = response.read()

	file = open('servantListPage.html', 'wb')
	file.write(content)
	file.close

if __name__ == '__main__':
	main()