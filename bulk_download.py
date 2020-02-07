import wget
from datetime import date


def grab_count():
    with open("count.txt", "r") as f:
        count = int(f.read())
    count -= 1
    return count


def main():
    urls = []
    count = grab_count()
    grabbed_date = str(date.today()).replace("-", "")

    for url in urls:
        wget.download(url, f"downloads/download_{count}_{grabbed_date}/")
