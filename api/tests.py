from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.auth import get_user_model

User = get_user_model()
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

class UserTestsTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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

    def test_signup(self):
        self.driver.get(f'{self.live_server_url}/signup/')
        self.driver.find_element(By.NAME, 'name').send_keys('Test User')
        self.driver.find_element(By.NAME, 'email').send_keys('testuser@example.com')
        self.driver.find_element(By.NAME, 'date_of_birth').send_keys('2000-01-01')
        self.driver.find_element(By.NAME, 'password1').send_keys('Str0ngP@ssw0rd!')
        self.driver.find_element(By.NAME, 'password2').send_keys('Str0ngP@ssw0rd!')
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.assertEqual(self.driver.current_url, f'{self.live_server_url}/')

    def test_login(self):
        self.driver.get(f'{self.live_server_url}/login/')
        self.driver.find_element(By.NAME, 'email').send_keys('user1@example.com')
        self.driver.find_element(By.NAME, 'password').send_keys('Str0ngP@ssw0rd!')
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        self.assertEqual(self.driver.current_url, f'{self.live_server_url}/')

    def test_edit_profile(self):
        self.test_login()
        self.driver.get(f'{self.live_server_url}/profile/')
        self.driver.find_element(By.ID, 'name').clear()
        self.driver.find_element(By.ID, 'name').send_keys('Updated User One')
        self.driver.find_element(By.ID, 'email').clear()
        self.driver.find_element(By.ID, 'email').send_keys('updateduser1@example.com')
        self.driver.find_element(By.ID, 'date_of_birth').clear()
        self.driver.find_element(By.ID, 'date_of_birth').send_keys('1999-01-01')
        self.driver.find_element(By.ID, 'newPassword1').send_keys('newStr0ngP@ssw0rd!')
        self.driver.find_element(By.ID, 'newPassword2').send_keys('newStr0ngP@ssw0rd!')
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        alert = Alert(self.driver)
        self.assertEqual(alert.text, 'Profile updated successfully')
        alert.accept()

        # Verify the page reload
        self.assertEqual(self.driver.current_url, f'{self.live_server_url}/profile/')

    # def test_users_page_with_age_filter(self):
    #     self.test_login()
    #     self.driver.get(f'{self.live_server_url}/')
    #     self.driver.find_element(By.ID, 'ageMin').send_keys('10')
    #     self.driver.find_element(By.ID, 'ageMax').send_keys('30')
    #     self.driver.find_element(By.CSS_SELECTOR, 'button.btn-primary').click()
    #     self.assertIn('Users with Similar Hobbies', self.driver.page_source)