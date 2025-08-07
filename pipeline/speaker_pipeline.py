import requests
from bs4 import BeautifulSoup
import csv
import os
from dotenv import load_dotenv
import time
import openai

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not set. Please define it in a .env file.")
client = openai.OpenAI(api_key=api_key)

url = "https://www.gse.harvard.edu/directory/faculty"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

faculty_list = []

faculty_cards = soup.select('li.o-summary-directory')

def get_bio_from_profile(profile_url):
    try:
        resp = requests.get(profile_url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        bio_div = soup.find('div', class_='paragraph paragraph--type--text-block paragraph--view-mode--default o-wysiwyg')
        if bio_div:
            bio_text = ' '.join([p.get_text(separator=' ', strip=True) for p in bio_div.find_all('p')])
            return bio_text
    except Exception as e:
        print(f"Error fetching bio from {profile_url}: {e}")
    return ''

def get_keywords_from_bio(bio_text):
    if not bio_text.strip():
        return ''
    prompt = f"Extract 5-10 relevant academic or professional keywords from this background (comma separated):\n\n{bio_text}\n\nKeywords:"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0.3,
        )
        keywords = response.choices[0].message.content.strip()
        return keywords
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return ''

for card in faculty_cards[:15]:  # Adjust as needed
    # Name and profile URL
    name_elem = card.select_one('h3.o-summary-directory__heading a')
    name = name_elem.text.strip() if name_elem else None
    profile_url = 'https://www.gse.harvard.edu' + name_elem['href'] if name_elem else None

    # Title
    title_elem = card.select_one('.o-summary-directory__position')
    title = title_elem.text.strip() if title_elem else ''

    # Email
    email_elem = card.select_one('.o-summary-directory__email a')
    email = email_elem.text.strip() if email_elem else ''

    # Location
    location_elem = card.select_one('.o-summary-directory__location')
    location = location_elem.text.strip() if location_elem else ''

    background = ''
    keywords = ''
    if profile_url:
        background = get_bio_from_profile(profile_url)
        # To avoid rate limits
        time.sleep(1)
        keywords = get_keywords_from_bio(background)
        time.sleep(1)

    if name:
        first_name = name.split()[0]
        last_name = name.split()[-1]

        faculty_list.append({
            'first_name': first_name,
            'last_name': last_name,
            'name': name,
            'title': title,
            'email': email,
            'location': location,
            'url': profile_url,
            'company': "Harvard Graduate School of Education",
            'background': background,
            'keywords': keywords
        })

# Export to CSV
csv_columns = [
    'first_name', 'last_name', 'email', 'company', 'title',
    'background', 'experience', 'keywords', 'location'
]

csv_path = 'data/new_speakers.csv'
os.makedirs(os.path.dirname(csv_path), exist_ok=True)
with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for f in faculty_list:
        row = {
            'first_name': f['first_name'],
            'last_name': f['last_name'],
            'email': f['email'],
            'company': f['company'],
            'title': f['title'],
            'background': f.get('background', ''),
            'experience': '',
            'keywords': f.get('keywords', ''),
            'location': f['location']
        }
        writer.writerow(row)
print(f"\nExported to {csv_path}\n")
