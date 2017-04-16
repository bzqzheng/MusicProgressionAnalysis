import bs4
import requests

lyrics_site = requests.get('https://tabs.ultimate-guitar.com/t/the_weeknd/i_feel_it_coming_ver2_crd.htm')
lyrics_soup = bs4.BeautifulSoup(lyrics_site.content, 'html.parser')
cont = lyrics_soup.find_all('pre', {'class':'js-tab-content'})
for k in cont:
	print(k)
