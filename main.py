import streamlit as st
from utils import scrape, parse, split, llm_parse

url = st.text_input("Enter URL to start scraping")

if st.button("Scrape"):
    html = scrape(url)
    content = parse(html)
    
    st.session_state.scraped_content = content

    with st.expander("Scraped Content"):
        st.text_area("Content", content, height=400)

if st.session_state.get("scraped_content"):
    user_prompt = st.text_area("Enter user prompt")
    if st.button("Parse"):
        chunks = split(st.session_state.scraped_content)
        res = llm_parse(chunks, user_prompt)
        st.text_area("Parsed Content", res, height=400)