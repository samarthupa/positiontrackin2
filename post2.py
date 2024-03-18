import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse

def get_search_results(keyword):
    url = f"https://www.google.co.in/search?q={'+'.join(keyword.split())}&num=60"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107 Safari/537",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        st.error("Failed to retrieve search results.")
        return None

def find_domain_ranking(html_content, domain):
    soup = BeautifulSoup(html_content, 'html.parser')
    results = soup.find_all('div', class_='tF2Cxc')
    urls_ranking = []
    for i, result in enumerate(results, start=1):
        url = result.find('a')['href']
        urls_ranking.append(url)
        if domain.lower() in result.get_text().lower():
            return i, urls_ranking
    return None, urls_ranking

def clean_domain(domain):
    parsed_domain = urlparse(domain)
    if parsed_domain.scheme and parsed_domain.netloc:
        return parsed_domain.netloc
    elif parsed_domain.netloc:
        return parsed_domain.netloc
    else:
        return domain

def main():
    st.title("Google Domain Ranking Checker")
    st.write("Enter the keywords and the domain you want to check.")

    keywords = st.text_area("Enter Keywords (one per line):")
    domain = st.text_input("Enter Domain (e.g., example.com):")

    if st.button("Check Ranking"):
        if not keywords.strip():
            st.error("Please enter at least one keyword.")
            return
        if not domain.strip():
            st.error("Please enter a domain to check.")
            return

        keywords_list = [keyword.strip() for keyword in keywords.split("\n") if keyword.strip()]

        data = []
        for keyword in keywords_list:
            search_results = get_search_results(keyword)
            if search_results:
                ranking, urls_ranking = find_domain_ranking(search_results, clean_domain(domain))
                if ranking:
                    data.append([keyword, ranking, urls_ranking])
                else:
                    data.append([keyword, "Not Found", urls_ranking])
            else:
                data.append([keyword, "Failed", urls_ranking])

        df = pd.DataFrame(data, columns=["Keyword", "Ranking", "URLs Ranking"])
        st.table(df)

if __name__ == "__main__":
    main()
