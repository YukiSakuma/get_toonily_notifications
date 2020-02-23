

"""Get email notifications of latest chapter of a manhwa/manga from toonily.com using ezgmail module"""
import datetime
import os
import re
import requests
import time
import ezgmail

path = r"YOUR CLIENTCONFIG DIRECTORY PATH"
os.chdir(path)


class EndedManhwa(Exception):
    pass


class ValidManhwa(Exception):
    pass


def main(chapter, link):
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
            ezgmail.send(my_email,subject,body)
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
        raise ValidManhwa(f"Not valid manhwa/manga, make sure the manhwa name is properly typed\n"
                          f" or is uploaded in toonily! If it's 'ripped' run the script again and add 'english' "
                          f"at the end of the manwha name\n or go toonily first find it and check its url title \n"
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
            ch_link = f"{link}/chapter-{num}"
            print("Click or copy link below if you want to go to the chapter number you entered")
            print(ch_link)
        else:
            print(f"Invalid chapter {num}")
        link = f"{link}/chapter-{num_end}"
        raise EndedManhwa(f"Manhwa supposedly ended at chapter {num_end}, link: {link}")
    return

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--manhwa", required=True, help="enter the name of the manga/manhwa")
    parser.add_argument("-c", "--chapter", required=True, help="enter the chapter number")
    parser.add_argument("-e", "--email", required=True, help="enter the email to send notifications")
    args = vars(parser.parse_args())
    manga = args['manhwa']
    num = args['chapter']
    chapter = "Chapter " + num
    my_email = args['email']
    # manga = "peerless dad"          #uncomment if you don't want to use argparse and edit it directly
    # num = "100"                     #uncomment if you don't want to use argparse and edit it directly
    # chapter = "Chapter " + num      #uncomment if you don't want to use argparse and edit it directly
    # my_email = "example@gmail.com"  #uncomment if you don't want to use argparse and edit it directly
    link = f"https://toonily.com/webtoon/{'-'.join(manga.lower().split())}"

    # check if valid manhwa name or/and uploaded to toonily
    check_valid(link)
    # else check if manhwa already ended
    is_ended(link, num)
    # else continue
    ch_link = f"{link}/chapter-{num}/"
    while 1:
        dt = datetime.datetime.now().strftime("%b-%d-%Y %I:%M:%S %p")
        ans = main(chapter, link)
        is_ended(link, num) # check if it already ended periodically
        if ans is True:
            subject = f"{manga} {chapter}"
            body = f"{manga} {chapter} is updated {dt}, link: {ch_link}"
            print(body)
            print(ch_link)
            send_email(my_email, subject, body)
            break
        elif ans is False:
            print(f"{manga.title()} {chapter} is NOT updated yet {dt}")
        else:
            print(f"{ans} date {dt}")
        print("-"*100)
        time.sleep(300)


