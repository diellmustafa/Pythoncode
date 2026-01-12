from bs4 import BeautifulSoup

#Metoda find ()
element = BeautifulSoup.find(name,attrs,recursive,string,**kwargs)

first_link = BeautifulSoup.find('a')

#metoda find_all()
element = BeautifulSoup.find_all(name,attrs,recursive,string,**kwargs)
all_links = BeautifulSoup.find_all('a')

#metoda select()
elements = BeautifulSoup.select(selector)
example = soup.select('.example')

#metoda get_text()
text = element.get_text(seperator, strip)
text = element.get_text()

#metoda attrs
Attribute = element.attrs
link = BeautifulSoup.find('a')
href = link.attrs['href']

parent = element.parent
parents = element.parents
children = element.children
descendants = element.descendants