"""
Tokenization of Bengali news articles using NLTK and tokenizers library.
"""

import json
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from tokenizers import Tokenizer, models, pre_tokenizers, decoders, trainers

# Download NLTK data
nltk.download('punkt')

def tokenize_with_nltk(text):
    """
    Tokenizes the text using NLTK.

    Args:
        text (str): The text to tokenize.

    Returns:
        list: List of sentences and words.
    """
    sentences = sent_tokenize(text)
    words = [word_tokenize(sentence) for sentence in sentences]
    return sentences, words

def tokenize_with_tokenizers(text):
    """
    Tokenizes the text using tokenizers library.

    Args:
        text (str): The text to tokenize.

    Returns:
        list: List of tokens.
    """
    tokenizer = Tokenizer(models.BPE())
    tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel()
    tokenizer.decoder = decoders.ByteLevel()
    tokenizer.trainer = trainers.BpeTrainer(
        special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"]
    )
    tokenizer.train_from_iterator([text])
    encoding = tokenizer.encode(text)
    tokens = encoding.tokens
    return tokens

def main():
    """
    Main function to tokenize Bengali news articles.
    """
    # Load data from JSON file
    with open('data/NewsArticle.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Ensure data is in the correct format
    if isinstance(data, dict):
        content = data["content"]
    elif isinstance(data, list):
        content = data[0]["content"]
    else:
        print("Invalid data format.")
        return

    # Tokenize the content
    bengali_sentences, bengali_words = tokenize_with_nltk(content)
    bengali_tokens = tokenize_with_tokenizers(content)

    # Print tokenized data
    print("Sentences:")
    for sentence in bengali_sentences:
        print(sentence)

    print("\nWords:")
    for word_list in bengali_words:
        print(' '.join(word_list))

    print("\nTokens:")
    print(' '.join(bengali_tokens))

if __name__ == "__main__":
    main()
