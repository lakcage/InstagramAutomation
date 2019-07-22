import sys
sys.path.append("instabot");

from instabot import Bot
from time import sleep
import random
from datetime import datetime
from twilio.rest import Client


account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)

def unfollow(bot, amt, following):
	
	i = 0;

	cap = min(0, len(following));
	for user in following[:-cap]: #get_user_following stored in reverse stack
		if bot.api.last_response.status_code == 400:
			sys.exit();
		username = bot.get_username_from_user_id(user);
		print("Attempting to unfollow:", username);
		if bot.unfollow(username):
			i += 1;
			print("Unfollowed -", username);
		else:
			print("Failed to unfollow -", username);
		if(i >= amt):
			break;
	return i;



def printUpdate(task):
	currTime = datetime.now();
	timeString = currTime.strftime("%Y-%m-%d %H:%M")
	print(task + ": " + timeString);
	with open("times.txt", "a+") as times: 
		times.write(task + ": " + timeString  + "\r\n");

	message = client.messages \
	    .create(
	         body= task + ": " + timeString,
	         from_='+18577634660',
	         to='+'
	     )

	return currTime;

bot = Bot(filter_users = True, follow_delay = 47, unfollow_delay = 47, max_follows_per_day = 3840, max_unfollows_per_day = 3840);

bot.login(username = "", password = "");

amt = 145;
delay = 600;



followCount = 0;
printUpdate("Starting Running")
following = bot.get_user_following("");
whitelist = bot.whitelist_file;
following = list(set(following) - whitelist.set);

while len(following) > 100:

	startTime = printUpdate("Starting UnFollowing")


	cap = min(0, len(following));
	i = 0;

	following = bot.get_user_following("");
	whitelist = bot.whitelist_file;
	following = list(set(following) - whitelist.set);
	for user in following:
		if bot.api.last_response.status_code == 400:
			sys.exit();
		username = bot.get_username_from_user_id(user);
		print("Attempting to unfollow:", username);
		if bot.unfollow(username):
			i += 1;
			print("Unfollowed -", username);
		else:
			print("Failed to unfollow -", username);
		if(i >= amt):
			break;

	endTime = printUpdate("Ending UnFollowing")

	secElapsed = (endTime - startTime).total_seconds();
	if secElapsed < 3600:
		sleep(3600 - secElapsed);




		
		 