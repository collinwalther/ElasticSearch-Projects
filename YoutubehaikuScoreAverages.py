# A python script that iterates throughout every post on /r/youtubehaiku, using the reddit
# submissions collection, searched through ElasticSearch.

import urllib.request
import json
import re

# The following variables will be used to calculate averages at the end
# of the entire program.
poetryScoreSum = 0              # counts the sum of scores belonging to [poetry] posts
haikuScoreSum = 0               # counts the sum of socres belonging to [haiku] posts
poetryScoreSumNoOutliers = 0    # counts the sum of scores belonging to [poetry] posts with score >= 20
haikuScoreSumNoOutliers = 0     # counts the sum of scores belonging to [haiku] posts with score >= 20
poetryCount = 0                 # counts the number of [poetry] posts
poetryCountNoOutliers = 0       # counts the number of [poetry] post with score >= 20
haikuCount = 0                  # counts the number of [haiku] posts
haikuCountNoOutliers = 0        # counts the number of [haiku] posts with score >= 20

# The following variable keeps track of which timestamp the program needs to
# search below, in order to iteritavely get all posts from youtubehaiku.
# Max UTC timestamp of all reddit posts at the time of this program being
# written was 1484647281, so any number bigger than that will make a good
# initial value for the variable.
currTimestamp = 2000000000

while 1:
    # The following request must have a normal user agent; the specific
    # domain that it queries rejects bots and apparently python says
    # it's a bot in url requests, so I have to look legit.
    pageRequest = urllib.request.Request('https://elastic.pushshift.io/reddit/submission/_search/?sort=created_utc:desc&size=1000&q=subreddit:youtubehaiku%20AND%20created_utc:<' + str(currTimestamp), headers={'User-Agent': 'Mozilla'})

    # The following line uses stackoverflow black magic, the likes of which
    # the world has never seen and should never see again.
    # Bascially, what it does is requests the page with
    # urllib.request.urlopen(pageRequest), reads the data in there using
    # the .read() method, and then interprets that data, which is apparently
    # encoded as a bytestream, with .decode('utf-8').  Without all of those
    # steps, the data will not be able to be interpreted by json.loads later.
    source = urllib.request.urlopen(pageRequest).read().decode('utf-8')

    # The following line stores the json data as a list with many, many levels
    # of sublists.  jsonData['hits']['hits'] returns the list with each element
    # corresponding to a reddit post, for some horrible reason.
    jsonData = json.loads(source)

    # Use regexes to find titles tagged appropriately with [Poetry]
    for i in range (0, len(jsonData['hits']['hits'])):
        if re.search('\[Poetry\]', jsonData['hits']['hits'][i]['_source']['title'], re.I):
            poetryCount += 1
            poetryScoreSum += jsonData['hits']['hits'][i]['_source']['score']
            if jsonData['hits']['hits'][i]['_source']['score'] >= 20:
                poetryCountNoOutliers += 1
                poetryScoreSumNoOutliers += jsonData['hits']['hits'][i]['_source']['score']
        elif re.search('\[Haiku\]', jsonData['hits']['hits'][i]['_source']['title'], re.I):
            haikuCount += 1
            haikuScoreSum += jsonData['hits']['hits'][i]['_source']['score']
            if jsonData['hits']['hits'][i]['_source']['score'] >= 20:
                haikuCountNoOutliers += 1
                haikuScoreSumNoOutliers += jsonData['hits']['hits'][i]['_source']['score']

    # The following condition will trigger when we've reached the end of
    # ALL of the data.
    if len(jsonData['hits']['hits']) < 1000:
        break

    # If we haven't reached the end of our data, set the limit on the timestamp
    # for the data we will get next to be equal to the lowest timestamp from
    # the current data set.
    currTimestamp = jsonData['hits']['hits'][999]['_source']['created_utc']

    # This next line lets me know that the program is actually making progress
    # and isn't just hanging.
    print("Results left = " + str(jsonData['hits']['total'] - 1000))

# Now that we're done with the data, calculate and display the averages.
poetryScoreAvg = poetryScoreSum / poetryCount
haikuScoreAvg = haikuScoreSum / haikuCount
poetryScoreAvgNoOutliers = poetryScoreSumNoOutliers / poetryCountNoOutliers
haikuScoreAvgNoOutliers = haikuScoreSumNoOutliers / haikuCountNoOutliers
print("poetry average = " + str(poetryScoreAvg))
print("haiku average = " + str(haikuScoreAvg))
print("poetry average (no outliers) = " + str(poetryScoreAvgNoOutliers))
print("haiku average (no outliers) = " + str(haikuScoreAvgNoOutliers))
