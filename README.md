# get_toonily_notifications



Get latest manhwa chapter email notifications from https://toonily.com using ezgmail module, could possibly work on other manga/manwha sites but some of those sites uses cloudfare protection and must use cfscrape module to get past that.
# Requirements
* Python >= 3.6

* ezgmail

* pyperclip

* A gmail account to send notifications

* An email account to receive manhwa chapter notifications from the gmail account
# Instructions
Follow the instructions in installing and setting up ezgmail from here:
https://github.com/asweigart/ezgmail

After you are done copy the directory path where your CLIENT CONFIGURATION files (credentials.json, token.json) are located to toonily.py at this line:

	path = "YOUR CLIENTCONFIG DIRECTORY PATH"
	
	os.chdir(path)
	
# Run script

Run the script like this:

	python toonily.py --manhwa "MANGA/MANHWA link" --chapter "chapter number" --email "your email address that receives the notification"
	
Example:

	python toonily.py --manhwa "https://toonily.com/webtoon/peerless-dad/" --chapter 100 --email "example@gmail.com"

	

Be sure the manga/manhwa name is properly typed else the script won't work.

The script will periodically check for the latest chapter that was inputted every 300 secs (5 minutes) and if it's updated it will send an email notification with the chapter link in it.

You can change how long it must wait before checking again by changing the time.sleep argument.

Be sure to periodically check the script output from console or from IDE, it might raise the is_ended function that says the manhwa already ended and if the chapter you entered is less than or equal to last chapter of the manhwa it will automatically copy the chapter link using copy method of pyperclip
