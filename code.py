import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
pip install newspaper3k

# Install necessary libraries
!pip install openpyxl beautifulsoup4
from google.colab import files

# Prompt to upload a file
uploaded = files.upload()
uploaded_file_name = next(iter(uploaded))
content = uploaded[uploaded_file_name]

df = pd.read_excel((content))


# Create a folder to store the extracted articles
output_folder = '/content/extracted_articles'
os.makedirs(output_folder, exist_ok=True)

# Function to extract article text from a given URL
def extract_article_text(url):
    try:
        # Fetch the web page content
        response = requests.get(url)
        response.raise_for_status()

        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract article title and text
        title = soup.title.text.strip() if soup.title else "Untitled"
        article_text = ' '.join([p.text for p in soup.select('p,content, script')])


        return title, article_text
    except Exception as e:
        print(f"Error extracting article from {url}: {e}")
        return None, None

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']

    # Extract article text
    title, article_text = extract_article_text(url)

    if title is not None and article_text is not None:
        # Save the extracted article to a text file
        output_file_path = os.path.join(output_folder, f"{url_id}.txt")
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(f"Title: {title}\n\n")
            file.write(article_text)

        print(f"Article for {url_id} saved to {output_file_path}")
    else:
        print(f"Skipping {url_id} due to extraction error.")

print("Extraction complete.")



!pip install openpyxl newspaper3k
import pandas as pd
import os
from newspaper import Article
from google.colab import files

# Install necessary libraries


# Prompt to upload a file
uploaded = files.upload()
uploaded_file_name = next(iter(uploaded))
content = uploaded[uploaded_file_name]

df = pd.read_excel((content))

# Create a folder to store the extracted articles
output_folder = '/content/extracted_articles'
os.makedirs(output_folder, exist_ok=True)

# Function to extract article text from a given URL using newspaper3k
def extract_article_text(url):
    try:
        # Create a newspaper3k Article object
        article = Article(url)

        # Download and parse the article
        article.download()
        article.parse()

        # Extract article title and text
        title = article.title.strip() if article.title else "Untitled"
        article_text = article.text

        return title, article_text
    except Exception as e:
        print(f"Error extracting article from {url}: {e}")
        return None, None

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']

    # Extract article text
    title, article_text = extract_article_text(url)

    if title is not None and article_text is not None:
        # Save the extracted article to a text file
        output_file_path = os.path.join(output_folder, f"{url_id}.txt")
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(f"Title: {title}\n\n")
            file.write(article_text)

        print(f"Article for {url_id} saved to {output_file_path}")
    else:
        print(f"Skipping {url_id} due to extraction error.")

print("Extraction complete.")



# In this code, I finally uploaded stopwords files and loaded them and then loaded extracted files. And then removed stopwords from extracted files.
# So, this code did uploading stopwords file from local pc and I attached extracted files from above path in colab only.
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import download
from google.colab import files
import nltk

nltk.download('punkt')
from google.colab import files

# Number of stopwords files
num_stopwords_files = 7

# Dictionary to store uploaded stop words content
uploaded_stopwords = {}

for i in range(num_stopwords_files):
    try:
        # Attempt to upload with UTF-8 encoding
        uploaded = files.upload()
        uploaded_stopwords[f'stopwords_{i + 1}.txt'] = list(uploaded.values())[0]
    except UnicodeDecodeError:
        try:
            # If UTF-8 fails, try uploading with Latin-1 encoding
            uploaded = files.upload(encoding='latin-1')
            uploaded_stopwords[f'stopwords_{i + 1}.txt'] = list(uploaded.values())[0]
        except UnicodeDecodeError:
            print(f"Error decoding stopwords_{i + 1}.txt. Please check the file encoding.")

# Check the uploaded stop words
for file_name, content in uploaded_stopwords.items():
    try:
        decoded_content = content.decode('utf-8')
    except UnicodeDecodeError:
        # If decoding with UTF-8 fails, try decoding with Latin-1
        decoded_content = content.decode('latin-1')

    print(f"Stop Words in {file_name}:\n{decoded_content}")


def load_stop_words(uploaded_stopwords):
    stop_words = set()

    for content in uploaded_stopwords.values():
        try:
            decoded_content = content.decode('utf-8')
        except UnicodeDecodeError:
            # If decoding with UTF-8 fails, try decoding with Latin-1
            decoded_content = content.decode('latin-1')

        stop_words.update(word_tokenize(decoded_content.lower()))

    return stop_words

# Load stopwords from the uploaded file
stop_words = load_stop_words(uploaded_stopwords)


# Create a folder for cleaned text files
cleaned_output_folder = '/content/cleaned_articles'
os.makedirs(cleaned_output_folder, exist_ok=True)

# Function to clean text by removing stop words
def clean_text(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        text = input_file.read()

    # Tokenize the text
    words = word_tokenize(text)

    # Remove stop words
    filtered_words = [word for word in words if word.lower() not in stop_words]

    # Join the filtered words back into text
    cleaned_text = ' '.join(filtered_words)

    # Save the cleaned text to a new file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(cleaned_text)

# Assuming your original 100 extracted text files are in the 'output_folder'
output_folder = '/content/extracted_articles'  # Replace with the actual path

# Iterate through each original text file
for filename in os.listdir(output_folder):
    if filename.endswith('.txt'):
        url_id = filename.split('.')[0]
        input_file_path = os.path.join(output_folder, filename)
        output_file_path = os.path.join(cleaned_output_folder, f"{url_id}_cleaned.txt")

        # Clean the text and save to a new file
        clean_text(input_file_path, output_file_path)

        print(f"Text for {url_id} cleaned and saved to {output_file_path}")

print("Cleaning complete.")

!pip install textstat

import os
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
from textstat import sentence_count, lexicon_count, syllable_count
import pandas as pd
nltk.download('vader_lexicon')

# Download NLTK data
nltk.download('punkt')

# Upload your positive and negative words files manually
# Click on the folder icon on the left sidebar, then click "Upload to Session Storage"
from google.colab import files

# Upload positive_words.txt
uploaded = files.upload()

# Save the uploaded file
with open('positive_words.txt', 'wb') as f:
    f.write(next(iter(uploaded.values())))

# Upload negative_words.txt
uploaded = files.upload()

# Save the uploaded file
with open('negative_words.txt', 'wb') as f:
    f.write(next(iter(uploaded.values())))

# Function to load positive and negative words from files
import chardet
from nltk.tokenize import word_tokenize

# Function to load positive and negative words from files
def load_sentiment_words(file_path):
    with open(file_path, 'rb') as rawdata:
        result = chardet.detect(rawdata.read(100000))  # Detect encoding of the first 100,000 bytes

    encoding = result['encoding']

    with open(file_path, 'r', encoding=encoding, errors='replace') as file:
        words = file.read().splitlines()

    return words

# Load positive and negative words
positive_words = load_sentiment_words('positive_words.txt')  # replace with actual path
negative_words = load_sentiment_words('negative_words.txt')  # replace with actual path

# Function to analyze sentiment and calculate metrics
def analyze_text(text):
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(text)
    positive_score = sum(1 for word in word_tokenize(text) if word.lower() in positive_words)
    negative_score = sum(1 for word in word_tokenize(text) if word.lower() in negative_words)

    avg_sentence_length = len(word_tokenize(text)) / sentence_count(text)
    complex_word_count = sum(1 for word in word_tokenize(text) if syllable_count(word) > 2)
    percentage_complex_words = (complex_word_count / lexicon_count(text)) * 100
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    return {
        'Positive Score': positive_score,
        'Negative Score': negative_score,
        'Polarity Score': scores['compound'],
        'Subjectivity Score': 1 - abs(scores['compound']),
        'Avg Sentence Length': avg_sentence_length,
        'Percentage of Complex Words': percentage_complex_words,
        'Fog Index': fog_index,
        'Avg Words per Sentence': len(word_tokenize(text)) / sentence_count(text),
        'Complex Word Count': complex_word_count,
        'Word Count': len(word_tokenize(text)),
        'Syllables per Word': sum(syllable_count(word) for word in word_tokenize(text)) / len(word_tokenize(text)),
        'Personal Pronouns': sum(1 for word in word_tokenize(text) if word.lower() in ['i', 'me', 'my', 'mine', 'myself']),
        'Avg Word Length': sum(len(word) for word in word_tokenize(text)) / len(word_tokenize(text))
    }


# Function to process all text files in a folder
def process_all_files(folder_path):
    results = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            result = analyze_text(text)
            result['Filename'] = filename  # Add filename to the result dictionary
            results.append(result)
    return results


# Replace 'path/to/your/files' with the actual path to the folder containing your 100 text files
folder_path = '/content/cleaned_articles'
analysis_results = process_all_files(folder_path)

# Convert results to a DataFrame for easy tabular representation
# df = pd.DataFrame(analysis_results)

# Display the DataFrame
# df
analysis_results = process_all_files(folder_path)

# Convert results to a DataFrame
df = pd.DataFrame(analysis_results)

output_filename = 'analysis_results.xlsx'
df.to_excel(output_filename, index=False)

# Download the Excel file
files.download(output_filename)

# Zip the individual Excel files into a single archive
archive_filename = 'analysis_results.zip'
!zip $archive_filename *_analysis.xlsx
