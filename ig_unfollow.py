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

	def unfollow(self, username):
		# Go to your Instagram profile page
		self.browser.get("https://www.instagram.com/{}/".format(username))
		sleep(5)

		# Get the usernames of all your followers
		followers = self.get_followers()
		sleep(5)

		# Unfollow accounts that aren't following you
		num_of_accounts_unfollowed, accounts_unfollowed = self.compare_followers_to_following(followers)
		print("You've unfollowed {} accounts.".format(num_of_accounts_unfollowed))
		sleep(5)
		
		# Close browser
		self.browser.quit()

		# Store the usernames of accounts you've unfollowed 
		new_file = open('accounts_unfollowed.txt', 'w')
		for account_unfollowed in accounts_unfollowed:
			new_file.write(account_unfollowed)
		new_file.close()

		return

	def get_followers(self):
		# Get number of followers
		num_of_followers = self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span").text

		# Click on the "followers" button
		# this will open a popup window that lists followers
		followers_button = self.browser.find_element_by_partial_link_text("followers")
		followers_button.click()
		sleep(5)

		# Scroll to load entire list of followers
		scroll_count = 0
		while scroll_count < 2: #int(num_of_followers) // 2: 
			scroll_box = self.browser.find_element_by_xpath("//div[@role='dialog']//a")
			scroll_box.send_keys(Keys.PAGE_DOWN)
			scroll_count += 1
			sleep(1)
		print("Done scrolling through followers.")

		# Get the usernames of all followers
		followers = set()
		#for i in range(1, num_of_followers + 1):
		for i in range(3, 0, -1):
			follower = self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/ul/div/li[{}]/div/div[1]/div[2]/div[1]/span/a".format(i))
			followers.add(follower.get_attribute("title"))
		sleep(1)
		
		# Close popup window
		close_popup_button = self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button")
		close_popup_button.click() 

		return followers

	def compare_followers_to_following(self, followers):
		# Get number of accounts you were following prior to unfollowing those that don't follow you back
		num_following_before = self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span").text

		# Click on the "following" button
		# this will open a popup window that lists accounts you're following
		following_button = self.browser.find_element_by_partial_link_text("following")
		following_button.click()
		sleep(5)

		# Scroll to load entire list of users you're following 
		scroll_count = 0
		while scroll_count < 4: #int(num_of_followers) // 2: 
			scroll_box = self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]")
			scroll_box.send_keys(Keys.PAGE_DOWN)
			scroll_count += 1
			sleep(1)
		print("Done scrolling through following.")

		# Unfollow accounts who don't follow you back
		#for i in range(1, int(num_of_followers) + 1):
		accounts_unfollowed = set()
		for i in range(1, 0, -1): 
			following = self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/ul/div/li[{}]/div/div[1]/div[2]/div[1]/span/a".format(i))
			following_username = following.get_attribute("title")	
			print(i, following_username)	
			if following_username not in followers:
				following_user_button = self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/ul/div/li[{}]/div/div[2]/button".format(i))
				following_user_button.click()
				sleep(1)
				unfollow_user_button = self.browser.find_element_by_xpath("/html/body/div[6]/div/div/div/div[3]/button[1]")
				unfollow_user_button.click()
				sleep(1)
				accounts_unfollowed.add(following_username)
		sleep(1)

		# Close popup window
		close_popup_button = self.browser.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button")
		close_popup_button.click() 
		sleep(1)

		# Get number of accounts you are following now
		num_following_after = self.browser.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span").text

		# Return the number of people you've unfollowed and their usernames
		num_of_accounts_unfollowed = int(num_following_before) - int(num_following_after)
		return num_of_accounts_unfollowed, accounts_unfollowed

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
