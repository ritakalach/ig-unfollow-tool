# Instagram Unfollow Tool
Automatically unfollow accounts that don't follow you back on Instagram with Selenium Python.

## Motivation
<img src="media/fluffy_geese.gif" align="right" width = 200>I have an Instagram account for my goose and duck photos 🦆. When another birder follows me, I feel that I must follow them back (supporting other birdwatchers and homesteaders feels like the polite thing to do). But some of these accounts are run by bots. They follow me, I follow them back, and then they unfollow me. It's not a huge problem, but I don't really like having a lengthy Instagram feed filled with content by users who don't interact with their followers. That's why I developed a tool to unfollow accounts that don't follow me back. As a result, I'm only following people who interact with my content and I interact with theirs. It makes me feel like I'm part of a little birdwatching community (yes, I know how dorky that sounds and my real-life friends tease me about it all the time).

## Running the code
You must have Python 3 and [Selenium](https://selenium-python.readthedocs.io) installed on your computer. I used Firefox as my chosen browser, which also requires geckodriver.

1) Download [ig_unfollow_tool.py](ig_unfollow_tool.py)
2) Update lines 189-190 with your account credentials 
3) Run ```python3 ig_unfollow_tool.py``` in the terminal

Here's what you'll see on screen as the code runs:

<img src="media/login_and_get_followers.gif" width = 500> 
<img src="media/unfollow.gif" width = 500> 

What you'll see in your terminal:

<img src="media/terminal.png" width = 500> 

(Of course, not all of the accounts unfollowed are run by bots. Regardless, I like having a smaller Instagram feed. I recommend creating an exception list for those accounts that you want to follow regardless of whether they follow you back.)
