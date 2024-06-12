import twitter  #https://python-twitter.readthedocs.io/en/latest/
import time, csv

# API setting
# Change None to your own credential information
#api = twitter.Api(consumer_key= None,
#                  consumer_secret= None,
#                  access_token_key= None,
#                  access_token_secret= None,
#                  tweet_mode='extended',
#                  sleep_on_rate_limit=True) ## This parameter setting automatically controls rate limit.
api = twitter.Api(consumer_key="UnyzxmPqvlxluLDFIWrrA",
                  consumer_secret="5dPzRECPdmQpQObC3YU5DI01WGwUilHreln6lObW6Vk",
                  access_token_key="47493090-SxKTyQ1dygCVRSpja99AAfUG0PAOpG6cUHQTlSe8M",
                  access_token_secret="AIyLsCxCHPuF4xBbUwBym2lHivN3Nm2VvUMi49D1aVmNS",
                  tweet_mode='extended',
                  sleep_on_rate_limit=True) ## This parameter setting automatically controls rate limit.

def get_tweets (status, api, csvwriter):
    # a list to save tweet attributes
    temp = []
    tweet_id = status.id
    user_id = status.user.id
    # sleep for controling rate limit
    time.sleep(0.1)
    if (status.lang == "en"): ## collect tweets only in english
        user_info = api.GetUser(user_id)
        account_description = user_info.description.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
        account_favourites_count = user_info.favourites_count
        account_followers_count = user_info.followers_count
        account_friends_count = user_info.friends_count
        account_name = user_info.name.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
        account_profile_image_url = user_info.profile_image_url
        account_screen_name = user_info.screen_name.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
        # tweets is trucated according to the new policy
        # https://github.com/bear/python-twitter/issues/420
        # https://stackoverflow.com/questions/38717816/twitter-api-text-field-value-is-truncated
        # We should use full_text instead of text
        # For retweets we need one more steps too.
        if status.retweeted_status == None :
            tweet_text = status.full_text.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
        else:
            temp_text = status.full_text
            new_text = status.retweeted_status.full_text
            ## find the overraped part and replace with the full text
            ## There are cases where the tweets are very short.
            if len(new_text) >= 3:
                length_compare = round(len(new_text) / 3)
                temp_text = temp_text.split(new_text[:length_compare])
                final_text = temp_text[0] + new_text
                tweet_text = final_text.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
            else:
                tweet_text = status.full_text.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
        temp.append(user_id)
        temp.append(account_description)
        temp.append(account_favourites_count)
        temp.append(account_followers_count)
        temp.append(account_friends_count)
        temp.append(account_name)
        temp.append(account_profile_image_url)
        temp.append(account_screen_name)
        temp.append(tweet_id)
        temp.append(tweet_text)
        ## There are three types of geostatus: geo, coordinates, and place.
        if status.place != None:
            if status.place["full_name"] != None:
                temp.append(status.place["full_name"])
            else:
                temp.append("N/A")
        else:
            temp.append("N/A")
        csvwriter.writerow(temp)
    return csvwriter

## ask search term to user
search_term = input("What do you want to search with Twitter API?: ")

filename = search_term + "_tweets.csv"

with open(filename, 'a', encoding="utf-8", newline="") as out_file:
    ## create a list that will save tweet instances
    ## following are field names
    temp = []
    temp.append("account_id")
    temp.append("account_description")
    temp.append("account_favourites_count")
    temp.append("account_followers_count")
    temp.append("account_friends_count")
    temp.append("account_name")
    temp.append("account_profile_image_url")
    temp.append("account_screen_name")
    temp.append("tweet_id")
    temp.append("tweet_text")
    temp.append("place")
    CSVWriter = csv.writer(out_file)
    CSVWriter.writerow(temp)
    ## Return twitter search results for a given term. You must specify one of term, geocode, or raw_query.
    tweets = api.GetSearch(search_term, count=100, lang="en", include_entities=True )
    ## loop over the returned statuses to extract attributes needed
    for tweet in tweets:
        CSVWriter = get_tweets(tweet, api, CSVWriter)

print("All process is done, and the file name as "+ filename + " is created.")
