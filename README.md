# get_toonily_notifications



Get latest manhwa chapter email notifications from toonily.com using ezgmail
# Requirements
Python >= 3.6

ezgmail
# Instructions
Follow the instructions in installing and setting up ezgmail from here:
https://github.com/asweigart/ezgmail

After you are done copy the directory path where your clientconfig files are located to the toonily.py at line 11

	line 11 - path = "YOUR CLIENTCONFIG DIRECTORY PATH"
	
	line 12 - path = os.chdir(path)
	
# Run script

Run the script like this

	python toonily.py "MANGA/MANHWA name" "chapter number" "your email address that receives the notification"
	
Example

	python toonily.py "peerless dad" "111" "example@gmail.com"
	

Be sure the manga/manhwa name is properly typed else the script won't work
