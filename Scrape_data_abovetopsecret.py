#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests 
import re
from bs4 import BeautifulSoup
import datetime
import pandas as pd
from time import sleep
from random import randint
from IPython.core.display import clear_output
import pymysql


# In[2]:


# the list store all the result links
links =[]


# In[ ]:


url ="https://www.google.com/search?biw=1602&bih=1142&sxsrf=ACYBGNT5nlhO3WG-vfLuFPKn_uUr_HR7GA%3A1568325612918&ei=7L96XY3LN-6Ogge6vabgDg&q=vaccine+site%3Aabovetopsecret.com"


# In[3]:


# define the function to scrape the links from google research result
def scraped_links(url):
    page_fc=requests.get(url)
    soup_fc = BeautifulSoup(page.content)
    # add the sleep function to avoid ip blocked by google
    sleep(randint(8,15))
    clear_output(wait = True)
    for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*pg1)")):
        href=re.split(":(?=http)",link["href"].replace("/url?q=",""))
        href_str = ''.join(href)
        href_1=href_str.split('&')[0]
        if href_1 not in links:
            links.append(href_1)


# In[4]:


# get the next page's link of the result from google research until getting all of the next pages
def get_next_page_link(url):
    page=requests.get(url)
    soup = BeautifulSoup(page.content)
    next_page = soup.find_all('a',{'aria-label':"Next page"})
    for link in next_page:
        next_href = link.get('href')
        next_link = 'http://www.google.com' + next_href
        search_links.append(next_link)
        return get_next_page_link(next_link)


# In[5]:


# scrape all the links's pages
def get_all_post(links):
    for link in links:
        page=requests.get(link)
        soup = BeautifulSoup(page.content)
        for pg in soup.find_all('a',{'class':'multitxt'}):
            num=[]
            pg_num =re.split('g',pg['href'])
            num.append(pg_num[1])
        for i in range(1,int(num[0])+1):
            link_page=link.split('g')[0]+'g'+str(i)
            scrape_post(link_page)


# In[ ]:


posts_list=[]
thread_num_list =[]
poster_name_list=[]
post_time_list=[]
raw_post=[]
src_id=[]
profile_url=[]
likes = []


# In[ ]:


# scrape the all content in the pages
def scrape_post(link_page):
    page_post=requests.get(link_page)
    soup_post = BeautifulSoup(page_post.content)
    # get the source id of each post
    for text in soup_post.find_all('div',{'class':'threadpostC post'}):
        post_id = text.get('id').split('t')[1]
        src_id.append(post_id)
    # get the text content of each post
    for text in soup_post.find_all('div',{'class':'KonaBody'}):
        raw_post.append(text)
        post=text.get_text()
        posts_list.append(post)
        # get the thread_number of each post
        thread_num = link_page.split('thread')[1].split('/')[0]
        thread_num_list.append(thread_num)
    # get the poster name 
    for poster in soup_post.find_all('a',{'class':'membr'}):
        poster_name = poster.get_text()
        poster_name_list.append(poster_name)
    # get the post time and the likes
    for time in soup_post.find_all('div',{'class':'posttopL'}):
        post_time = time.get_text()
        post_time_list.append(post_time)
        # get the stars and count likes
        count = 0
        for i in time.find_all('i'):
            if i:
                count +=1
        if time.find_all('b'):
            for b in time.find_all('b'):
                more = b.get_text()
                num_str= more.split('+')[1].split(' ')[0]
                num_more = int(num_str)
                num_likes = num_more + count
                likes.append(num_likes)
        else:
            num_likes = count
            likes.append(num_likes)


# In[ ]:


# scrape all the profile url of each user in the websites
def scrape_post_profileurl(link_page):
    page_post=requests.get(link_page)
    soup_post = BeautifulSoup(page_post.content)
    for poster in soup_post.find_all('a',{'class':'membr'}):
        half_url = poster.get('href').split('.')[2]
        url_whole = 'http://www.abovetopsecret.com/forum/' + half_url
        profile_2.append(url_whole) 


# In[ ]:


post_createdtime=[]


# In[ ]:


# scrape the first time
def scrape_created_time(links):
    for link in links:
        page_post=requests.get(link)
        soup_post = BeautifulSoup(page_post.content)
        for time in soup_post.find_all('div',{'class':'posttopL'}):
            post_time = time.get_text()
            time_raw = post_time.split('on')[1].split()
            time_str = time_raw[0]+' '+time_raw[1]+' '+time_raw[2]+' '+time_raw[4] +' '+time_raw[5]
            start_date = datetime.datetime.strptime(time_str, "%b, %d %Y %I:%M %p")
            final_time = start_date.strftime("%Y-%m-%d %H:%M:%S")
            post_createdtime.append(final_time)
            break


# In[ ]:


scrape_created_time(links)


# In[ ]:


# scrape all the titles for each thread
def scrape_post_title(links):
    for link in links:
        page=requests.get(link)
        soup = BeautifulSoup(page.content)
        for i in soup.find_all('h1'):
            title1 = i.get_text()
            title.append(title1)
    


# In[ ]:


# get the profile url
for name in poster_name_list:
    profile = 'http://www.abovetopsecret.com/forum/mem/' + name
    profile_url.append(profile)


# In[ ]:


create_time=[]
# transform the type of time
for time in post_time_list:
    time_raw = time.split('on')[1].split()
    time_str = time_raw[0]+' '+time_raw[1]+' '+time_raw[2]+' '+time_raw[4] +' '+time_raw[5]
    start_date = datetime.datetime.strptime(time_str, "%b, %d %Y %I:%M %p")
    final_time = start_date.strftime("%Y-%m-%d %H:%M:%S")
    create_time.append(final_time)


# In[ ]:


scrape_post_title(links)


# In[ ]:


dict_content ={}
dict_content ={'site_id':src_id,'creator':FK_PosterID,'thread':FK_threadid,'raw':raw_post,'clean':posts_list,
               'likes':likes,'creation_date':create_time
              }


# In[ ]:


# transform to dataframe
scraped_content = pd.DataFrame(dict_content)


# In[ ]:


dict_threads = {}
dict_threads={'links':links,'time':time_now,'domain':domain_threads,'title':title,'creationtime':post_createdtime}


# In[ ]:


# transform to dataframe
scraped_threads = pd.DataFrame(dict_threads)


# In[ ]:


# get the data of posters and transform to a dataframe
dict_posters ={}
dict_posters={'name':unqi_name,'url':unqi_profile_url,'domain':domain_posters}


# In[ ]:


scraped_posters = pd.DataFrame(dict_posters)


# In[ ]:


# connect the database
#SQL connection data to connect 
HOST = "localhost"
USERNAME = "mingkang"
PASSWORD = "zmk520"
DATABASE = "vaccinedatabase"
db = pymysql.connect(HOST, USERNAME, PASSWORD, DATABASE)
cursor = db.cursor()


# In[ ]:


# insert data to content table
for i,row in scraped_content.iterrows():
    insert_query = """INSERT INTO content (site_id,creator,thread,raw,clean,likes,creation_date) 
                                VALUES (%s,%s,%s,%s,%s,%s,%s) """
    record2 = (row['site_id'],row['creator'],row['thread'],str(row['raw']),row['clean'],row['likes'],row['creation_date'])
    cursor.execute(insert_query,record2)
    #db.commit()


# In[ ]:


# insert data to quotes
quotes_src_id =[]
quotes_targ_id = []
quotes_targers_id =[]
quotes_clean = []
quotes_raw = []


# In[ ]:


# get the key from content table
for tupl in content_select:
    if 'quotebox' in tupl[3]:
        quotes_src_id.append(tupl[0])
        quotes_raw.append(tupl[3])
        quotes_clean.append(tupl[4])


# In[ ]:


pattern = re.compile('\d+')


# In[ ]:


# insert data to quotes table
for i in range(len(quotes_src_id)):
    count = 0
    if re.search(pattern,quotes_raw[i]):
        x=re.search(pattern,quotes_raw[i]).group()
        for tupl in content_select:
            if x == tupl[1]:
                tupl1 = (quotes_src_id[i],tupl[0],tupl[2],quotes_raw[i],quotes_clean[i])
                insert_query2 = "insert into quotes (src_id,targ_id,targ_user,clean,raw) values (%s,%s,%s,%s,%s)"
                cursor.execute(insert_query2,tupl1)
                #db.commit()
                count += 1
                break
        if count == 0:
            tupl2 = (quotes_src_id[i],quotes_raw[i],quotes_clean[i])
            insert_query3 = "insert into quotes (src_id,clean,raw) values (%s,%s,%s)"
            cursor.execute(insert_query3,tupl2)
            #db.commit()
            
    else:
        tupl3 = (quotes_src_id[i],quotes_raw[i],quotes_clean[i])
        insert_query4 = "insert into quotes (src_id,clean,raw) values (%s,%s,%s)"
        cursor.execute(insert_query4,tupl3)
        #db.commit()


# In[ ]:


relations_src_id = []
relations_targ_id =[]
relations_src_user=[]
relations_targ_user=[]
relations_raw=[]


# In[ ]:


# get the key from content table
for tupl in content_select:
    if 'a reply to' in tupl[3]:
        relations_src_id.append(tupl[0])
        relations_src_user.append(tupl[2])
        relations_raw.append(tupl[3])


# In[ ]:


# get the relpy post from selations_raw
for ele in relations_raw:
    count+=1
    num_raw = ele.split('reply')[1]
    real_raw.append(num_raw)


# In[ ]:


# insert data to the relations table
for i in range(len(relations_src_id)):
    count = 0
    if re.search(pattern,real_raw[i]):
        x=re.search(pattern,real_raw[i]).group()
        for tupl in content_select:
            if x == tupl[1]:
                tupl1 = (relations_src_id[i],tupl[0],relations_src_user[i],tupl[2],'direct reply')
                insert_query2 = "insert into relations (src_id,targ_id,src_user,targ_user,type) values (%s,%s,%s,%s,%s)"
                cursor.execute(insert_query2,tupl1)
                #db.commit()
                count += 1
                break
        if count == 0:
            tupl2 = (relations_src_id[i],relations_src_user[i],'direct reply')
            insert_query3 = "insert into relations (src_id,src_user,type) values (%s,%s,%s)"
            cursor.execute(insert_query3,tupl2)
            #db.commit()
    else:
        tupl2 = (relations_src_id[i],relations_src_user[i],'direct reply')
        relations_tuple.append(tupl2)
        insert_query3 = "insert into relations (src_id,src_user,type) values (%s,%s,%s)"
        cursor.execute(insert_query3,tupl2)
        #db.commit()


# In[ ]:


# get the unique name in poster_name_list
for name in poster_name_list:
    if name not in unqi_name:
        unqi_name.append(name)


# In[ ]:


id_of_threads=cursor.fetchall()


# In[ ]:


# get the foreign key of thread id 
for num in thread_num_list:
    for tupl in id_of_threads:
        if str(num) in str(tupl[1]):
            FK_threadid.append(tupl[0])
            break


# In[ ]:


id_of_posters = cursor.fetchall()


# In[ ]:


# get the foreign key of poster id
for name in poster_name_list:
    for tupl in  id_of_posters:
        if name == tupl[1]:
            FK_PosterID.append(tupl[0])


# In[6]:


# get the now time
now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
time_now = []
for i in links:
    # get the repeated domain
    domain_threads.append(a)
    # get the repeated now time
    time_now.append(now_time)


# In[ ]:




