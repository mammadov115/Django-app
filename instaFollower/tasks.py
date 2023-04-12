from celery import shared_task
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from .models import Account

@shared_task 
def update():

    accounts = Account.objects.all()
    for account in accounts:
        # Username and password
        USERNAME = account.login
        PASSWORD = account.password

        # Instagram-a daxil olmaq ucun driver-i baslat
        # driver = webdriver.Chrome()
        # driver.maximize_window()

        # Hide driver
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')

        driver = webdriver.Chrome(options=options)

        driver.get('https://www.instagram.com/accounts/login/')

        # Enter username and password
        time.sleep(5)
        username_input = driver.find_element(By.NAME,'username')
        username_input.send_keys(USERNAME)
        password_input = driver.find_element(By.NAME,'password')
        password_input.send_keys(PASSWORD)


        # Click login button
        time.sleep(2)
        login_button = driver.find_element(By.XPATH,"//button[@type='submit']")
        login_button.click()

        # Profile page
        time.sleep(15)
        profile_button = driver.find_element(By.XPATH,"//div[text()='Profile']")
        profile_button.click()

        # _ac8f

        # Get Follow data
        time.sleep(10)
        followers_s = driver.find_elements(By.XPATH,"//span[@class='_ac2a']")[1].text
        following_s = driver.find_elements(By.XPATH,"//span[@class='_ac2a']")[2].text

        # Get username
        user_name = driver.find_element(By.TAG_NAME,"h2").text

        # Close driver
        driver.quit()

        # update follow data
        account.followers=followers_s
        account.following=following_s
        account.save()