from lxml import html
import requests
import csv

def get_movie(title_id, writer):
    url = "http://www.imdb.com/title/"+title_id+"/"

    source = html.fromstring(requests.get(url).content)

    header = source.xpath("//div[@class='title_wrapper']")[0]
    rating = source.xpath(".//div[@class='ratingValue']/strong/span[@itemprop='ratingValue']")[0].text.strip()
    h1 = header.find("h1")
    title = h1.text.strip()
    year = h1.xpath("span[@id = 'titleYear']/a")[0].text.strip()

    subtext = header.xpath("div[@class = 'subtext']")[0]

    duration = subtext.find("time").text.strip()
    sublinks = subtext.findall("a")

    genre = []
    for i in sublinks:
        try:
            genre.append(i.attrib["href"].split("/genre/")[1].split("?")[0])
        except IndexError:
            continue


    summarydiv = source.xpath("//div[@id='main_top']/div//div[@class='plot_summary_wrapper']/div")[0]

    director_links = summarydiv.xpath("div[@class='credit_summary_item']/span[@itemprop='director']/a")

    directors = []
    for i in director_links:
        try:
            directors.append(i.attrib["href"].split("/name/")[1].split("?")[0])
        except IndexError:
            continue

    creator_links = summarydiv.xpath("div[@class='credit_summary_item']/span[@itemprop='creator']/a")
    creators = []
    for i in creator_links:
        try:
            creators.append(i.attrib["href"].split("/name/")[1].split("?")[0])
        except IndexError:
            continue
        
    actor_links = summarydiv.xpath("div[@class='credit_summary_item']/span[@itemprop='actors']/a")
    actors = []
    for i in actor_links:
        try:
            actors.append(i.attrib["href"].split("/name/")[1].split("?")[0])
        except IndexError:
            continue

    
    writer.writerow([title_id, title.encode("utf-8"), rating, year, duration, str(genre), str(directors), str(creators), str(actors)])
    
def get_person(name_id):
    url = "http://www.imdb.com/name/"+name_id+"/"

    source = html.fromstring(requests.get(url).content)

    header = source.xpath("//td[@id='overview-top']")[0]

    name = header.xpath("h1/span[@itemprop='name']")[0].text.strip()

    born = header.xpath("div[@id='name-born-info']/time")[0].attrib['datetime'].strip()
    died = ''
    try:
        died = header.xpath("div[@id='name-death-info']/time")[0].attrib['datetime'].strip()
    except IndexError:
        pass


url = "http://www.imdb.com/chart/top"
source = html.fromstring(requests.get(url).content)

filmi = [(i.text, i.attrib["href"].split("/title/")[1].split("/")[0]) for i in source.xpath("//td[@class='titleColumn']/a")]

with open('filmi.csv', 'wt') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for film in filmi:
        get_movie(film[1],writer)


        
