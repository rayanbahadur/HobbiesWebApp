from django.test import TestCase

# Create your tests here.
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class UserTestsTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # cls.live_server_url = 'http://localhost:8000'
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()
        
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def signup(self):
        self.driver.get(f'{self.live_server_url}/signup/')
        self.driver.find_element(By.NAME, 'name').send_keys('Test User')
        self.driver.find_element(By.NAME, 'email').send_keys('testuser@example.com')
        self.driver.find_element(By.NAME, 'date_of_birth').send_keys('01-01-2000')
        self.driver.find_element(By.NAME, 'password1').send_keys('Str0ngP@ssw0rd!')
        self.driver.find_element(By.NAME, 'password2').send_keys('Str0ngP@ssw0rd!')
        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        submit_button.click()
        self.assertEqual(self.driver.current_url, f'{self.live_server_url}/')

    def login(self):
        self.driver.get(f'{self.live_server_url}/login/')
        self.driver.find_element(By.NAME, 'email').send_keys('testuser@example.com')
        self.driver.find_element(By.NAME, 'password').send_keys('Str0ngP@ssw0rd!')
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        print("Current URL:", self.driver.current_url)
        print("Page Source:", self.driver.page_source)
        print("Cookies:", self.driver.get_cookies())
        print("self.live_server_url:", self.live_server_url)
        self.assertEqual(self.driver.current_url, f'{self.live_server_url}/')

    def test_01_signup(self):
        self.signup()

    def test_02_login(self):
        self.signup()  # Ensure the user is signed up before logging in
        self.login()

    # def test_03_edit_profile(self):
    #     self.signup()  # Ensure the user is signed up before logging in
    #     self.login()  # Ensure the user is logged in before editing profile
    #     self.driver.get(f'{self.live_server_url}/profilepage/')
    #     print("Current URL:", self.driver.current_url)
    #     print("Page Source:", self.driver.page_source)
        
    #     # Wait for the Vue.js component to be present
    #     WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located((By.ID, 'name'))
    #     )
        
    #     name_field = self.driver.find_element(By.ID, 'name')
    #     name_field.clear()
    #     name_field.send_keys('New Name')
    #     # Add more steps as needed