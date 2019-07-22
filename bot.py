import sys
sys.path.append("instabot");

from instabot import Bot
from time import sleep
import random
from datetime import datetime
from twilio.rest import Client




accounts = [];
accCount = 0;
 #fill this out with a starting page
accounts.append("communist_conclusion");
accounts.append("soviet.shiba");



def follow(bot, followers, followCount, amt):

	lower = followCount;
	#upper = min(followCount + amt, len(followers));
	count = 0;
	actualCount = 0;
	#follow
	for user in followers[lower:]: 
		print("count", count);
		print("amt", amt);
		if count >= amt:
			return actualCount;
		username = bot.get_username_from_user_id(user);		
		#print("Attempting to follow:", username);
		if bot.follow(username):
			print("Followed! -", username);
			count += 1;
		else:
			print("Not Followed! -", username);
		actualCount += 1;
		
	return actualCount;

def unfollow(bot, amt):
	following = bot.get_user_following("");
	whitelist = bot.whitelist_file;
	following = list(set(following) - whitelist.set);


	i = 0;

	cap = min(100, len(following));
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
	return True;

def filter(bot, amt):
	following = bot.get_user_following("");
	whitelist = bot.whitelist_file;
	following = list(set(following) - whitelist.set);

	added = 0;

	for user in following[-amt:]: #file read is stored in reversed stack
		if bot.api.last_response.status_code == 400:
			sys.exit();
		username = bot.get_username_from_user_id(user);
		user_info = bot.get_user_info(user)
		bio = user_info['biography'];
		username = user_info['username'];
		name = user_info['full_name'];
		followers = user_info['follower_count'];
		following = user_info['following_count'];
		if "meme" in bio.lower() or "meme" in name.lower() or "meme" in username.lower():
			if followers > 2500 and followers < 10000:
				if following/followers < 4:
					accounts.append(username);
					print("Added: ", username);
					added += 1;
		if added >= 3:
			return;
		sleep(round(random.uniform(4,7), 2));

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


for acc in accounts:

	followers = bot.get_user_followers(acc);

	skipped = bot.skipped_file;
	followed = bot.followed_file;
	unfollowed = bot.unfollowed_file;

	followers = list(set(followers) - skipped.set - followed.set - unfollowed.set);
	followCount = 0;

	printUpdate("Starting Running")

	while followCount < len(followers):


		startTime = printUpdate("Starting Following")

		followCount += follow(bot, followers, followCount, amt);

		endTime = printUpdate("Ending Following")

		secElapsed = (endTime - startTime).total_seconds();
		if secElapsed < 3600:
			sleep(3600 - secElapsed);

		startTime = printUpdate("Starting UnFollowing")

		unfollow(bot,amt//3);

		endTime = printUpdate("Ending UnFollowing")

		secElapsed = (endTime - startTime).total_seconds();
		if secElapsed < 3600:
			sleep(3600 - secElapsed);

		#printUpdate("Starting Approve")
		#bot.approve_pending_follow_requests();
		#printUpdate("Ending Approve")
		
		sleep(300);

		if(len(accounts) - accCount < 2):
			startTime = printUpdate("Starting Filter");
			filter(bot, 400);
			endTime = printUpdate("Ending Filter");
			secElapsed = (endTime - startTime).total_seconds();
			if secElapsed < 3600:
				sleep(3600 - secElapsed);
					
	accCount += 1;


		
		 