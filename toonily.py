"""Get email notifications of latest chapter of a manhwa/manga from toonily.com using ezgmail module"""
import datetime
import os
import re
import requests
import time
import ezgmail


class EndedManhwa(Exception):
    pass


class ValidManhwa(Exception):
    pass


def main(link, chapter):
    try:
        r = requests.get(link, stream=True)
    except:
        return "Error trying again in 300 sec"

    if chapter in r.text:
        # print(r.text)
        return True
    else:
        return False


def send_email(my_email, subject, body):
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
    check_status = requests.get(link, stream=True)
    if check_status.ok:
        return
    else:
        raise ValidManhwa(f"Not valid manhwa/manga link, make sure the manhwa url is valid\n"
                          f"{link}")


def is_ended(link, num):
    check_end = re.compile(r"Chapter \d* - The End")
    r = requests.get(link, stream=True).text
    result = check_end.search(r)
    if result:
        print(link)
        result = result.group()
        r = result.split()
        num_end = r[1]
        if int(num) <= int(num_end):
            ch_link = f"{link}chapter-{num}"
            print("Click or copy link below if you want to go to the chapter number you entered")
            print(ch_link)
        else:
            print(f"Invalid chapter {num}")
        link = f"{link}chapter-{num_end}"
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
        is_ended(manhwa_link, num)  # check if it already ended periodically
        if ans is True:
            subject = f"{manhwa_name} {chapter}"
            body = f"{manhwa_name} {chapter} is updated {dt}, link: {ch_link}"
            print(body)
            print(ch_link)
            send_email(my_email, subject, body)
            break
        elif ans is False:
            print(f"{manhwa_name} {chapter} is NOT updated yet {dt}")
        else:
            print(f"{ans} date {dt}")
        print("-" * 75)
        time.sleep(300)


