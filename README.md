# Web Scraper with LLM Integration

This project is a web scraping and content parsing tool that uses Selenium for scraping, BeautifulSoup for HTML parsing, and a language model (LLM) for extracting specific information from the scraped content through prompts.

## Features

- **Web Scraping:** Uses Selenium to load and scroll through web pages, ensuring all content is captured, including lazy-loaded elements.
- **Content Parsing:** Cleans and extracts meaningful text content from raw HTML using BeautifulSoup.
- **Chunk Splitting:** Splits large text content into manageable chunks for processing.
- **LLM Integration:** Utilizes the Ollama LLM with LangChain to extract specific information based on user prompts. (Any LLM can be used for this part. Ollama was chosen for its cost and accessiblity not for its performance)
- **Streamlit UI:** Provides a simple interface for entering URLs, scraping content, and extracting insights.

## File Structure

### `utils.py`

Contains utility functions for scraping, parsing, splitting content, and interacting with the LLM.

- **`scrape(url, max_scroll=10):`**  
  Scrapes a webpage using Selenium, scrolling to load all content.

- **`parse(html):`**  
  Cleans and extracts text content from raw HTML.

- **`split(content, max_length=8000):`**  
  Splits large text content into smaller chunks for processing.

- **`llm_parse(chunks, user_prompt):`**  
  Interacts with the LLM to extract information based on a user-provided prompt.

### `main.py`

Streamlit interface.

- **`url` Input Field:** Allows the user to enter a URL for scraping.  
- **`Scrape` Button:** Initiates the scraping and parsing process.  
- **`User Prompt` Text Area:** Accepts a prompt describing the information to extract.  
- **`Parse` Button:** Processes the scraped content using the LLM based on the user prompt.  
- **Expandable Views:** Displays scraped and parsed content in a user-friendly format.

## Dependencies

- Python 3.8+
- Google Chrome & ChromeDriver
- Streamlit
- Selenium
- BeautifulSoup (bs4)
- LangChain
- Ollama LLM (configured for `llama3.1`)


