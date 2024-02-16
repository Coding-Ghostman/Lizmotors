import csv
import yfinance as yf
from googlesearch import search
from bs4 import BeautifulSoup


from langchain.retrievers import ArxivRetriever
from langchain.document_loaders import PyMuPDFLoader


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

SCRAPED_DATA = dict()


def search_google(query):
    links = []
    for link in search(query, tld="com", num=15, stop=10, pause=1):
        links.append(link)
    return links


def scrape_data(url):

    service = Service(executable_path="chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--enable-javascript")
    options.add_argument("--no-sandbox")
    options.add_experimental_option("prefs", {"download_restrictions": 3})
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options, service=service)

    print(f"scraping url: {url}...")
    driver.get(url)

    delay = 3
    try:
        WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.TAG_NAME, "body")))
        print(f"Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")

    # check if url is a pdf or arxiv link
    if url.endswith(".pdf"):
        loader = PyMuPDFLoader(url)
        text = str(loader.load())

    elif "arxiv" in url:
        doc_num = url.split("/")[-1]
        retriever = ArxivRetriever(load_max_docs=2)
        text = retriever.get_relevant_documents(query=doc_num)[0].page_content

    else:

        page_source = driver.execute_script("return document.body.outerHTML;")
        soup = BeautifulSoup(page_source, "html.parser")
        soup.encode(
            'utf-8', errors='ignore'
        ).decode('utf-8')

        # for script in soup(["script", "style"]):
        #     script.extract()

        text = ""
        tags = ["h1", "h2", "h3", "h4", "h5", "p"]
        for element in soup.find_all(tags):
            text += element.text + "\n"

    # For Creating individual tokens from the website
    lines = (line.strip() for line in text.splitlines())
    chunks = (token.strip() for line in lines for token in line.split(" "))
    tokens = "\n".join(chunk for chunk in chunks if chunk)

    SCRAPED_DATA[url] = tokens
    print("scraped data added")
    driver.quit()


def save_to_csv(filename):
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        fieldnames = list(SCRAPED_DATA.keys())
        w = csv.DictWriter(f, fieldnames)
        w.writeheader()
        w.writerow(SCRAPED_DATA)


def scarape_financial_data(filename):
    ticker = "GOEV"  # Change this to the Canoo ticker symbol
    company = yf.Ticker(ticker)
    financial_data = company.info

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = financial_data.keys()
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        writer.writerow(financial_data)


# Main function
def main():
    queries = ["Canoo financial performance revenue, profit margins, return on investment, expense structure", "Canoo industry size, growth rate, trends, key players",
               "Canoo main competitors market share, products, pricing, marketing", "Market trends changes in consumer behavior, technological advancements, competitive landscape"]

    for query_I, query in enumerate(queries):
        print(f"Query that is being searched right now : {query}\n\n\n\n")
        url_list = search_google(query)
        print(
            f"List of all the urls for the above query : {str(url_list)}\n\n")
        for url_I, url in enumerate(url_list):
            if url:
                scrape_data(url)

        save_to_csv(filename=f"data_scraped_{query}.csv")

    scarape_financial_data(filename=f"data_scraped_financial_data.csv")


if __name__ == "__main__":
    main()
