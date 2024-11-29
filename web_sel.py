import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Setup WebDriver
options = Options()
options.add_argument("--start-maximized")
service = Service(r"C:\Users\k\Downloads\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

try:
    # Navigate to Amazon
    driver.get("https://www.amazon.eg/s?k=samsung&language=en")

     # Extract product titles
    comapny_titles = driver.find_elements(By.XPATH, "//span[@class='a-size-base-plus a-color-base']")
    title = [t.text for t in comapny_titles]

    # Extract product descriptions
    descriptionS = driver.find_elements(By.XPATH, "//span[@class='a-size-base-plus a-color-base a-text-normal']")
    description = [d.text for d in descriptionS]

    # Extract prices
    price_elements = driver.find_elements(By.XPATH, "//span[@class='a-price']")
    prices = [p.text for p in price_elements]

    # Extract ratings
    # Extract ratings
    rating_elements = driver.find_elements(By.XPATH, "//div[@class='a-row a-size-small']/span")

    # Extract the 'aria-label' attribute for each rating element
    ratings = []
    for element in rating_elements:
        if element:
            aria_label = element.get_attribute('aria-label')
            if aria_label and "out of 5 stars" in aria_label:
                ratings.append(aria_label.split("rating details")[0].strip())
            else:
            # Append "NA" if aria-label is missing or doesn't contain the rating text
                ratings.append("NA")
        else:
            ratings.append("NA")  # Append NA for missing ratings

    # # Print the cleaned ratings
    # for rating in ratings:
    #     print(rating)

    # Extract total ratings (number of reviews)
    num_rating_elements = driver.find_elements(By.XPATH, "//span[@class='a-size-base s-underline-text']")
    num_rating = [nr.text for nr in num_rating_elements]



    # print(f"{len(comapny_titles)}and {len(descriptionS)}{len(prices)}")
    # data=[]
    # # Combine titles and descriptions into rows
    # for i in range(min(len(comapny_titles), len(descriptionS),len(prices))):
    #     data.append((title[i], description[i],price[i]))  # Append as a tuple


    


    
    # Print product names
    # for id,title in enumerate(comapny_titles, start=1):
    #     print(f"{id}{title.text}")

    output_file = "company_titles.csv"

    # with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    #    writer=csv.writer(file)
    #    writer.writerow(["Title"])  # Add header
    #    for title in title:
    #     writer.writerow([title])
    #    writer.writerow(["description"])  # Add header
    #    for description in description:
    #     writer.writerow([description])

    # print(f"Data saved to {output_file}")





    # with open (output_file,mode="w", newline="", encoding="utf-8") as file:

    #     writer = csv.writer(file)
    #     writer.writerow(["Title", "Description","Price"])  # Add headers
    #     writer.writerows(data)  # Write all rows
    # print(f"Data saved to {output_file}")





    # To handle cases where the lengths of the lists are different, you can normalize the lists by filling in missing values 
    # Find the maximum length among the lists

    # Handle varying lengths by padding with "Na"
    max_length = max(len(title), len(description), len(prices), len(ratings), len(num_rating))
    title.extend(["Na"] * (max_length - len(title)))
    description.extend(["Na"] * (max_length - len(description)))
    prices.extend(["Na"] * (max_length - len(prices)))
    ratings.extend(["Na"] * (max_length - len(ratings)))
    num_rating.extend(["Na"] * (max_length - len(num_rating)))

    # Combine all data into rows
    data = [(title[i], description[i], prices[i], ratings[i], num_rating[i]) for i in range(max_length)]

    
    
    


   # Save to CSV
    output_file = "amazon_products.csv"
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Description", "Price", "Rating", "Total Reviews"])
        writer.writerows(data)
    print(f"Data saved to {output_file}")


    print("Press Ctrl + C to stop the script.")

    # while True:
    #     time.sleep(10)  # Keep the script running and the browser open
    input("Press Enter to exit the script and close the browser...")
except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    print("Script interrupted. The browser is still open.")
    # Don't call driver.quit() here to prevent the browser from closing
    
