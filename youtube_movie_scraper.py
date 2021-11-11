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

    # extract Rating , Release date, runtime
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
        v = row["metadataRowRenderer"]["contents"][0]
        if label == label_text and detail_type == "runs":
            return v["runs"][0]["text"]
        elif label == label_text and detail_type == "simpleText":
            return v["simpleText"]


desc = Description()
provd = Other_Details("Provider","runs")
ratg = Other_Details("Rating","runs")
rels_date = Other_Details("Release date","simpleText")
run_time = Other_Details("Running time","simpleText")
aud = Other_Details("Audio","simpleText")
subs = Other_Details("Subtitle","simpleText")
cast = Other_Details("Actors","runs")
direc = Other_Details("Director","runs")
prod =  Other_Details("Producers","runs")
writer = Other_Details("Writers","runs")
category = Other_Details("Genres","runs")

c1,c2,c3,c4 = st.columns(4)
c5,c6,c7,c8 = st.columns(4)
c9,c10,c11,c12 = st.columns(4)

try :
    with c1:
         st.text_area("Title",title)
    with c2:
         st.text_area("Provider", provd)
    with c3:
         st.text_area("Rating",ratg)
    with c4:
         st.text_area("Release date", rels_date)
    with c5:
         st.text_area("Running time",run_time)
    with c6:
         st.text_area("Audio", aud)
    with c7:
         st.text_area("Subtitle",subs)
    with c8:
         st.text_area("Genres", category)

    with c9:
         st.text_area("Director",direc)
    with c10:
         st.text_area("Producers", prod)
    with c11:
         st.text_area("Writers",writer)
    with c12:
         st.text_area("Actors", cast)
    st.text_area("Description", desc, height=200)
except Exception as e:
        st.error(e)
