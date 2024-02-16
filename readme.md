## Readme.md

This Github repository contains Python code for web scraping from the internet and storing the scraped data in a .csv file for further usage in a RAG-based model. The code uses the following Python libraries: `csv`, `yfinance`, `googlesearch`, `bs4`, `selenium`, `langchain.retrievers`, and `langchain.document_loaders`.

### How to use the code

1. Clone the repository to your local machine.
2. Install the required Python libraries using `pip install -r requirements.txt`.
3. Run the `main()` function in the `main.py` file.
4. The scraped data will be stored in .csv files in the same directory as the `main.py` file.

### Code explanation

The `search_google(query)` function searches Google for the given query and returns a list of URLs. The `scrape_data(url)` function scrapes the text data from the given URL using Selenium and BeautifulSoup. The `save_to_csv(filename)` function saves the scraped data to a .csv file with the given filename. The `scarape_financial_data(filename)` function scrapes financial data for a specific company using the `yfinance` library and saves it to a .csv file with the given filename. The `main()` function runs the above functions for a list of queries and saves the scraped data to .csv files.

### Steps Involved

- Each query are searched in a googlesearch api to get the top k (k = 10) links from the google.com.
- All the url links are iterate over and send to the `scrape_data(url)` function to scrape the data using selenium.
- In the `scrape_data(url)` function, an instance of the Chrome driver with the required configurations are created and the url is given to the driver.
- In the function the driver is setup to collect either pdfs, arxiv links or normal html.
- For pdfs and arxiv links, langchain retrievers are used for the extraction of the data.
- As per the HTML, only the tag of `["h1", "h2", "h3", "h4", "h5", "p"]` are selected and the content insdie these tags are extracted.
- The extracte content are further processed to convert into tokens which is suitable format for the RAG based vector database

### Challenges Faced

- Encoding error in some html webpages, The content in the webpages are not meant to be in a standard encoding lik utf-8 so, I have to look it up to find how to remove the non-encoded characters from the html. The outcome for this change you will find the in the csv file with some characters that are non english language.
- Some errors encountered while scraping particular websites which involves third-party cookie blocked error, permission errors, and other such. For that some more configurations are added to the drivers to counter those errors.
