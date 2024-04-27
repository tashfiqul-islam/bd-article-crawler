# BD News Article Crawler - WIP

```plaintext
bd_news_crawler/ 
│
├── src/
│   ├── crawlers/
│   |   ├── bdp_crawler.py # Crawler for BD Pratidin website
│   |   ├── bn24_crawler.py # Crawler for BanglaNews24 website
│   ├── tokenization/
|   |   |── bn_tokenizer.py # tokenizer for Bangla language
│
├── data/ 
│   ├── newspaper_articles/
│   |   ├── bdp_articles.json # JSON file for articles crawled from BD Pratidin
│   |   ├── bn24_articles.json # JSON file for articles crawled from BanglaNews24
|   |── NewsArticle.json # JSON file for the compiled list
│
├── LICENSE # License file
├── README.md # Project README file
├── output.txt # Output file for the tokenization
├── requirements.txt # Python dependencies
```
