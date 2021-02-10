from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class MANAGER:
	def open_web(self):
		chrome_options = Options()
		"""chrome_options.add_argument('--headless')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--disable-dev-shm-usage')"""
		self.web = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

	def load_cookies(self):
		self.web.get("https://discord.com/")
		for c in self.cookies:
			self.web.add_cookie(c)

	def save_cookies(self):
		self.cookies = self.web.get_cookies()

	def load_account(self):
		if not self.logged:
			self.login()
			self.profile_info["discord"]["logged"] = False
		else:
			self.load_cookies()
			self.web.get("https://discord.com/channels/@me")
		sleep(2)
		self.save_cookies()

		return self.profile_info, self.cookies







	def get_inner(self, element, selector):
		try:
			return element.find_element_by_css_selector(selector).get_attribute('innerHTML')
		except Exception as e:
			print(e, element, selector)

			return False

	def get_message_from_element(self, element):
		return self.get_inner(element, self.chat_message_content_css_selector)

	def get_messages_elements(self):
		return self.web.find_elements_by_css_selector(self.chat_message_css_selector)

	def new_messages_label(self):
		if len(self.web.find_elements_by_css_selector(self.chat_new_messages_div_css_select)) > 2:
			return True
		else:
			return False

	def get_name_of_current_chat(self):
		return self.get_inner(self.web, self.current_chat_name_css_selector)


	def get_name_of_chat_element(self, element):
		return self.get_inner(element, self.chat_name_css_selector)


	def get_name_of_chat_message_element(self, element):
		return self.get_inner(element, self.message_chat_username_css_selector)




	def check_remembered(self):
		chat = self.get_name_of_current_chat()
		last = self.get_last_message_element()
		sender = self.get_name_of_chat_message_element(last)

		remembered = False

		try:
			log = self.log[chat]
		except:
			self.remember(last, chat, sender)
			return False
		else:
			if log == [sender, self.get_message_from_element(last)]:
				return True
			else:
				self.remember(last, chat, sender)
				return False

	def remember(self, last=False, chat=False, sender=False):
		if not last:
			last = self.get_last_message_element()
		if not sender:
			sender = self.get_name_of_chat_message_element(last)
		if not chat:
			chat = self.get_name_of_current_chat()
		print("Remember: ", last, chat, sender, "\n")
		self.log[chat] = [sender, self.get_message_from_element(last)]











	def send_message(self, message):
		now = self.get_messages_elements()
		try:
			input_ = self.web.find_element_by_xpath(self.chat_input)
			input_.send_keys(message)
			input_.send_keys(Keys.ENTER)
		except:
			return False
		else:
			self.remember()		
			while not self.changed(now):
				sleep(0.1)
			sleep(2)
			return True
































	def go_to_chat(self, chat_name):
		for c in self.get_chats_elements():
			if self.get_name_of_chat_element(c) == chat_name:
				c.click()
				return True
		return False





















	def get_messages(self):
		messages = []
		for c in self.get_messages_elements():
			messages.append(self.get_message_from_element(c))
		return messages



	def changed(self, messages):
		now = self.get_messages_elements()
		if not now == messages:
			return True
		else:
			return False





	def get_last_message_element(self):
		messages = self.get_messages_elements()
		try:
			last_element = messages[len(messages)-1]
		except:
			return False
		else:
			return last_element

	def get_last_message(self):
		element = self.get_last_message_element()
		if element:
			return self.get_message_from_element(element)
		else:
			return False




	def input_chat(self, message=False):
		if message:
			self.send_message(message)
		reply = False
		while not reply:
			print(reply)
			reply = self.get_new_message()
			sleep(0.01)
		return reply



	def get_new_message(self):
		if not self.check_remembered():
			return self.get_last_message()
		else:
			return False





















	def get_chats_elements(self):
		chats = []
		for c in self.web.find_elements_by_css_selector(self.chat_container_css_selector):
			if not self.get_name_of_chat_element(c) in self.trash_chats:
				chats.append(c)
		return chats

	def get_chat_names(self):
		names = []
		for c in self.get_chats_elements():
			names.append(self.get_name_of_chat_element(c))
		return names

	def login(self):
		self.web.get("https://discord.com/login")
		email_input = self.web.find_element_by_xpath('//*[@id="app-mount"]/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[1]/div/div[2]/input')
		password_input = self.web.find_element_by_xpath('//*[@id="app-mount"]/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[2]/div/input')
		submit_input = self.web.find_element_by_xpath('//*[@id="app-mount"]/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/button[2]')
		email_input.send_keys(self.email)
		password_input.send_keys(self.password)
		submit_input.click()

	def load_elements_keys(self, keys):
		self.chat_container_css_selector = keys["chat_container_css_selector"]

		self.chat_name_css_selector = keys["chat_name_css_selector"]

		self.current_chat_name_css_selector = keys["current_chat_name_css_selector"]

		self.chat_new_messages_div_css_select = keys["chat_new_messages_div_css_select"]

		self.chat_message_css_selector = keys["chat_message_css_selector"]

		self.chat_message_content_css_selector = keys["chat_message_content_css_selector"]

		self.chat_container_xpath = keys["chat_container_xpath"]

		self.chat_input = keys["chat_input"]

		self.message_chat_username_css_selector = keys["message_chat_username_css_selector"]


	def __init__(self, profile_info, cookies, keys):
		self.profile_info = profile_info
		self.logged = self.profile_info["discord"]["logged"]
		self.cookies = cookies
		self.email = self.profile_info["discord"]["email"]
		self.password = self.profile_info["discord"]["password"]
		self.web = False
		self.messages_sent = []
		self.keys = keys
		self.log = {}

		self.trash_chats = ["Nitro", "Friends", False]

		self.load_elements_keys(self.keys)