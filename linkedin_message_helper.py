from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# ---- Setup Chrome driver ----
driver = webdriver.Chrome()
driver.maximize_window()

# ---- Open LinkedIn login ----
driver.get('https://www.linkedin.com/login')

# ---- Login ----
email_input = driver.find_element(By.ID, 'username')
email_input.send_keys('YOUR_EMAIL')  # replace with your email
password_input = driver.find_element(By.ID, 'password')
password_input.send_keys('YOUR_PASSWORD')  # replace with your password
password_input.send_keys(Keys.ENTER)

# ---- Wait for login to complete ----
time.sleep(10)

# ---- Go to connections page ----
driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')
time.sleep(5)

# ---- Scroll down to load more connections ----
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# ---- Send messages safely ----
message_buttons = driver.find_elements(By.XPATH, "//span[text()='Message']")
print(f"Found {len(message_buttons)} connections with Message button.")

for button in message_buttons:
    try:
        # Click the message button
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)  # small wait for modal to open

        # Wait for the message textbox to appear
        message_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
        )

        # Type your message
        message_input.send_keys("Hello! This is a friendly test message 🙂")
        message_input.send_keys(Keys.ENTER)

        print("Message sent to one connection!")

        # Close the message modal
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Dismiss']"))
        )
        close_button.click()
        time.sleep(1)

    except Exception as e:
        print(f"Skipped one connection: {e}")
        continue

print("All messages attempted. Done!")
driver.quit()
