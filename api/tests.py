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

    def test_01_signup(self):
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
        
    def test_02_login(self):
        self.test_01_signup()
        self.driver.get(f'{self.live_server_url}/login/')
        self.driver.find_element(By.NAME, 'email').send_keys('testuser@example.com')
        self.driver.find_element(By.NAME, 'password').send_keys('Str0ngP@ssw0rd!')
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.assertEqual(self.driver.current_url, f'{self.live_server_url}/')
        # time.sleep(5)

    # def test_03_edit_profile(self):
    #     self.driver.get(f'{self.live_server_url}/profile/')
    #     self.driver.find_element(By.ID, 'name').clear()
    #     self.driver.find_element(By.ID, 'name').send_keys('Updated User One')
    #     self.driver.find_element(By.ID, 'email').clear()
    #     self.driver.find_element(By.ID, 'email').send_keys('updateduser1@example.com')
    #     self.driver.find_element(By.ID, 'date_of_birth').clear()
    #     self.driver.find_element(By.ID, 'date_of_birth').send_keys('01-01-1999')
    #     self.driver.find_element(By.ID, 'newPassword1').send_keys('newStr0ngP@ssw0rd!')
    #     self.driver.find_element(By.ID, 'newPassword2').send_keys('newStr0ngP@ssw0rd!')
    #     submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    #     self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    #     submit_button.click()
    #     # Handle and verify alert
    #     WebDriverWait(self.driver, 10).until(EC.alert_is_present())
    #     alert = self.driver.switch_to.alert
    #     self.assertEqual(alert.text, 'Profile updated successfully')
    #     alert.accept()

    #     # Verify the page reloads to the profile page
    #     self.assertEqual(self.driver.current_url, f'{self.live_server_url}/profile/')

    # def test_users_page_with_age_filter(self):
    #     self.test_login()
    #     self.driver.get(f'{self.live_server_url}/similar/')
    #     self.driver.find_element(By.ID, 'ageMin').send_keys('10')
    #     self.driver.find_element(By.ID, 'ageMax').send_keys('30')
    #     self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    #     users = self.driver.find_elements(By.CLASS_NAME, 'user-card')  # Ensure 'user-card' is in the frontend
    #     for user in users:
    #         age = int(user.find_element(By.CLASS_NAME, 'user-age').text)
    #         self.assertTrue(10 <= age <= 30)

    # def test_05_send_friend_request(self):
    #     # self.test_02_login()
    #     self.driver.get(f'{self.live_server_url}/friends/')
    #     self.driver.find_element(By.NAME, 'search').send_keys('r')
    #     self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    #     send_request_button = WebDriverWait(self.driver, 10).until(
    #         EC.element_to_be_clickable((By.NAME, 'request'))
    #     )
    #     send_request_button.click()
    #     WebDriverWait(self.driver, 10).until(EC.alert_is_present())
    #     alert = self.driver.switch_to.alert
    #     self.assertEqual(alert.text, 'Friend request sent!')
    #     time.sleep(5)




    # # def test_send_friend_request(self):
    # #     self.driver.get(f'{self.live_server_url}/friends/')

    # #     # Wait for the search box to be visible and enter the query

    # #     # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'searchBox')))
    # #     self.driver.find_element(By.NAME, 'search').send_keys('rahul')
    # #     time.sleep(5)
    # #     # Wait for the search button to be clickable and click it
    # #     WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.search-btn')))
    # #     self.driver.find_element(By.CSS_SELECTOR, 'button.search-btn').click()

    # #     # Wait for the send request button to be visible
    # #     WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.send-request-btn')))
    # #     send_request_button = self.driver.find_element(By.CSS_SELECTOR, 'button.send-request-btn')

    # #     # Ensure the send request button is clickable
    # #     WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.send-request-btn')))
    # #     send_request_button.click()

    # #     # Handle and verify the alert (if applicable)
    # #     try:
    # #         WebDriverWait(self.driver, 10).until(EC.alert_is_present())
    # #         alert = self.driver.switch_to.alert
    # #         self.assertEqual(alert.text, 'Friend request sent!')
    # #         alert.accept()
    # #     except:
    # #         # If no alert, verify success message in DOM
    # #         confirmation_message = WebDriverWait(self.driver, 10).until(
    # #             EC.presence_of_element_located((By.CSS_SELECTOR, '.success-message'))
    # #         )
    # #         self.assertEqual(confirmation_message.text, 'Friend request sent!')


    # # def test_accept_friend_request(self):
    # #     # Login as User 2
    # #     self.driver.get(f'{self.live_server_url}/login/')
    # #     self.driver.find_element(By.NAME, 'email').send_keys('user2@example.com')
    # #     self.driver.find_element(By.NAME, 'password').send_keys('Str0ngP@ssw0rd!')
    # #     self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # #     # Accept Friend Request
    # #     self.driver.get(f'{self.live_server_url}/friend-requests/')
    # #     self.driver.find_element(By.CSS_SELECTOR, 'button.btn-accept-request').click()  # Update selector to match your frontend
    # #     alert = Alert(self.driver)
    # #     self.assertEqual(alert.text, 'Friend request accepted!')
    # #     alert.accept()

    # #     # Verify Friendship
    # #     self.driver.get(f'{self.live_server_url}/friends/')
    # #     self.assertIn('User One', self.driver.page_source)
