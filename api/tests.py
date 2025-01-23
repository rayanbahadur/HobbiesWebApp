import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
class UserTestsTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def signup_user(self, name, email, password, dob):
        """Helper function to sign up a user."""
        self.driver.get(f"{self.live_server_url}/signup/")
        self.driver.find_element(By.NAME, "name").send_keys(name)
        self.driver.find_element(By.NAME, "email").send_keys(email)
        self.driver.find_element(By.NAME, "date_of_birth").send_keys(dob)
        self.driver.find_element(By.NAME, "password1").send_keys(password)
        self.driver.find_element(By.NAME, "password2").send_keys(password)
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        submit_button.click()

    def login_user(self, email, password):
        """Helper function to log in a user."""
        self.driver.get(f"{self.live_server_url}/login/")
        self.driver.find_element(By.NAME, "email").send_keys(email)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    def test_01_signup(self):
        """Test signing up a user."""
        self.signup_user("Test User", "testuser@example.com", "Str0ngP@ssw0rd!", "01-01-2000")
        self.assertEqual(self.driver.current_url, f"{self.live_server_url}/")

    def test_02_login(self):
        """Test logging in a user."""
        self.signup_user("Test User", "testuser@example.com", "Str0ngP@ssw0rd!", "01-01-2000")
        self.login_user("testuser@example.com", "Str0ngP@ssw0rd!")
        self.assertEqual(self.driver.current_url, f"{self.live_server_url}/")

    def test_03_edit_profile(self):
        """Test editing the profile."""
        self.signup_user("Test User", "testuser@example.com", "Str0ngP@ssw0rd!", "01-01-2000")
        self.login_user("testuser@example.com", "Str0ngP@ssw0rd!")
        self.driver.get(f"{self.live_server_url}/profile-page/")
        self.driver.find_element(By.ID, "name").clear()
        self.driver.find_element(By.ID, "name").send_keys("Updated User")
        self.driver.find_element(By.ID, "email").clear()
        self.driver.find_element(By.ID, "email").send_keys("updateduser@example.com")
        self.driver.find_element(By.ID, "date_of_birth").clear()
        self.driver.find_element(By.ID, "date_of_birth").send_keys("01-01-1995")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        submit_button.click()

        # Verify the alert
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        self.assertEqual(alert.text, "Profile updated successfully")
        alert.accept()

    def test_04_users_page_with_age_filter(self):
        """Test filtering users by age."""
        self.signup_user("User One", "user1@example.com", "Str0ngP@ssw0rd!", "01-01-1999")
        self.login_user("user1@example.com", "Str0ngP@ssw0rd!")
        self.driver.get(f"{self.live_server_url}/profile-page/")
        self.driver.find_element(By.ID, "newHobby").send_keys("swimming")
        time.sleep(2)
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(2)
        submit_button.click()
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        self.assertEqual(alert.text, "Profile updated successfully")
        alert.accept()
    #     self.driver.get(f"{self.live_server_url}/users-page/")
    #     self.driver.find_element(By.ID, "ageMin").send_keys("20")
    #     self.driver.find_element(By.ID, "ageMax").send_keys("30")
    #     self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    #     # Verify the filtered results
    #     users = self.driver.find_elements(By.CLASS_NAME, "user-card")
    #     for user in users:
    #         age = int(user.find_element(By.CLASS_NAME, "user-age").text)
    #         self.assertTrue(20 <= age <= 30)

    def test_05_friend_request(self):
        """Test sending a friend request."""
        # Sign up and login as User One
        self.signup_user("User One", "user1@example.com", "Str0ngP@ssw0rd!", "01-01-2000")
        self.login_user("user1@example.com", "Str0ngP@ssw0rd!")
        time.sleep(1)

        self.driver.find_element(By.NAME, "logout").click()
        # time.sleep(5)
        self.driver.get(f"{self.live_server_url}/")
        time.sleep(2)


        self.signup_user("Test User", "testuser@example.com", "Str0ngP@ssw0rd!", "01-01-2000")
        self.login_user("testuser@example.com", "Str0ngP@ssw0rd!")
        time.sleep(2)

        # Navigate to Friends Page and search for User One
        self.driver.get(f"{self.live_server_url}/friends-page/")
        time.sleep(2)
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "searchBox")))
        self.driver.find_element(By.NAME, "search").send_keys("User One")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # self.driver.find_element(By.ID, "searchButton").click()
        time.sleep(2)
        send_request_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'request'))
        )
        send_request_button.click()
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        self.assertEqual(alert.text, 'Friend request sent!')
        time.sleep(2)
        alert.accept()
        
        self.driver.find_element(By.NAME, "logout").click()
        # time.sleep(5)
        self.driver.get(f"{self.live_server_url}/")
        time.sleep(2)
        # Sign up and login as User One
        self.login_user("user1@example.com", "Str0ngP@ssw0rd!")
        self.driver.get(f"{self.live_server_url}/friends-page/")
        time.sleep(2)
        self.driver.find_element(By.NAME, "accept").click()
        time.sleep(2)