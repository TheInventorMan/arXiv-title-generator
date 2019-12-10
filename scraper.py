"""
Scraping tool for grabbing titles of 10,000 papers from the
computer science/systems category on arXiv. Adapted from user
manual example code at https://arxiv.org/help/api/user-manual

"""

import urllib
import feedparser
import time


# Arbitrarily grab 200 results
for i in range(200):
    # Chill out on the API calls
    time.sleep(3)

    # Base API query url
    base_url = 'http://export.arxiv.org/api/query?';

    # Search parameters
    search_query = 'cs.SY' # Get all systems-related papers
    max_results = 50
    start = max_results*i

    query = 'search_query=%s&start=%i&max_results=%i' % (search_query,
                                                         start,
                                                         max_results)
    # Open file for saving scraped data
    f = open("dataset.txt", "a+")

    # Setup parser parameters
    feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
    feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

    # Perform a GET request using the base_url and query
    response = urllib.request.urlopen(base_url+query).read()

    # Parse the response
    feed = feedparser.parse(response)

    # Print out feed information
    print ('Feed title: %s' % feed.feed.title)
    print ('Feed last updated: %s' % feed.feed.updated)

    # Print opensearch metadata
    print ('totalResults for this query: %s' % feed.feed.opensearch_totalresults)
    print ('itemsPerPage for this query: %s' % feed.feed.opensearch_itemsperpage)
    print ('startIndex for this query: %s'   % feed.feed.opensearch_startindex)
    print (i)

    # Run through each entry and save desired data
    for entry in feed.entries:

        # Preliminary data cleaning
        line = entry.title.replace('\n', '')
        line = line.replace('\t', '')
        line = line.replace('  ', ' ')
        #print ('Title:  %s' % line)

        # Some lines have non-unicode characters and causes this to derp out
        try:
            f.write(line + "\n")
        except:
            pass

# Mission accomplished
f.close()
