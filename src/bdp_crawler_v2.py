"""
Bengali News Crawler Module.

This module provides a class to crawl Bengali news articles from a specific website.
"""

import json
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup


class BengaliNewsCrawler:
    """
    A class to crawl Bengali news articles from a specific website.
    """

    def __init__(self):
        self.articles = []

    def fetch_articles(self, base_url, start, end):
        """
        Fetches articles from the specified range of dates.

        Args:
            base_url (str): The base URL of the news website.
            start (datetime): The start date for fetching articles.
            end (datetime): The end date for fetching articles.
        """
        try:
            print(f"Fetching articles from URL: {base_url}")
            current_date = start
            while current_date <= end:
                archive_url = (
                    f"{base_url}{current_date.strftime('%Y/%m/%d')}/{current_date.day}"
                )
                self.parse_archive(archive_url)
                current_date += timedelta(days=1)
        except requests.RequestException as e:
            print("Failed to fetch articles:", e)

    def parse_archive(self, url):
        """
        Parses the archive page to extract individual article URLs.

        Args:
            url (str): The URL of the archive page.
        """
        try:
            print(f"Fetching articles from archive URL: {url}")
            archive_soup = BeautifulSoup(
                requests.get(url, timeout=10).content, "html.parser"
            )
            for link in archive_soup.find_all("a", href=True):
                link_tokens = link["href"].split("/")
                if len(link_tokens) == 5 and link_tokens[1].startswith("20"):
                    article_url = f"https://www.bd-pratidin.com/{link['href']}"
                    self.parse_article(article_url)
        except requests.RequestException as e:
            print("Failed to parse archive:", url, e)

    def parse_article(self, url):
        """
        Parses an individual article page to extract relevant information.

        Args:
          url (str): The URL of the article page.
        """
        try:
            print(f"Fetching article from URL: {url}")
            article_soup = BeautifulSoup(
                requests.get(url, timeout=10).content, "html.parser"
            )
            title_tag = article_soup.find("h1")
            date_tag = article_soup.find("div", class_="row p-3")
            author_tag = article_soup.find("div", class_="news-info ps-3 my-3")
            content_tag = article_soup.find_all("p")
            category_tag = article_soup.find("ol", class_="breadcrumb")

            title = title_tag.get_text(strip=True) if title_tag else "Unknown"
            date = date_tag.find("span").get_text(strip=True) if date_tag else "Unknown"
            author = (
                author_tag.find("h2").get_text(strip=True) if author_tag else "Unknown"
            )
            content = (
                "\n".join(p.get_text(strip=True) for p in content_tag)
                if content_tag
                else "Unknown"
            )
            category = (
                category_tag.find_all("li")[-2].get_text(strip=True)
                if category_tag
                else "Unknown"
            )

            self.articles.append(
                {
                    "title": title,
                    "date": date,
                    "author": author,
                    "content": content,
                    "category": category,
                    "url": url,
                }
            )
        except requests.RequestException as e:
            print("Failed to parse article:", url, e)
        except AttributeError as e:
            print("Failed to find necessary elements in the article:", url, e)

    def save_articles_to_json(self, output_file):
        """
        Saves the extracted articles to a JSON file.

        Args:
            output_file (str): The path to the output JSON file.
        """
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.articles, f, ensure_ascii=False, indent=4)
        print("Article data saved to JSON file")


if __name__ == "__main__":
    crawler = BengaliNewsCrawler()
    BASE_URL = "https://www.bd-pratidin.com/first-page/"
    start_date = datetime(2024, 3, 30)  # Start date
    end_date = datetime(2024, 3, 31)  # End date
    crawler.fetch_articles(BASE_URL, start_date, end_date)
    crawler.save_articles_to_json("./data/bdpratidin_articles.json")
