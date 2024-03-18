import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import base64  # Add this import for base64 encoding

def get_search_results(keyword):
    url = f"https://www.google.co.in/search?q={'+'.join(keyword.split())}&num=60&gl=in&hl=en"
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
    results = soup.find_all('div', class_='yuRUbf')
    urls_ranking = []
    for i, result in enumerate(results, start=1):
        url = result.find('a')['href']
        urls_ranking.append(url)
        if domain.lower() in result.get_text().lower():
            return i, urls_ranking
    return None, urls_ranking

def clean_domain(domain):
    domain = domain.lower()
    if domain.startswith('http://') or domain.startswith('https://'):
        domain = domain.split("//")[-1]
    if domain.startswith('www.'):
        domain = domain.split("www.")[-1]
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
        urls_ranking_data = []
        for keyword in keywords_list:
            search_results = get_search_results(keyword)
            if search_results:
                ranking, urls_ranking = find_domain_ranking(search_results, clean_domain(domain))
                urls_ranking_data.append(urls_ranking)
                if ranking:
                    data.append([keyword, ranking])
                else:
                    data.append([keyword, "Not Found"])
            else:
                data.append([keyword, "Failed"])

        df = pd.DataFrame(data, columns=["Keyword", "Ranking"])

        # Display the table without the "URLs Ranking" column
        st.table(df)

        # Add a download button to download the data as a CSV file
        if st.button("Download CSV"):
            df_with_urls = df.copy()
            df_with_urls["URLs Ranking"] = urls_ranking_data
            csv = df_with_urls.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="domain_rankings.csv">Download CSV File</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
