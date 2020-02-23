# get_toonily_notifications



Get latest manhwa chapter email notifications from toonily.com using ezgmail
# Requirements
* Python >= 3.6

* ezgmail

* A gmail account to send notifications

* An email account to receive manhwa chapter notifications from the gmail account
# Instructions
Follow the instructions in installing and setting up ezgmail from here:
https://github.com/asweigart/ezgmail

After you are done copy the directory path where your CLIENT CONFIGURATION files (credentials.json, token.json) are located to the toonily.py at line 11

	line 10 - path = "YOUR CLIENTCONFIG DIRECTORY PATH"
	
	line 11 - os.chdir(path)
	
# Run script

Run the script like this

	python toonily.py --manhwa "MANGA/MANHWA name" --chapter "chapter number" --email "your email address that receives the notification"
	
Example

	python toonily.py --manhwa "peerless dad" --chapter 100 --email "example@gmail.com"

	

Be sure the manga/manhwa name is properly typed else the script won't work

The script will periodically check for the latest chapter that was inputted every 300 secs (5 minutes)
