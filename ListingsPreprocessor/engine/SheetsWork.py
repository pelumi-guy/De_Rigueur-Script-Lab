import csv
import gspread
from google.oauth2.service_account import Credentials
import random
import re
from pprint import pprint

def get_listings():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)

    sheet_id = "1pHnJUuTXualuOE6wFtQm5SWkP2f-XGE51J2WbcHbY2Q"
    workbook = client.open_by_key(sheet_id)

    sheet = workbook.worksheet("Sheet1")
    data = sheet.get_all_values()

    return data


def shuffle_features(body):
    for col in body:
        description = col[19]

        # Define a regular expression pattern to match the features section
        pattern = r'(Features:)(.*?)(Price:)'

        # Find the features section using regular expressions
        matches = re.search(pattern, description, re.DOTALL)

        # Extract the features section
        features_prefix = matches.group(1)
        features_str = matches.group(2).strip()
        price_prefix = matches.group(3)

        # Split the features into a list of lines
        features_list = features_str.split('\n')

        # Shuffle the lines
        random.shuffle(features_list)

        # Join the shuffled lines back into a single string
        shuffled_features_str = '\n'.join(features_list)

        # Replace the original features section with the shuffled features section in the full string
        shuffled_description = description.replace(features_str, shuffled_features_str)

        col[19] = shuffled_description

def extract_active_listings():
    data = get_listings()

    headers = data[0]
    body = data[1:]

    active_listings = []

    for col in body:
        listing_pictures_dir = col[20]
        active_listings.append(listing_pictures_dir)

    return active_listings

def adjustPrices(body):
    for col in body:
        price = int(col[10])

        if price < 1_000_000_000:
            adjustment = round((random.randint(-2, 2) * random.random()), 3)

            mil_price = price / 1_000_000
            new_mil_price = mil_price + adjustment

            new_price = int(new_mil_price * 1_000_000)
        else:
            adjustment = round((random.randint(-2, 2) * random.random()), 6)

            bil_price = price / 1_000_000_000
            new_bil_price = bil_price + adjustment

            new_price = int(new_bil_price * 1_000_000_000)

        col[10] = new_price



def run():
    data = get_listings()

    headers = data[0]
    body = data[1:]

    # shuffle_features(body)
    # adjustPrices(body)

    random.shuffle(body)

    filename = 'NPC_Listings.csv'
    with open(filename, 'w', newline='' ) as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(body)

if __name__ == "__main__":
    run()

