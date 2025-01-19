import subprocess
import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.auth import get_user_model

User = get_user_model()
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

class UserTestsTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        
        # Start the backend server
        cls.backend_process = subprocess.Popen(['python', 'manage.py', 'runserver', '127.0.0.1:8000'], cwd='./')
        time.sleep(5)  # Wait for the backend server to start

        cls.live_server_url = 'http://localhost:5173'

        # Start the frontend server
        try:
            cls.frontend_process = subprocess.Popen(['npm', 'run', 'dev'], cwd='../frontend') ## Path seems to be wrong but I'm not sure why
            time.sleep(10)  # Wait for the frontend server to start
        except FileNotFoundError as e:
            print(f"Error starting frontend server: {e}")
            cls.frontend_process = None

        # Set the live server URL to the frontend server
        cls.live_server_url = 'http://localhost:5173'

        try:
            cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            cls.driver.implicitly_wait(10)
        except Exception as e:
            print(f"Error setting up WebDriver: {e}")
            cls.driver = None

    @classmethod
    def tearDownClass(cls):
        if cls.driver:
            cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        self.user1 = User.objects.create_user(email='user1@example.com', password='Str0ngP@ssw0rd!', name='User One', date_of_birth='2000-01-01')
        self.user2 = User.objects.create_user(email='user2@example.com', password='Str0ngP@ssw0rd!', name='User Two', date_of_birth='2000-01-01')

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
        self.driver.get(f'{self.live_server_url}/login/')
        self.driver.find_element(By.NAME, 'email').send_keys('testuser@example.com')
        self.driver.find_element(By.NAME, 'password').send_keys('Str0ngP@ssw0rd!')
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.assertEqual(self.driver.current_url, f'{self.live_server_url}/')

    def test_03_edit_profile(self):
        self.driver.get(f'{self.live_server_url}/profile/')
        self.driver.find_element(By.ID, 'name').clear()
        self.driver.find_element(By.ID, 'name').send_keys('Updated User One')
        self.driver.find_element(By.ID, 'email').clear()
        self.driver.find_element(By.ID, 'email').send_keys('updateduser1@example.com')
        self.driver.find_element(By.ID, 'date_of_birth').clear()
        self.driver.find_element(By.ID, 'date_of_birth').send_keys('01-01-1999')
        self.driver.find_element(By.ID, 'newPassword1').send_keys('newStr0ngP@ssw0rd!')
        self.driver.find_element(By.ID, 'newPassword2').send_keys('newStr0ngP@ssw0rd!')
        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        submit_button.click()
        # Handle and verify alert
        WebDriverWait(self.driver, 10).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        self.assertEqual(alert.text, 'Profile updated successfully')
        alert.accept()

        # Verify the page reloads to the profile page
        self.assertEqual(self.driver.current_url, f'{self.live_server_url}/profile/')

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


    # def test_send_friend_request(self):
    #     self.test_login()
    #     self.driver.get(f'{self.live_server_url}/search/')
    #     self.driver.find_element(By.ID, 'searchBox').send_keys('User Two')
    #     self.driver.find_element(By.CSS_SELECTOR, 'button.search-btn').click()
    #     self.driver.find_element(By.CSS_SELECTOR, 'button.send-request-btn').click()
    #     alert = Alert(self.driver)
    #     self.assertEqual(alert.text, 'Friend request sent!')
    #     alert.accept()
    # def test_accept_friend_request(self):
    #     # Login as User 2
    #     self.driver.get(f'{self.live_server_url}/login/')
    #     self.driver.find_element(By.NAME, 'email').send_keys('user2@example.com')
    #     self.driver.find_element(By.NAME, 'password').send_keys('Str0ngP@ssw0rd!')
    #     self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    #     # Accept Friend Request
    #     self.driver.get(f'{self.live_server_url}/friend-requests/')
    #     self.driver.find_element(By.CSS_SELECTOR, 'button.btn-accept-request').click()  # Update selector to match your frontend
    #     alert = Alert(self.driver)
    #     self.assertEqual(alert.text, 'Friend request accepted!')
    #     alert.accept()

    #     # Verify Friendship
    #     self.driver.get(f'{self.live_server_url}/friends/')
    #     self.assertIn('User One', self.driver.page_source)
