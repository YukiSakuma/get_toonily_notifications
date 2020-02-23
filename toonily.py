

"""Get email notifications of latest chapter of a manhwa/manga from toonily.com using ezgmail module"""
import datetime
import os
import requests
import time
import ezgmail

path = r"YOUR CLIENTCONFIG DIRECTORY PATH"
os.chdir(path)


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


def send_email(my_email,subject,body):
    while 1:
        dt = datetime.datetime.now().strftime("%b-%d-%Y %I:%M:%S %p")
        try:
            ezgmail.send(my_email,subject,body)
            print(f'Success sending email {dt}')
            return
        except:
            print(f"Error Trying again in 10 sec, {dt}")
        time.sleep(10)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--manhwa", required=True, help="enter the name of the manga/manhwa")
    parser.add_argument("-c", "--chapter", required=True, help="enter the chapter number")
    parser.add_argument("-e", "--email", required=True, help="enter the email to send notifications")
    args = vars(parser.parse_args())
    # manga = "peerless dad"
    # num = "69"
    # chapter = "Chapter " + num
    manga = args['manhwa']
    num = args['chapter']
    chapter = "Chapter " + num
    my_email = args['email']
    link = f"https://toonily.com/webtoon/{'-'.join(manga.lower().split())}"
    check = requests.get(link, stream=True); print(check.ok)
    if not check.ok:
        raise ValidManhwa(f"Not valid manhwa/manga, it doesn't exist, make sure the manhwa name is properly typed"
                          f" or is uploaded in toonily! {link}")
    ch_link = f"{link}/chapter-{num}/"
    while 1:
        dt = datetime.datetime.now().strftime("%b-%d-%Y %I:%M:%S %p")
        ans = main(chapter, link)
        if ans is True:
            subject = f"{manga} {chapter}"
            body = f"{manga} {chapter} is updated {dt}, link: {ch_link}"
            print(body)
            print(ch_link)
            send_email(my_email, subject, body)
            break
        elif ans is False:
            print(f"{manga} {chapter} is NOT updated yet {dt}")
        else:
            print(f"{ans} date {dt}")
        print("-"*100)
        time.sleep(300)


