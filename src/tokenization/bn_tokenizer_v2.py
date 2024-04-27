"""
Tokenization of Bengali news articles using NLTK and tokenizers library.
"""

import os
import nltk
from indicnlp.tokenize import indic_tokenize


def download_nltk_resources():
    """
    Download necessary NLTK resources.
    """
    nltk.download("punkt", download_dir="nltk_data")


def set_nltk_data_path():
    """
    Set NLTK data path to the appropriate directory.
    """
    nltk_data_dir = os.path.join(os.path.dirname(__file__), 'nltk_data')
    nltk.data.path.append(nltk_data_dir)


def tokenize_characters(text):
    """
    Tokenize the input text into characters.

    Args:
        text (str): The input text to be tokenized.

    Returns:
        list: A list of characters tokenized from the input text.
    """
    return [char for char in text if char.strip()]


def tokenize_words(text):
    """
    Tokenize the input text into words.

    Args:
        text (str): The input text to be tokenized.

    Returns:
        list: A list of words tokenized from the input text.
    """
    return indic_tokenize.trivial_tokenize(text)


def tokenize_sentences(text):
    """
    Tokenize the input text into sentences.

    Args:
        text (str): The input text to be tokenized.

    Returns:
        list: A list of sentences tokenized from the input text.
    """
    return text.split("।")


def main():
    """
    Tokenize different sections of a Bengali news article and print the tokens.
    """
    # Download NLTK resources if not already downloaded
    download_nltk_resources()

    # Set NLTK data path
    set_nltk_data_path()

    # Sample Bengali news article
    data = {
        "title": "প্রথম সেশনে  এক উইকেটই নিতে পারলো বাংলাদেশ",
        "date": "১২০৫ ঘণ্টা, মার্চ ৩১, ২০২৪",
        "author": "স্টাফ করেসপন্ডেন্ট, স্পোর্টস ",
        "content": "দিনের শুরুতে আকাশে মেঘ। কিন্তু ম্যাচের ভাগ্যে কোনো বদল এলো না তবুও। স্বস্তি কেবল সাকিব আল হাসানের উইকেট। প্রথম দিনের শেষেই বড় রানের পথে থাকা শ্রীলঙ্কার কাছে এখন সেটি বাস্তব। চট্টগ্রামের জহুর আহমেদ চৌধুরী স্টেডিয়ামে দুই ম্যাচ টেস্ট সিরিজের শেষটিতে মুখোমুখি হয়েছে বাংলাদেশ-শ্রীলঙ্কা। প্রথম ইনিংসে ব্যাট করতে নেমে দ্বিতীয় দিনের প্রথম সেশন শেষে ৫ উইকেট হারিয়ে ৪১১ রান করেছে লঙ্কানরা। দ্বিতীয় দিনের সকালে আকাশ ছিল বেশ মেঘলা। পুরো প্রথম সেশনেই ছিল মেঘের আনাগোনা। যদিও শেষ অবধি বৃষ্টি আসেনি। কিন্তু ম্যাচের ধরন থেকে গেছে একই। দিনের প্রথম ঘণ্টায় লঙ্কানদের কোনো উইকেট তুলে নিতে পারেনি বাংলাদেশ। প্রথম সাত ওভার পেসারদের দিয়ে করানোর পর সপ্তম ওভারে গিয়ে স্পিনার আনেন অধিনায়ক শান্ত। একপ্রান্তে স্পিন, আরেকদিকে পেসার; কিছুক্ষণ এমন চেষ্টার পর দুই দিক থেকেই স্পিনার নিয়ে আসেন তিনি। এ দফায় সফল হন। উইকেট এনে দেন সাকিব আল হাসান। অফ স্টাম্পের বাইরে ফুল লেংথে ঝুলিয়ে দেন সাকিব। সামনের পায়ে এসে ডিফেন্স করার চেষ্টা করেন চান্দিমাল। তার ব্যাট ছুয়ে বল চলে যায় উইকেটরক্ষক লিটন কুমার দাসের গ্লাভসে। ভেঙে যায় চান্দিমালের সঙ্গে ধনঞ্জয়ার ৮৯ রানের জুটি। এরপর উইকেটে আসেন কামিন্দু মেন্ডিস। তিনি ও ধনঞ্জয়া প্রথম টেস্টের দুই ইনিংসেই সেঞ্চুরি করেছিলেন, গড়েছিলেন বড় জুটি। লাঞ্চ বিরতি অবধি ৭৬ বলে ৩৬ রানের জুটি হয়ে গেছে তাদের। ১০৮ বলে ৭০ রান করে ধনঞ্জয়া ও ৪১ বলে ১৭ রানে অপরাজিত কামিন্দু। বাংলাদেশ সময় : ১২০৩ ঘণ্টা, ৩১ মার্চ, ২০২৪  এমএইচবি",
        "category": "ক্রিকেট",
        "url": "https://www.banglanews24.com/cricket/news/bd/1306708.details",
    }

    # Tokenize each section of the data
    title_tokens_char = tokenize_characters(data["title"])
    title_tokens_word = tokenize_words(data["title"])
    title_tokens_sentence = tokenize_sentences(data["title"])

    date_tokens_char = tokenize_characters(data["date"])
    date_tokens_word = tokenize_words(data["date"])
    date_tokens_sentence = tokenize_sentences(data["date"])

    author_tokens_char = tokenize_characters(data["author"])
    author_tokens_word = tokenize_words(data["author"])
    author_tokens_sentence = tokenize_sentences(data["author"])

    content_tokens_char = tokenize_characters(data["content"])
    content_tokens_word = tokenize_words(data["content"])
    content_tokens_sentence = tokenize_sentences(data["content"])

    category_tokens_char = tokenize_characters(data["category"])
    category_tokens_word = tokenize_words(data["category"])
    category_tokens_sentence = tokenize_sentences(data["category"])

    # Print tokenized data
    print("\nTokens:")
    print("Title:")
    print("- Characters:", " ".join(title_tokens_char))
    print("- Words:", " ".join(title_tokens_word))
    print("- Sentences:", " ".join(title_tokens_sentence))
    print("\nDate:")
    print("- Characters:", " ".join(date_tokens_char))
    print("- Words:", " ".join(date_tokens_word))
    print("- Sentences:", " ".join(date_tokens_sentence))
    print("\nAuthor:")
    print("- Characters:", " ".join(author_tokens_char))
    print("- Words:", " ".join(author_tokens_word))
    print("- Sentences:", " ".join(author_tokens_sentence))
    print("\nContent:")
    print("- Characters:", " ".join(content_tokens_char))
    print("- Words:", " ".join(content_tokens_word))
    print("- Sentences:", " ".join(content_tokens_sentence))
    print("\nCategory:")
    print("- Characters:", " ".join(category_tokens_char))
    print("- Words:", " ".join(category_tokens_word))
    print("- Sentences:", " ".join(category_tokens_sentence))


if __name__ == "__main__":
    main()
