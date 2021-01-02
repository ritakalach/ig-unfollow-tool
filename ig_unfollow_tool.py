from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class InstaBot:
	def __init__(self, username, password):
		# Open Firefox
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(5)

		# Login in to Instagram
		home_page = HomePage(self.browser)
		home_page.login(username, password)

		self.username = username

	def unfollow(self):
		# Go to your Instagram profile page
		self.browser.get("https://www.instagram.com/{}/".format(self.username))
		sleep(5)

		# Get the usernames of all your followers
		followers, num_of_followers = self.get_followers()
		
		# Check to make sure that approximately all followers were scraped
		# (I say approximately because I've noticed I always have a few less followers than stated on Instagram)
		if len(followers) < num_of_followers * 0.99:
			print("There's been an error while scraping the usernames of your followers.")
			return

		# Unfollow accounts that aren't following you
		num_of_accounts_unfollowed, accounts_unfollowed = self.compare_to_following_and_unfollow(followers)
		# The number of accounts unfollowed is rounded if you have lots of followers
		# E.g., if you have 20,426 followers, Instagram will say you have 20.4K followers
		# and that's why the calculation will be rounded as well
		print("You've unfollowed {} accounts.".format(num_of_accounts_unfollowed))
		sleep(5)
		
		# Close browser
		self.browser.quit()

		# Store the usernames of accounts you've unfollowed 
		new_file = open('accounts_unfollowed.txt', 'w')
		for account_unfollowed in accounts_unfollowed:
			new_file.write(account_unfollowed + "\n")
		new_file.close()

		return

	def scroll(self, popup_window):
		js_command = """
					popup_window = document.querySelector('.isgrP');
					popup_window.scrollTo(0, popup_window.scrollHeight);
					var curr_page_len = popup_window.scrollHeight;
					return curr_page_len;
					"""
		curr_page_len = self.browser.execute_script(js_command)
		scrolling = True
		sleep(1)
		while scrolling:
			prev_page_len = curr_page_len
			curr_page_len = self.browser.execute_script(js_command)
			if prev_page_len == curr_page_len:
				scrolling = False
			sleep(1)

	def convert_str_to_num(self, num_as_str):
		num_map = {'K':1000, 'M':1000000, 'B':1000000000}
		num_as_str = num_as_str.replace(",", "")

		last_ch = num_as_str[-1]
		if last_ch in num_map:
			num_as_int = float(num_as_str[:-1])
			num_as_int *= num_map[last_ch]
			num_as_int = int(num_as_int)
		else:
			num_as_int = int(num_as_str)

		return num_as_int

	def get_followers(self):
		# Get number of followers
		num_of_followers = self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span").text
		num_of_followers = self.convert_str_to_num(num_of_followers)

		followers_button = self.browser.find_element_by_partial_link_text("followers")
		followers_button.click()
		sleep(5)

		# Scroll to load entire list of followers
		self.scroll(followers_button)
		print("Done scrolling through followers.")

		# Get the usernames of all followers
		usernames_of_followers = set()
		followers = self.browser.find_elements_by_css_selector('.FPmhX.notranslate')
		for follower in followers:
			usernames_of_followers.add(follower.text)

		# Close popup window
		close_popup_button = self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button")
		close_popup_button.click() 

		return usernames_of_followers, num_of_followers

	def compare_to_following_and_unfollow(self, followers):
		# Compare followers and following
		# Unfollow accounts that don't follow you back

		# Get number of accounts you are following (before unfollowing those that don't follow you back)
		num_following_before = self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span").text
		num_following_before = self.convert_str_to_num(num_following_before)

		# Click on the "following" button
		# this will open a popup window that lists accounts you're following
		following_button = self.browser.find_element_by_partial_link_text("following")
		following_button.click()
		sleep(5)

		# Scroll to load entire list of users you're following 
		self.scroll(following_button)
		print("Done scrolling through following.")

		# Unfollow accounts that don't follow you back
		accounts_unfollowed = self.unfollow_helper(followers, num_following_before)

		# Close popup window
		close_popup_button = self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button")
		close_popup_button.click() 
		sleep(1)

		# Get number of accounts you are following now (after ufollowing those that don't follow you back)
		num_following_after = self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span").text
		num_following_after = self.convert_str_to_num(num_following_after)

		# Return the number of people you've unfollowed and their usernames
		num_of_accounts_unfollowed = num_following_before - num_following_after
		return num_of_accounts_unfollowed, accounts_unfollowed

	def unfollow_helper(self, followers, num_following_before):
		accounts_unfollowed = set()

		for i in range(int(num_following_before), 0, -1):
			following = self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/ul/div/li[{}]/div/div[1]/div[2]/div[1]/span/a".format(i))
			following_username = following.get_attribute("title")		
			if following_username not in followers:
				# Unfollow account
				following_user_button = self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/ul/div/li[{}]/div/div[2]/button".format(i))
				following_user_button.click()
				sleep(1)
				unfollow_user_button = self.browser.find_element_by_xpath("/html/body/div[6]/div/div/div/div[3]/button[1]")
				self.browser.execute_script("arguments[0].click();", unfollow_user_button)
				sleep(1)
				accounts_unfollowed.add(following_username)
				print("You've unfollowed {}.".format(following_username))

		return accounts_unfollowed

class HomePage:
    def __init__(self, browser):
        self.browser = browser
        self.browser.get("https://www.instagram.com/")

    def login(self, username, password):
    	# Find the username and password inputs
        username_input = self.browser.find_element_by_css_selector("input[name='username']")
        password_input = self.browser.find_element_by_css_selector("input[name='password']")

        # Type your username and password in their respective inputs
        username_input.send_keys(username)
        password_input.send_keys(password)

        # Submit credentials and wait for page to load
        login_button = self.browser.find_element_by_xpath("//button[@type='submit']")
        login_button.click()
        sleep(5)

# Credentials to access Instagram account
username = ""
password = ""

my_insta_bot = InstaBot(username, password)
my_insta_bot.unfollow(username)
