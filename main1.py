import requests
from bs4 import BeautifulSoup
import lxml
import csv
import re
import time
import random
import os

def web_scrapper2(web_url, file_name):
    print('Thank you for sharing the URL and file name!\nReading the content...')

    # Add a random delay to mimic human behavior
    time.sleep(random.randint(3, 7))

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'
    }

    response = requests.get(web_url, headers=headers)

    if response.status_code == 200:
        print('Connected to the website')
        soup = BeautifulSoup(response.text, "html.parser")
        hotel_divs = soup.find_all('div', role="listitem")

        file_exists = os.path.isfile(f'{file_name}.csv')

        with open(f'{file_name}.csv', 'a', newline="", encoding='utf-8') as file_csv:
            writer = csv.writer(file_csv)

            # Write header only if file is new
            if not file_exists:
                writer.writerow(['Hotel_Name', 'Location', 'Price', 'Rating', 'Score', 'Total_Review', 'Link'])

            for hotel in hotel_divs:
                try:
                    hotel_name = hotel.find('div', class_='f6431b446c a15b38c233')
                    hotel_name = hotel_name.text.strip() if hotel_name else 'NaN'

                    location = hotel.find('span', class_="aee5343fdb def9bc142a")
                    location = location.text.strip() if location else 'NaN'

                    price = hotel.find('span', class_="f6431b446c fbfd7c1165 e84eb96b1f")
                    price = price.text.strip().replace('₹', '') if price else 'NaN'

                    review_text = hotel.find('div', class_="a3b8729ab1 e6208ee469 cb2cbb3ccb")
                    review_text = review_text.text if review_text else 'NaN'

                    score = hotel.find('div', class_="a3b8729ab1 d86cee9b25")
                    score = score.text.split(' ')[-1] if score else 'NaN'

                    total_review = hotel.find('div', class_="abf093bdfe f45d8e4c32 d935416c47")
                    total_review = total_review.text if total_review else 'NaN'

                    link = hotel.find('a', href=True)
                    link = link.get('href') if link else 'NaN'

                    writer.writerow([hotel_name, location, price, review_text, score, total_review, link])

                except Exception as e:
                    print("Error extracting hotel data:", e)

        print('Web scraping completed and data added to file.')

    else:
        print(f' Connection failed! Status code: {response.status_code}')


# Run if executed directly
if __name__ == '__main__':
    url = input("Please enter the Booking.com URL: ")
    file_name = input("Please enter the file name (without .csv): ")

    web_scrapper2(url, file_name)
