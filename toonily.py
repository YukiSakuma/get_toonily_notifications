"""Get email notifications of latest chapter of a manhwa/manga from toonily.com using ezgmail module"""
import ctypes
import datetime
import os
import re
import requests
import time
import ezgmail
import pyperclip


class EndedManhwa(Exception):
    "Manhwa ended already exception"
    pass


class ValidManhwa(Exception):
    """Manhwa is not valid exception"""
    pass


def main(link, chapter):
    """Main link chapter check"""
    try:
        r = requests.get(link, stream=True)
    except:
        return "Error trying again in 300 sec"
    
    
    try:
        if chapter in r.text:
            # print(r.text)
            return True
        else:
            return False
    except:
        return False


def send_email(my_email, subject, body):
    """send email notification"""
    while 1:
        dt = datetime.datetime.now().strftime("%b-%d-%Y %I:%M:%S %p")
        try:
            ezgmail.send(my_email, subject, body)
            print(f'Success sending email {dt}')
            return
        except:
            print(f"Error Trying again in 10 sec, {dt}")
        time.sleep(10)


def check_valid(link):
    """check if manhwa is valid on toonily site"""
    check_status = requests.get(link, stream=True)
    if check_status.ok:
        return
    else:
        raise ValidManhwa(f"Not valid manhwa/manga link, make sure the manhwa url is valid\n"
                          f"{link}")


def is_ended(link, num):
    """check if manwha already ended"""
    check_end = re.compile(r"Chapter \d* - The End")
    try:
        r = requests.get(link, stream=True).text
    except:
        return
    result = check_end.search(r)
    if result:
        print(f"Manhwa homepage: {link}\n")
        result = result.group()
        r = result.split()
        num_end = r[1]
        if int(num) <= int(num_end):
            ch_link = f"{link}chapter-{num}"
            print("The link of the chapter number you entered below is copied\n")
            print(ch_link)
            ctypes.windll.user32.MessageBoxW(0, f"{ch_link}\nClose this window to finish copying the link",
                                             f"Copying Chapter {num}", 0)
            pyperclip.copy(ch_link)
        else:
            print(f"Invalid chapter {num}")
            link = f"{link}chapter-{num_end}"
            ctypes.windll.user32.MessageBoxW(0, f"Invalid chapter {num}, manhwa already ended at chapter {num_end}\n"
                                                f"{link}\nClose this window to finish copying the link",
                                                f"Copying Chapter {num_end}", 0)
            pyperclip.copy(link)
        raise EndedManhwa(f"Manhwa supposedly ended at chapter {num_end}, link: {link}")
    return


if __name__ == '__main__':
    import argparse
    path = r"YOUR CLIENTCONFIG DIRECTORY PATH"
    os.chdir(path)
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--manhwa", required=True, help="enter the link of the manga/manhwa")
    parser.add_argument("-c", "--chapter", required=True, help="enter the chapter number")
    parser.add_argument("-e", "--email", required=True, help="enter the email to send notifications")
    args = vars(parser.parse_args())
    manhwa_link = args['manhwa']
    num = args['chapter']
    chapter = "Chapter " + num
    my_email = args['email']
    # uncomment the block below if you don't want to use argparse and instead want to edit it directly
    # manhwa_link = "https://toonily.com/webtoon/peerless-dad/"
    # num = "100"
    # chapter = "Chapter " + num
    # my_email = "example@gmail.com"
    manhwa_name = manhwa_link.split("/")[-2]
    manhwa_name = " ".join(manhwa_name.split('-')).title()
    # check if valid manhwa name or/and uploaded to toonily
    check_valid(manhwa_link)
    # else check if manhwa already ended
    is_ended(manhwa_link, num)
    # else continue
    ch_link = f"{manhwa_link}chapter-{num}/"
    while 1:
        dt = datetime.datetime.now().strftime("%b-%d-%Y %I:%M:%S %p")
        ans = main(manhwa_link, chapter)
        if ans is True:
            subject = f"{manhwa_name} {chapter}"
            body = f"{manhwa_name} {chapter} is updated {dt}, link: {ch_link}"
            print(body)
            send_email(my_email, subject, body)
            break
        elif ans is False:
            print(f"{manhwa_name} {chapter} is NOT updated yet {dt}")
        else:
            print(f"{ans} date {dt}")
        print("-" * 75)
        time.sleep(300)
        is_ended(manhwa_link, num)  # check if it already ended periodically
        time.sleep(5) # add a little delay for sanity check


