import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Setup WebDriver
options = Options()
options.add_argument("--start-maximized")
service = Service(r"C:\Users\k\Downloads\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

try:
    # Navigate to Amazon
    driver.get("https://www.amazon.eg/s?k=samsung&language=en")
    
    # Wait for product containers to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='a-section a-spacing-base']"))
    )

    # Extract all product containers
    product_containers = driver.find_elements(By.XPATH, "//div[@class='a-section a-spacing-base']")

    # Initialize lists to store product data
    products_data = []

    # Iterate through each product container
    for product in product_containers:
        try:
            # Extract title (relative XPath within the container)
            title_element = product.find_elements(By.XPATH, ".//div[@class='a-row a-color-secondary']")
            title = title_element[0].text if title_element else "NA"

            # Extract description (relative XPath within the container)
            description_element = product.find_elements(By.XPATH, ".//h2[@class='a-size-mini a-spacing-none a-color-base s-line-clamp-4']")
            description = description_element[0].text if description_element else "NA"

            # Extract price (relative XPath within the container)
            price_element = product.find_elements(By.XPATH, ".//span[@class='a-price-whole']")
            price = price_element[0].text if price_element else "NA"

            # Extract rating (relative XPath within the container)
            rating_element = product.find_elements(By.XPATH, ".//div[@class='a-row a-size-small']/span")
            if rating_element:
                aria_label = rating_element[0].get_attribute('aria-label')
                rating = aria_label.split(" out of 5 stars")[0].strip() if aria_label and "out of 5 stars" in aria_label else "NA"
            else:
                rating = "NA"

            # Append product data
            products_data.append((title, description, price, rating))

        except Exception as e:
            print(f"Error processing a product: {e}")
            continue

    # Save data to CSV
    output_file = "amazon_products_with_ratings.csv"
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Description", "Price", "Rating"])
        writer.writerows(products_data)

    print(f"Data saved successfully! {len(products_data)} products scraped.")
    input("Press Enter to exit the script and close the browser...")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Ensure browser closes
    # driver.quit()
    print("Script interrupted. The browser is still open.")