import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
from utils.preProcess import preProcessing
from utils import variables



def scraper(url):
    response = requests.get(url)
    # if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract article title
    title_tag = soup.find('h1', class_='entry-title')
    title = title_tag.text.strip() if title_tag else ""

    # Extract article text
    content_div = soup.find('div', class_='td-post-content tagdiv-type')
    paragraphs = []
    if content_div:
        # Extract text from all paragraph tags within the div
        paragraphs = content_div.find_all('p')
    article_text = []
    for p in paragraphs:
        article_text.append(p.get_text(strip=True))
    article_text = "\n".join(article_text)
    return title, article_text

# Preprocessing
stop_words, pos_words, neg_words = preProcessing()


# Read excel file
input = 'Input.xlsx'
output_directory = 'output_articles'

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Read excel
df = pd.read_excel(input)

# WEB SCRAPING
# Iterate through excel and save the article files

# if len(os.listdir(output_directory)) == 0:
print("Checking for articles...")
for index, urls in df.iterrows():
    url_id = urls['URL_ID']
    url = urls['URL']
    title, text = scraper(url)
    file_name = f"{url_id}.txt"
    file_path = os.path.join(output_directory, file_name)
    if os.path.exists(file_path):
        pass
    else:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"{title}\n")
            file.write(text)
        print(f"Created {url_id}.txt")

# Fetching Variables
ANALYSIS_METRICS = variables.analyticsMetrics()

# printing the total number of files in output_articles
file_count = len([f for f in os.listdir(output_directory) if f.endswith(".txt")])

# Write to Excel
output_df = pd.DataFrame(ANALYSIS_METRICS)
with pd.ExcelWriter('Output Data Structure.xlsx',mode='a',engine='openpyxl',if_sheet_exists='overlay') as writer:
    output_df.to_excel(writer,sheet_name='Sheet1',startcol=2, startrow=1, header=False, index=False)
