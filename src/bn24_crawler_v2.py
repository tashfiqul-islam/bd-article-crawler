"""
This module provides functionality to interact with JSON data.
"""

import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests


class BanglaNews24Crawler:
    """
    A class to crawl news articles from BanglaNews24 website.
    """

    def __init__(self):
        """
        Initializes the BanglaNews24Crawler class.
        """
        self.articles = []

    def fetch_articles(self, base_url_param, start_date_param, end_date_param):
        """
        Fetches articles from the BanglaNews24 website for a specified date range.

        Args:
            base_url_param (str): The base URL of the website.
            start_date_param (datetime): The start date of the article search range.
            end_date_param (datetime): The end date of the article search range.
        """
        try:
            current_date = start_date_param
            while current_date <= end_date_param:
                date_str = current_date.strftime("%Y/%m/%d")
                url = f"{base_url_param}category/জাতীয়/1?date={date_str}"
                print("Fetching articles from URL:", url)
                self.parse_archive(url)
                current_date += timedelta(days=1)
        except requests.exceptions.RequestException as e:
            print("Failed to fetch articles:", e)

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
            title_tag = article_soup.find("h1", class_="post-heading")
            title = title_tag.get_text().strip() if title_tag else None

            # Extracting date
            date_tags = article_soup.select(".news-article .time")
            date = date_tags[0].get_text().strip() if date_tags else None

            # Extracting content
            content_tag = article_soup.find("div", {"class": "details"})
            content_parts = content_tag.find_all("p")
            # Combine all paragraphs to get the main content
            content = "\n".join([p.get_text().strip() for p in content_parts])

            # Extracting author
            author_tag = article_soup.find("div", {"class": "row news-source"})
            author = (
                author_tag.find("span").get_text().strip().split("|")[0]
                if author_tag
                else "Unknown"
            )

            # Extracting category
            category_tag = article_soup.find("div", {"class": "section-page-title"})
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

    # Fetch articles and save to JSON
    crawler.fetch_articles(BASE_URL, START_DATE, END_DATE)
    crawler.save_articles_to_json("./data/banglanews24_articles.json")
