"""
Scraping tool for grabbing titles of 10,000 papers from the 
computer science/systems category on arXiv. Adapted from user
manual example code at https://arxiv.org/help/api/user-manual

"""

import urllib
import feedparser
import time



for i in range(200):
    time.sleep(3)
    
    # Base api query url
    base_url = 'http://export.arxiv.org/api/query?';

    # Search parameters
    search_query = 'cs.SY' # get all systems-related papers
    max_results = 50
    start = max_results*i                     

    query = 'search_query=%s&start=%i&max_results=%i' % (search_query,
                                                         start,
                                                         max_results)
    f = open("dataset.txt", "a+")

    feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
    feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'
    
    # perform a GET request using the base_url and query
    response = urllib.request.urlopen(base_url+query).read()

    # parse the response using feedparser
    feed = feedparser.parse(response)

    # print out feed information
    print ('Feed title: %s' % feed.feed.title)
    print ('Feed last updated: %s' % feed.feed.updated)

    # print opensearch metadata
    print ('totalResults for this query: %s' % feed.feed.opensearch_totalresults)
    print ('itemsPerPage for this query: %s' % feed.feed.opensearch_itemsperpage)
    print ('startIndex for this query: %s'   % feed.feed.opensearch_startindex)
    print (i)
    
    # Run through each entry, and print out information
    for entry in feed.entries:

        line = entry.title.replace('\n', '')
        line = line.replace('\t', '')
        line = line.replace('  ', ' ')
        #print ('Title:  %s' % line)

        try:
            f.write(line + "\n")
        except:
            pass
        
        
f.close()