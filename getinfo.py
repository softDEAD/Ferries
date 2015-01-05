from bs4 import BeautifulSoup
from google import search
import urllib2, re, operator


def pulladdress(d):
        r= re.findall( "[A-Z][a-z]+ Street [A-Z][a-z]+, [A-Z][a-z]+ [0-9]{5}", d)#old code from name finder
        return r;
#Going to be used to find obscure tourist locations.
def getResults(noun):
        links = search(noun, lang='en', stop=10)
        results = []
        for url in links:
                req = urllib2.Request(url)
                try:
                        webpage = urllib2.urlopen(req)
                        webpagetext = webpage.read()
                        webpage.close()
                        soup = BeautifulSoup(webpagetext)
                        results.append(pulladdress(soup))
                except urllib2.HTTPError, e:
                        pass
        return result
