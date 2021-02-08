from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pickle

class MANAGER:
	def open_web(self):
		chrome_options = Options()
		"""chrome_options.add_argument('--headless')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--disable-dev-shm-usage')"""
		self.web = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

	def load_cookies(self):
		for c in self.cookies:
			self.web.add_cookie(c)

	def save_cookies(self):
		self.cookies = self.web.get_cookies()
		self.profile_info["cookies"] = pickle.dumps(self.cookies)

	def login(self):
		self.web.get("https://discord.com/login")
		email_input = self.web.find_element_by_xpath('//*[@id="app-mount"]/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[1]/div/div[2]/input')
		password_input = self.web.find_element_by_xpath('//*[@id="app-mount"]/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[2]/div/input')
		submit_input = self.web.find_element_by_xpath('//*[@id="app-mount"]/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/button[2]')
		email_input.send_keys(self.email)
		password_input.send_keys(self.password)
		submit_input.click()

	def __init__(self, profile_info):
		self.profile_info = profile_info
		self.cookies = pickle.loads(self.profile_info["cookies"])
		self.email = self.profile_info["email"]
		self.password = self.profile_info["password"]
		self.web = False
