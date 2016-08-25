import bs4
import urllib2
import json


base = "https://papers.nips.cc/book/advances-in-neural-information-processing-systems"

baseno = 13
baseye = 2000
for offset in range(16):
    no = str(baseno + offset)
    year = str(baseye + offset)
    url = "-".join([base, no, year])

    soup = bs4.BeautifulSoup(urllib2.urlopen(url), "lxml")

    lis = soup.select(".main > ul li")
    papers = []
    for li in lis:
        parsed = li.find_all("a")
        papers.append({
          "title": parsed[0].text,
          "authors": [parsed[i].text for i in range(1, len(parsed))]
        })

    print year, len(papers)
    json.dump(papers, open("nips-%s.json" % year, "w"))
