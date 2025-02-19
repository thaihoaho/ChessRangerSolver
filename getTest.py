from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--size", type=int, default=4, help="Kích thước")
parser.add_argument("--num_test", type=int, default=1, help="Số lượng test")

args = parser.parse_args()

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-images")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
options.page_load_strategy = "eager"
options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

for iteration in range(args.num_test):
    print(f"test {iteration + 1}", end=": ")

    driver.get(f"https://www.puzzle-chess.com/chess-ranger-{args.size}/")

    try:
        div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "board-pieces")))
        print("found")
        child_divs = div.find_elements(By.XPATH, "./div") 
        matrix = [['.' for _ in range(8)] for _ in range(8)]
        for i, child in enumerate(child_divs, 1):
            class_name = child.get_attribute("class")
            top = child.value_of_css_property("top").replace("px", "")
            top = int((int(top) - 5) / 30)
            left = child.value_of_css_property("left").replace("px", "")
            left = int((int(left) - 5) / 30)
            icon_name = class_name.split("icon-w")[-1]
            matrix[top][left] = icon_name

        with open(f"tests/test{args.size}.txt", "a", encoding="utf-8") as file:
            file.write(repr(matrix) + "\n")

    except Exception as e:
        print("error:", e)

driver.quit()
