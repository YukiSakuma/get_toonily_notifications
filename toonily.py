"""Get email notifications of latest chapter of a manhwa/manga from toonily.com
 using ezgmail module"""
import ctypes
import datetime
import os
import re
import time
import requests
import ezgmail
import pyperclip


# pylint: disable=no-else-break

class EndedManhwa(Exception):
    "Manhwa ended already exception"


class ValidManhwa(Exception):
    """Manhwa is not valid exception"""


def main(link, chapter):
    """Main link chapter check"""
    try:
        req = requests.get(link, stream=True)
    except requests.exceptions.RequestException:
        return "Error trying again in 300 sec"
    try:
        if chapter in req.text:
            # print(r.text)
            return True
        return False
    except requests.exceptions.ChunkedEncodingError:
        return False


def send_email(my_email, subject, body):
    """send email notification"""
    while 1:
        date_email = datetime.datetime.now().strftime("%b-%d-%Y %I:%M:%S %p")
        try:
            ezgmail.send(my_email, subject, body)
            print(f'Success sending email {date_email}')
            return
        except ezgmail.EZGmailException:
            print(f"Error Trying again in 10 sec, {date_email}")
        time.sleep(10)


def check_valid(link):
    """check if manhwa is valid on toonily site"""
    check_status = requests.get(link, stream=True)
    if check_status.ok:
        return
    raise ValidManhwa(f"Not valid manhwa/manga link, make sure the manhwa url is valid\n",
                      f"{link}")


def is_ended(link, num):
    """check if manwha already ended"""
    check_end = re.compile(r"Chapter \d* - The End")
    try:
        req = requests.get(link, stream=True).text
    except requests.exceptions.RequestException:
        return
    result = check_end.search(req)
    if result:
        print(f"Manhwa homepage: {link}\n")
        result = result.group()
        req = result.split()
        num_end = req[1]
        if int(num) <= int(num_end):
            ch_link = f"{link}chapter-{num}"
            print("The link of the chapter number you entered below is copied\n")
            print(ch_link)
            ctypes.windll.user32.MessageBoxW(0, f"{ch_link}\nClose this window to finish copying",
                                             f" the link",
                                             f"Copying Chapter {num}", 0)
            pyperclip.copy(ch_link)
        else:
            print(f"Invalid chapter {num}")
            link = f"{link}chapter-{num_end}"
            ctypes.windll.user32.MessageBoxW(0, f"Invalid chapter {num}, manhwa already ended ",
                                             f"at chapter {num_end}\n",
                                             f"{link}\nClose this window to finish ",
                                             f"copying the link",
                                             f"Copying Chapter {num_end}", 0)
            pyperclip.copy(link)
        raise EndedManhwa(f"Manhwa supposedly ended at chapter {num_end}, link: {link}")
    return


if __name__ == '__main__':
    import argparse
    PATH = r"YOUR CLIENTCONFIG DIRECTORY PATH"
    os.chdir(PATH)
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument("-m", "--manhwa", required=True, help="enter the link of the "
                                                              "manga/manhwa")
    PARSER.add_argument("-c", "--chapter", required=True, help="enter the chapter number")
    PARSER.add_argument("-e", "--email", required=True, help="enter the email to send"
                                                             " notifications")
    ARGS = vars(PARSER.parse_args())
    MANWHA_LINK = ARGS['manhwa']
    NUM = ARGS['chapter']
    CHAPTER = "Chapter " + NUM
    MY_EMAIL = ARGS['email']
    # uncomment the block below if you don't want to use argparse
    # and instead want to edit it directly
    # manhwa_link = "https://toonily.com/webtoon/peerless-dad/"
    # num = "100"
    # chapter = "Chapter " + num
    # my_email = "example@gmail.com"
    MANHWA_NAME = MANWHA_LINK.split("/")[-2]
    MANHWA_NAME = " ".join(MANHWA_NAME.split('-')).title()
    # check if valid manhwa name or/and uploaded to toonily
    check_valid(MANWHA_LINK)
    # else check if manhwa already ended
    is_ended(MANWHA_LINK, NUM)
    # else continue
    CH_LINK = f"{MANWHA_LINK}chapter-{NUM}/"
    while 1:
        DT = datetime.datetime.now().strftime("%b-%d-%Y %I:%M:%S %p")
        ANS = main(MANWHA_LINK, CHAPTER)
        if ANS is True:
            SUBJECT = f"{MANHWA_NAME} {CHAPTER}"
            BODY = f"{MANHWA_NAME} {CHAPTER} is updated {DT}, link: {CH_LINK}"
            print(BODY)
            send_email(my_email=MY_EMAIL, subject=SUBJECT, body=BODY)
            break
        elif ANS is False:
            print(f"{MANHWA_NAME} {CHAPTER} is NOT updated yet {DT}")
        else:
            print(f"{ANS} date {DT}")
        print("-" * 75)
        time.sleep(300)
        is_ended(MANWHA_LINK, NUM)  # check if it already ended periodically
        time.sleep(5) # add a little delay for sanity check
