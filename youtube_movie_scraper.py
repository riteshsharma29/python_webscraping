import json
from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
import streamlit as st
import pandas as pd
import os

df = pd.read_excel(os.path.join('data', 'url.xlsx'),sheet_name='url')
df.dropna(inplace=True)
url = df['URL'].to_list()
urllist=tuple(url)

st.sidebar.title("YouTube Movie Scraper")
st.sidebar.markdown("A generic scraper developed in Python to extract content from YouTube Movie links.")
URL = st.sidebar.selectbox("Select YouTube URL:",urllist)

# init an HTML Session
session = HTMLSession()
# get the html content
response = session.get(URL)
soup = bs(response.content, "html.parser")
data = soup.find_all("script")

# extract title
title = soup.find("title").text
title = title.replace(" - YouTube", "")

def Description():
    # extract Description
    for i in range(0, len(data)):
        if "shortDescription" in str(data[i]):
            d = str(data[i])
            dd = d.split(" = ")[1]
            j = json.loads(dd.replace(";</script>", ""))
            return j["videoDetails"]["shortDescription"]
            break

def Other_Details(label_text,detail_type):
    # other movie details
    d_2 = ""
    for j in range(0, len(data)):
        if "metadataRowContainerRenderer" in str(data[j]):
            d_2 += str(data[j])
            break
    dd_2 = d_2.split(" = ")[1]
    jj = json.loads(dd_2.replace(";</script>", ""))
    row_data = \
    jj["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][1]["videoSecondaryInfoRenderer"][
        "metadataRowContainer"]["metadataRowContainerRenderer"]["rows"]
    for row in row_data:
        label = row["metadataRowRenderer"]["title"]["runs"][0]["text"]
        v = row["metadataRowRenderer"]["contents"]
        if label == label_text and detail_type == "runs":
            v_list_1 = []
            for i in range(0,len(v)):
                v_list_1.append(v[i]["runs"][0]["text"])
            #return ",".join(v_list_1)
            return v
        elif label == label_text and detail_type == "simpleText":
            v_list_2 = []
            for i in range(0,len(v)):
                v_list_2.append(v[i]["simpleText"])
            return ",".join(v_list_2)

# calling respective functions

desc = Description()
provd = Other_Details("Provider","runs")
ratg = Other_Details("Rating","runs")
rels_date = Other_Details("Release date","simpleText")
run_time = Other_Details("Running time","simpleText")
aud = Other_Details("Audio","simpleText")
subs = Other_Details("Subtitle","simpleText")
if subs == None:subs = Other_Details("Subtitles","simpleText")
cast = Other_Details("Actor","runs")
if cast == None:cast = Other_Details("Actors","runs")
direc = Other_Details("Director","runs")
if direc == None:direc = Other_Details("Directors","runs")
prod =  Other_Details("Producer","runs")
if prod == None:prod = Other_Details("Producers","runs")
writer = Other_Details("Writer","runs")
if writer == None:writer = Other_Details("Writers","runs")
category = Other_Details("Genre","runs")
if category == None:category = Other_Details("Genres","runs")

c1,c2,c3,c4,c5,c6 = st.columns(6)
c7,c8,c9 = st.columns(3)
c10,c11 = st.columns(2)
c12,c13 = st.columns(2)

try :
    # row 1
    with c1:
         title = st.text_area("Title",title)
    with c2:
         provd = st.text_area("Provider", provd)
    with c3:
         ratg = st.text_area("Rating",ratg)
    with c4:
         rels_date = st.text_area("Release date", rels_date)
    with c5:
         run_time = st.text_area("Running time",run_time)
    # row 2
    with c6:
         subs = st.text_area("Subtitle",subs)
    with c7:
         aud = st.text_area("Audio", aud)
    with c8:
         category = st.text_area("Genres", category)
    with c9:
         direc = st.text_area("Director",direc)
    # row 3
    with c10:
         prod = st.text_area("Producers", prod)
    with c11:
         writer = st.text_area("Writers",writer)
    # row 4
    with c12:
         cast = st.text_area("Actors", cast,height=240)
    with c13:
         desc = st.text_area("Description", desc, height=240)
    genstr = title + "|" + desc + "|" + provd + "|" + ratg + "|" + rels_date + "|" + run_time + "|" + aud + "|" + subs + "|" \
             + cast + "|" + direc + "|" + prod + "|" + writer + "|" + category
    st.sidebar.download_button(label="Download Ouput", data=genstr, file_name="Output.txt", mime="text/plain")
except Exception as e:
        st.error(e)



