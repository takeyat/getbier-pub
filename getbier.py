import config
import os
import json
import urllib
import time
import re
import lxml.html
import cssselect
from TwitterAPI import TwitterAPI

# Twitter用クレデンシャルを設定
CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET

SEARCH_TERM = config.TARGET_ACCOUNT
api = TwitterAPI(CK, CS, AT, ATS)
mkdir_name = "bier_illustration"
reg_url = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"

# 集めた画像を格納するディレクトリの作成を行う
def dir_check():
    if not os.path.isdir(mkdir_name):
        os.mkdir(mkdir_name)
    check_count = 0
    while True:
        if not os.path.isdir(mkdir_name + "/dir" + str(check_count)):
            os.mkdir(mkdir_name + "/dir" + str(check_count))
            dir_name = "/dir" + str(check_count)
            return dir_name
        check_count += 1

# Tweetを取得
def get_target_word(keyword):
    req = api.request('tweets/search/fullarchive/:bier', {'query': SEARCH_TERM + keyword, 'fromDate': '200603210000'})
    # req = api.request('tweets/search/30day/:bier', {'query': SEARCH_TERM + keyword, 'fromDate': '201908010000'})
    timeline = json.loads(req.text)
    # print(timeline)
    return timeline

# 取得したツイートに画像があれば、その画像を取得する
def get_illustration(timeline, dir_name):
    global image
    check_image = []
    for tweet in timeline['results']:
        try:
            time_stirng = time.strftime('%Y-%m-%d', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
            # tweetから直接画像を取得
            extended_entities = tweet.get('extended_entities')
            if extended_entities == None:
                tweet_text = tweet['text']
                insta_url = re.search(reg_url, tweet_text)
                # instagramから画像を取得するコードは省略
            else:
                media_list = tweet['extended_entities']['media']
                for media in media_list:
                    image = media['media_url']
                    path_str = mkdir_name + dir_name + "/"+ time_stirng + "_" + os.path.basename(image)
            if image in check_image:
                continue
            with open(path_str, 'wb') as f:
                img = urllib.request.urlopen(image).read()
                f.write(img)
                check_image.append(image)
        except:
            import traceback
            traceback.print_exc()
if __name__ == '__main__':
    dir_name = dir_check()
    all_list = []
    # 検索対象の単語を設定
    keyword = config.TARGET_KEYWORD
    timeline = get_target_word(keyword)
    get_illustration(timeline, dir_name)
