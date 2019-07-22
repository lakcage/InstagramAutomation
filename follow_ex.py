import sys
sys.path.append("instabot");

from instabot import Bot

bot = Bot(filter_users = False, max_following_to_followers_ratio = 100, max_followers_to_following_ratio = 100, follow_delay = 5);
#this overrides the initial bot parameters bc we dont want any restrictions on it yet

bot.login(username = "", password = "");

followers = bot.get_user_followers("");

i = 0;
for user in followers[0:]: 
	username = bot.get_username_from_user_id(user);
	print("Attempting to follow:", username);
	if bot.follow(username):
		i += 1;
		print("Followed! -", username);
	else:
		print("Not Followed! -", username);
	if i > 50:
		break;