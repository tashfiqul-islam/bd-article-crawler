"""
This module contains the BanglaNews24Crawler class which is used to crawl 
news articles from the BanglaNews24 website.
"""

import json
from datetime import datetime, timedelta
import re
import requests
from bs4 import BeautifulSoup


class BanglaNews24Crawler:
    """
    A class to crawl news articles from the BanglaNews24 website.
    """

    def __init__(self):
        """
        Initializes the BanglaNews24Crawler class.
        """
        self.articles = []

    def fetch_all_categories(self, base_url):
        """
        Fetches all category URLs from the homepage of BanglaNews24 website.

        Args:
            base_url (str): The base URL of the website.
        """
        try:
            print("Fetching all categories from URL:", base_url)
            response = requests.get(base_url, timeout=5)
            soup = BeautifulSoup(response.content, "html.parser")
            all_category_links = self.extract_category_links(soup)
            return all_category_links
        except requests.exceptions.RequestException as e:
            print("Failed to fetch categories:", e)
            return None  # Return None in case of failure

    def extract_category_links(self, soup):
        """
        Extracts category URLs from the homepage soup.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the homepage.

        Returns:
            list: List of category URLs.
        """
        extracted_links = []
        categories = soup.find_all("li", class_="dropdown")
        for category in categories:
            category_link = category.find("a").get("href")
            extracted_links.append(category_link)
        return extracted_links

    def fetch_articles(self, links, start_date_param, end_date_param):
        """
        Fetches articles from the specified category URLs for a specified date range.

        Args:
            links (list): List of category URLs.
            start_date_param (datetime): The start date of the article search range.
            end_date_param (datetime): The end date of the article search range.
        """
        for category_link in links:
            try:
                current_date = start_date_param
                while current_date <= end_date_param:
                    date_str = current_date.strftime("%Y/%m/%d")
                    url = f"{category_link}?date={date_str}"
                    print("Fetching articles from URL:", url)
                    self.parse_archive(url)
                    current_date += timedelta(days=1)
            except requests.exceptions.RequestException as e:
                print("Failed to fetch articles from category:", category_link, e)

    def parse_archive(self, url):
        """
        Parses the archive page to extract article URLs.

        Args:
            url (str): The URL of the archive page.
        """
        try:
            archive_soup = requests.get(url, timeout=10)
            soup = BeautifulSoup(archive_soup.content, "html.parser")
            all_links = soup.find_all("a")
            for link in all_links:
                link_separator = link.get("href")
                link_tokens = link_separator.split("/")
                if (
                    len(link_tokens) == 7
                    and link_tokens[4] == "news"
                    and link_tokens[5] == "bd"
                ):
                    article_url = link_separator
                    self.parse_article(article_url)
        except requests.exceptions.RequestException as e:
            print("Failed to parse archive:", e)

    def parse_article(self, url):
        """
        Parses the article page to extract relevant information.

        Args:
            url (str): The URL of the article page.
        """
        try:
            print(f"Fetching article from URL: {url}")
            article_soup = BeautifulSoup(
                requests.get(url, timeout=10).text, "html.parser"
            )

            # Extracting title
            title_tag = article_soup.find("img", class_="lazy-load")
            title = title_tag["alt"].strip() if title_tag else None

            # Extracting date
            date_tag = article_soup.find("spam", class_="time")
            if date_tag:
                date_str = date_tag.get_text().strip()
                # Remove "আপডেট:" from the date string
                date = date_str.replace("আপডেট:", "").strip()
            else:
                date = None

            # Extracting content
            content_tag = article_soup.find("article")
            content_parts = content_tag.find_all("p")

            # Initialize an empty list to hold the sentences
            content_sentences = []

            class CustomStopIteration(Exception):
                """
                Custom exception used to break out of nested loops.
                """

            try:
                # Iterate over each paragraph
                for p in content_parts:
                    # Split the paragraph into sentences
                    sentences = p.get_text().replace("\n", " ").strip().split(".")
                    # Iterate over each sentence
                    for sentence in sentences:
                        # Find "বাংলাদেশ সময়:" or "সৌজন্যে:", stop processing this paragraph
                        if sentence.strip().startswith(
                            "বাংলাদেশ সময়:"
                        ) or sentence.strip().startswith("সৌজন্যে:"):
                            raise CustomStopIteration
                        # Otherwise, add the sentence to the list
                        content_sentences.append(sentence)
            except CustomStopIteration:
                pass

            # Combine all sentences to get the main content
            content = " ".join(content_sentences)

            # Remove extra spaces
            content = re.sub(" +", " ", content)

            # Extracting author
            author_tag = article_soup.find("div", class_="row news-source")
            author = (
                author_tag.find("span").get_text().strip().split("|")[0]
                if author_tag
                else "Unknown"
            )

            # Extracting category
            category_tag = article_soup.find("div", class_="section-page-title")
            category = (
                category_tag.find("h1").get_text().strip()
                if category_tag
                else "Unknown"
            )

            self.articles.append(
                {
                    "title": title if title else "Unknown",
                    "date": date if date else "Unknown",
                    "author": author,
                    "content": content,
                    "category": category,
                    "url": url,
                }
            )
        except requests.exceptions.RequestException as e:
            print("Failed to parse article:", e)
        except AttributeError as e:
            print("Failed to find necessary elements in the article:", e)

    def save_articles_to_json(self, output_file):
        """
        Saves the crawled articles to a JSON file.

        Args:
            output_file (str): The path to the output JSON file.
        """
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.articles, f, ensure_ascii=False, indent=4)
        print("Article data saved to JSON file")


if __name__ == "__main__":
    # Initialize the crawler
    crawler = BanglaNews24Crawler()

    # Define the parameters
    BASE_URL = "https://www.banglanews24.com/"
    START_DATE = datetime(2024, 3, 30)  # Start date
    END_DATE = datetime(2024, 3, 30)  # End date

    # Fetch all categories
    category_links = crawler.fetch_all_categories(BASE_URL)

    # Fetch articles for each category and save to JSON
    if category_links:
        crawler.fetch_articles(category_links, START_DATE, END_DATE)
        crawler.save_articles_to_json("./data/banglanews24_articles.json")
