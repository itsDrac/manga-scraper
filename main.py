from bs4 import BeautifulSoup as bs
import requests, os


class Mangakakalot:
	def __init__(self, url):
		self.title=''
		self.chapter = 0
		self.page = 0
		self.url = url
		self.heading()
		self.download()

	def heading(self):
		source = requests.get(self.url).text
		soup = bs(source, 'lxml')
		self.title = soup.find('ul', class_='manga-info-text').find('h1').text

	def download(self):
		source = requests.get(self.url).text
		soup = bs(source, 'lxml')

		chapter_list = soup.find('div', class_='chapter-list')
		chapters = [ch.find('a')['href'] for ch in chapter_list.find_all('div', class_='row')][::-1]

		for i, chapter in enumerate(chapters):
			self.chapter = i+1
			os.makedirs(f'{self.title}/{self.chapter}')
			self.download_chapter(chapter)

	def download_chapter(self, url):
		source = requests.get(url).text
		soup = bs(source, 'lxml')
		page_list = soup.find('div', class_='vung-doc')
		pages = [ch['src'] for ch in page_list.find_all('img')]
		for i, page in enumerate(pages):
			self.page = i+1
			self.download_page(page)
	
	def download_page(self, url):
		temp = list(url)
		temp[9]=temp[19]='8'
		url=''.join(temp)
		img = requests.get(url)
		print(f'{self.title} | {self.chapter} | {self.page} | {img.ok}')
		print()
		with open(f'{self.title}/{self.chapter}/{self.page}.jpg', 'wb') as f :
			f.write(img.content)
		


class Manganelo:
	def __init__(self, url):
		self.title = ''
		self.chapter = 0
		self.page = 0
		self.url = url
		self.heading()
		self.download()

	def heading(self):
		source = requests.get(self.url).text
		soup = bs(source, 'lxml')
		self.title = soup.select_one('.story-info-right>h1').text

	def download(self):
		source = requests.get(self.url).text
		soup = bs(source, 'lxml')
		chapter_list = soup.select('li>.chapter-name')
		chapters = [c['href'] for c in chapter_list[::-1]]
		for i, chapter in enumerate(chapters):
			self.chapter = i+1
			os.makedirs(f'{self.title}/{self.chapter}')
			self.download_chapter(chapter)

	def download_chapter(self, url):
		source = requests.get(url).text
		soup = bs(source, 'lxml')
		page_list = soup.select('.container-chapter-reader>img')
		pages = [p['src'] for p in page_list]
		for i, page in enumerate(pages):
			self.page = i+1
			self.download_page(page)

	def download_page(self, url):
		temp = list(url)
		temp[9]=temp[19]='8'
		url=''.join(temp)
		img = requests.get(url)
		print(f'{self.title} | {self.chapter} | {self.page} | {img.ok}')
		print()
		with open(f'{self.title}/{self.chapter}/{self.page}.jpg', 'wb') as f :
			f.write(img.content)
		

url = input('Enter Url of manga : ')

if 'mangakakalot.com' in url:
	manga = Mangakakalot(url)

elif 'manganelo.com' in url:
	manga = Manganelo(url)



'''
Test Case 1 :
	https://mangakakalot.com/manga/dv922179  
	https://mangakakalot.com/manga/tt923341

Test Case 2 :
	https://mangakakalot.com/read-ek1hu158504836793

Test Case 3 :
	https://manganelo.com/manga/fk918347
	https://manganelo.com/manga/zt922734
'''
