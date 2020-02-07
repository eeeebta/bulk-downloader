# Scrape links and processing
from abc import ABC
from html.parser import HTMLParser
import re
import requests

import sys


# Boolean to validate url
def validate_url(input_url):
    with open("regex.txt") as f:
        regex_seq = str(f.read())
    if re.match(regex_seq, input_url):
        return True
    else:
        return False


def generate_download_links(count, url):
    with open(f"link_files/links_{count}.txt", "a+") as f:
        if isinstance(url, list):
            for gen_url in url:
                gen_url += "\n"
                f.write(gen_url)
        else:
            f.write(url)


def count_up():
    with open("count.txt", "r") as f:
        count = int(f.read())
    count += 1
    with open("count.txt", "w") as f:
        f.write(str(count))
    return count


def validate_zip(input_url):
    with open("zip_regex.txt") as f:
        regex_seq = str(f.read())
    if re.match(regex_seq, input_url):
        return True
    else:
        return False


def main():
    # Parse HTML and grab <a href="..."> data
    class ParseTagData(HTMLParser, ABC):
        def handle_starttag(self, tag, attrs):

            # Check
            if tag == "a" and "href" in attrs[0]:

                # Grab validated URL
                if validate_url(attrs[0][1]):
                    grab_tags.append(attrs[0][1])

    # Initialize URL as nothing
    url = None

    # Initialize grab_tags
    grab_tags = []
    valid = False
    url_list = None
    validated_urls = []
    list_of_urls = False
    # Check for system arguments in command line (python scrape_links.py <link>)
    if len(sys.argv) > 2:
        for ind in range(1, len(sys.argv)):
            print(sys.argv[ind])
        list_of_urls = True
    elif len(sys.argv) < 2:
        print("Switching to input mode...")
        url = input("URL(s) to scrape (separate with spaces): ")
        if url.count(" ") >= 2:
            url_list = url.split()
            list_of_urls = True
            print(list_of_urls)
        else:
            valid = validate_url(url)

    # Validate each url in the list that was submitted
    if list_of_urls:
        for grabbed_url in url_list:
            valid = validate_url(grabbed_url)
            print(f"VALID?: {valid}")
            if valid:
                validated_urls.append(grabbed_url)
                print("HIT IF")
        validated_urls = set(validated_urls)
        for valid_url in validated_urls:
            print("IN FOR")
            req = requests.get(valid_url)
            req = str(req.content)
            parser = ParseTagData()
            parser.feed(req)
            current_count = count_up()
            generate_download_links(current_count, grab_tags)
        count_up()
    # else:
    #     print("HIT ELSE")
    #     # For testing purposes; TODO REMOVE
    #     if not url and len(sys.argv) < 2:
    #         print("Skipped")
    #     # Finish thought sometime
    #     elif not url:
    #         url = sys.argv[1]
    elif valid:
        req = requests.get(url)
        req = str(req.content)
        parser = ParseTagData()
        parser.feed(req)
        current_count = count_up()
        generate_download_links(current_count, grab_tags)
    else:
        print("Invalid link(s) or none found")


if __name__ == '__main__':
    main()
