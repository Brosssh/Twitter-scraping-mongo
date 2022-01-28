from time import sleep
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
import cleaning

def create_webdriver_instance():
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--lang=en")
    options.add_argument("--headless")
    driver = Edge(options=options)
    return driver

def twitter_search(driver, url, id):
    tweet = {}
    tweet["tweet_id"]=id
    try:
        driver.get(url)
    except:
        print("Error on url, message may be deleted")
        return
    sleep(3)
    try:
        authors = driver.find_element(By.XPATH,'/html//body/div[@id="react-root"]/div[@class="css-1dbjc4n r-13awgt0 r-12vffkv"]'
                                                '/div[@class="css-1dbjc4n r-13awgt0 r-12vffkv"]/div[@class="css-1dbjc4n r-18u37iz r-13qz1uu r-417010"]'
                                                '/main/div/div/div/div/div/div[@class="css-1dbjc4n"]/section/div/div/div/div/div/article/div'
                                                '/div/div/div[@class="css-1dbjc4n r-18u37iz r-15zivkp"]')
        tweet["author_alias"]=authors.text.split("\n")[0]
        tweet["author_name"] = authors.text.split("\n")[1]
    except:
        print("Skipping authors")

    try:
        time_source_line = driver.find_element(By.XPATH,
                                  '/html//body/div[@id="react-root"]/div[@class="css-1dbjc4n r-13awgt0 r-12vffkv"]'
                                  '/div[@class="css-1dbjc4n r-13awgt0 r-12vffkv"]/div[@class="css-1dbjc4n r-18u37iz r-13qz1uu r-417010"]'
                                  '/main/div/div/div/div/div/div[@class="css-1dbjc4n"]/section/div/div/div/div/div/article/div'
                                  '/div/div/div[@class="css-1dbjc4n"]/div[@class="css-1dbjc4n r-1r5su4o"]')
        tweet = {**tweet, **cleaning.clean_date_source(time_source_line.text)}
    except:
        print("Skipping time_source")
    #likerow = driver.find_element(By.XPATH,
    #                                       '/html//body/div[@id="react-root"]/div[@class="css-1dbjc4n r-13awgt0 r-12vffkv"]'
    #                                  '/div[@class="css-1dbjc4n r-13awgt0 r-12vffkv"]/div[@class="css-1dbjc4n r-18u37iz r-13qz1uu r-417010"]'
    #                                       '/main/div/div/div/div/div/div[@class="css-1dbjc4n"]/section/div/div/div/div/div/article/div'
    #                                       '/div/div/div[@class="css-1dbjc4n"]/div[@class="css-1dbjc4n"]'
    #                                       '/div[@class="css-1dbjc4n r-1dgieki r-1efd50x r-5kkj8d r-13awgt0 r-18u37iz r-tzz3ar r-s1qlax r-1yzf0co"]')
    try:
        text_message = driver.find_element(By.XPATH,
                                           '/html//body/div[@id="react-root"]/div[@class="css-1dbjc4n r-13awgt0 r-12vffkv"]'
                                           '/div[@class="css-1dbjc4n r-13awgt0 r-12vffkv"]/div[@class="css-1dbjc4n r-18u37iz r-13qz1uu r-417010"]'
                                           '/main/div/div/div/div/div/div[@class="css-1dbjc4n"]/section/div/div/div/div/div/article/div'
                                           '/div/div/div[@class="css-1dbjc4n"]/div[@class="css-1dbjc4n"]/div[@class="css-1dbjc4n r-1s2bzr4"]')
        tweet = {**tweet, **cleaning.clean_text(text_message.text)}
    except:
        print("Skipping text_message")

    try:
        reply_to = driver.find_element(By.XPATH,
                                           '/html//body/div[@id="react-root"]/div[@class="css-1dbjc4n r-13awgt0 r-12vffkv"]'
                                           '/div[@class="css-1dbjc4n r-13awgt0 r-12vffkv"]/div[@class="css-1dbjc4n r-18u37iz r-13qz1uu r-417010"]'
                                           '/main/div/div/div/div/div/div[@class="css-1dbjc4n"]/section/div/div/div/div/div/article/div'
                                           '/div/div/div[@class="css-1dbjc4n"]/div[@class="css-1dbjc4n"]/div[@class="css-1dbjc4n"]')
        attachment = cleaning.clean_attachment(reply_to.text)
        if attachment != None:
            tweet["attachment"] = attachment

    except:
        print("Skipping attachmente")

    return tweet


def user_search(driver, url):
    user={}
    try:
        driver.get(url)
    except:
        print("Error on url, message may be deleted")
        return
    sleep(3)
    try:
        following_followers = driver.find_element(By.XPATH,
                                  '/html//body/div[@id="react-root"]/div[@class="css-1dbjc4n r-13awgt0 r-12vffkv"]'
                                  '/div[@class="css-1dbjc4n r-13awgt0 r-12vffkv"]/'
                                  'div[@class="css-1dbjc4n r-18u37iz r-13qz1uu r-417010"]/main/div/div/div/div/div/div[@class="css-1dbjc4n"]'
                                  '/div/div/div/div/div[@class="css-1dbjc4n r-13awgt0 r-18u37iz r-1w6e6rj"]')
        user["following"] = str(following_followers.text).split("\n")[0].split(" ")[0]
        user["followers"] = str(following_followers.text).split("\n")[1].split(" ")[0]
    except:
        print("Skipping following line")



    try:
        description = driver.find_element(By.XPATH,
                                              '/html//body/div[@id="react-root"]/div[@class="css-1dbjc4n r-13awgt0 r-12vffkv"]'
                                              '/div[@class="css-1dbjc4n r-13awgt0 r-12vffkv"]/'
                                              'div[@class="css-1dbjc4n r-18u37iz r-13qz1uu r-417010"]/main/div/div/div/div/div/div[@class="css-1dbjc4n"]'
                                              '/div/div/div/div/div[@class="css-1dbjc4n r-1adg3ll r-6gpygo"]/div[@class="css-1dbjc4n"]/div[@class="css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0"]')
        user["description"] = str(description.text)
    except:
        print("Skipping user description")

    return user


def get_json_author(name):  # 'https://twitter.com/AsherCarneiro/status/1484502627752763393'
    print("\nStarting scraping of the author", name)
    driver = create_webdriver_instance()
    user=user_search(driver,'https://twitter.com/'+name)
    driver.quit()
    return user

def get_json_twitter(id): #'https://twitter.com/AsherCarneiro/status/1484502627752763393'
    print("\nStarting scraping from ID", id)
    driver = create_webdriver_instance()
    tweet= twitter_search(driver, "https://twitter.com/me/status/"+id, id)
    #tweet= twitter_search(driver, "https://twitter.com/me/status/1484547246926741507",1484547246926741507)
    driver.quit()
    return tweet

