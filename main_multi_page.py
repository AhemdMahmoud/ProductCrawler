import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def scrape_amazon_page(driver, page_num):
    """Scrape a single page of Amazon search results."""
    products_data = []
    
    try:
        # Wait for product containers to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='a-section a-spacing-base']"))
        )

        # Extract all product containers
        product_containers = driver.find_elements(By.XPATH, "//div[@class='a-section a-spacing-base']")

        # Iterate through each product container
        for product in product_containers:
            try:
                # Extract title
                title_element = product.find_elements(By.XPATH, ".//span[@class='a-size-medium a-color-base a-text-normal']")
                title = title_element[0].text if title_element else "NA"

                # Extract description
                description_element = product.find_elements(By.XPATH, ".//h2[@class='a-size-mini a-spacing-none a-color-base s-line-clamp-4']")
                description = description_element[0].text if description_element else "NA"

                # Extract price
                price_element = product.find_elements(By.XPATH, ".//span[@class='a-price-whole']")
                price = price_element[0].text if price_element else "NA"

                # Extract rating
                rating_element = product.find_elements(By.XPATH, ".//div[@class='a-row a-size-small']/span")
                if rating_element:
                    aria_label = rating_element[0].get_attribute('aria-label')
                    rating = aria_label.split(" out of 5 stars")[0].strip() if aria_label and "out of 5 stars" in aria_label else "NA"
                else:
                    rating = "NA"

                # Append product data
                products_data.append((title, description, price, rating))

            except Exception as e:
                print(f"Error processing a product on page {page_num}: {e}")
                continue

        print(f"Scraped {len(products_data)} products on page {page_num}")
        return products_data

    except Exception as e:
        print(f"Error scraping page {page_num}: {e}")
        return products_data

def main():
    # Setup WebDriver
    options = Options()
    options.add_argument("--start-maximized")
    # Uncomment the next line to run in headless mode
    # options.add_argument("--headless")
    service = Service(r"C:\Users\k\Downloads\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    # Base URL for Amazon Egypt Samsung search
    base_url = "https://www.amazon.eg/s?k=samsung&page={}&language=en"
    
    # Number of pages to scrape
    max_pages = 5
    
    # Collect all products
    all_products = []

    try:
        # Iterate through pages
        for page_num in range(1, max_pages + 1):
            # Navigate to the specific page
            driver.get(base_url.format(page_num))
            
            # Random delay to avoid detection (optional but recommended)
            time.sleep(2)
            
            # Scrape the current page
            page_products = scrape_amazon_page(driver, page_num)
            all_products.extend(page_products)

        # Save data to CSV
        output_file = "amazon_samsung_products.csv"
        with open(output_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Description", "Price", "Rating"])
            writer.writerows(all_products)

        print(f"\nTotal products scraped: {len(all_products)}")
        print(f"Data saved to {output_file}")

    except Exception as e:
        print(f"An error occurred during scraping: {e}")

    finally:
        # Ensure browser closes
        driver.quit()

if __name__ == "__main__":
    main()