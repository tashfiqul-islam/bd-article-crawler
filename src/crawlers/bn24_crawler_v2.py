"""
This module contains the BanglaNews24Crawler class which is used to crawl 
news articles from the BanglaNews24 website.
"""

import json
from datetime import datetime, timedelta
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

            title = self.extract_title(article_soup)
            date = self.extract_date(article_soup)
            content = self.extract_content(article_soup)
            author = self.extract_author(article_soup)
            category = self.extract_category(article_soup)

            self.articles.append({
                "title": title,
                "date": date,
                "author": author,
                "content": content,
                "category": category,
                "url": url,
            })

        except requests.exceptions.RequestException as e:
            print("Failed to parse article:", e)
        except AttributeError as e:
            print("Failed to find necessary elements in the article:", e)

    def extract_title(self, soup):
        """
        Extracts the title from the article soup.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the article page.

        Returns:
            str: The title of the article.
        """
        title_tag = soup.find("img", class_="lazy-load")
        return title_tag["alt"].strip() if title_tag else "Unknown"

    def extract_date(self, soup):
        """
        Extracts the date from the article soup.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the article page.

        Returns:
            str: The date of the article.
        """
        date_tag = soup.find("span", class_="time")
        return date_tag.get_text().strip().replace("আপডেট:", "").strip() if date_tag else "Unknown"

    def extract_content(self, soup):
        """
        Extracts the content from the article soup.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the article page.

        Returns:
            str: The content of the article.
        """
        content_tag = soup.find("article")
        content_parts = content_tag.find_all("p")
        content_sentences = []

        for p in content_parts:
            sentences = p.get_text().replace("\n", " ").strip().split(".")
            for sentence in sentences:
                if sentence.strip().startswith("বাংলাদেশ সময়:") or \
                    sentence.strip().startswith("সৌজন্যে:"):
                    break
                content_sentences.append(sentence)

        return " ".join(content_sentences)

    def extract_author(self, soup):
        """
        Extracts the author from the article soup.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the article page.

        Returns:
            str: The author of the article.
        """
        author_tag = soup.find("div", class_="row news-source")
        return author_tag.find("span").get_text().strip().split("|")[0] if author_tag else "Unknown"

    def extract_category(self, soup):
        """
        Extracts the category from the article soup.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object of the article page.

        Returns:
            str: The category of the article.
        """
        category_tag = soup.find("div", class_="section-page-title")
        return category_tag.find("h1").get_text().strip() if category_tag else "Unknown"

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
