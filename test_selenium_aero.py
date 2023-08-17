from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("window-size=1920,1080")

#options = ChromeOptions()
#options.headless = True
driver = Chrome(options=options)
driver.get('https://www.kinoaero.cz/?sort=sort-by-data&cinema=2%2C3%2C7&hall=10%2C23%2C1%2C2%2C3') # https://www.kinoaero.cz/?sort=sort-by-data
#driver.maximize_window()
#driver.set_window_size(1920, 1080)
time.sleep(5)
driver.find_element(By.CLASS_NAME, 'custom-select__input-chevron').click()
time.sleep(1)
driver.find_element(By.CLASS_NAME, 'form-check-input').click()
driver.find_element(By.CLASS_NAME, 'custom-select__input-chevron-active').click()
time.sleep(5)
#driver.find_element(By.CLASS_NAME, 'program__movie-name').click()
projections = driver.find_element(By.ID, 'projections-ids').get_attribute('data-projections').split(',')
for projection in projections[:-1]:
    print(f'https://www.kinoaero.cz/?sort=sort-by-data&cinema=1%2C2%2C3%2C7&hall=10%2C23%2C1%2C2%2C3&projection={projection}')
print(len(projections))
driver.quit()