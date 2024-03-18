import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_search_results(keyword):
    url = f"https://www.google.co.in/search?q={'+'.join(keyword.split())}"
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
    for i, result in enumerate(results, start=1):
        if domain in result.get_text():
            return i
    return None

def main():
    st.title("Google Domain Ranking Checker")
    st.write("Enter the keywords and the domain you want to check.")

    keywords = st.text_input("Enter Keywords (separated by commas):")
    domain = st.text_input("Enter Domain (e.g., example.com):")

    if st.button("Check Ranking"):
        if not keywords:
            st.error("Please enter at least one keyword.")
            return
        if not domain:
            st.error("Please enter a domain to check.")
            return

        keywords_list = [keyword.strip() for keyword in keywords.split(",")]

        for keyword in keywords_list:
            st.subheader(f"Keyword: {keyword}")
            search_results = get_search_results(keyword)
            if search_results:
                ranking = find_domain_ranking(search_results, domain)
                if ranking:
                    st.success(f"The domain {domain} is ranked {ranking} for the keyword '{keyword}'.")
                else:
                    st.warning(f"The domain {domain} is not found in the search results for the keyword '{keyword}'.")
            else:
                st.error(f"Failed to retrieve search results for the keyword '{keyword}'.")

if __name__ == "__main__":
    main()
