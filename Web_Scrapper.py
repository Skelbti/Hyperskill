import requests
import string
import os


from urllib.parse import urljoin
from bs4 import BeautifulSoup

def ask_inputs():
    n_pages = int(input())
    file_type = input()
    return n_pages, file_type


def request_url_bs_parser(url):
    r = requests.get(url)
    s = BeautifulSoup(r.content, "html.parser")
    return s


def create_filename(title):
    for p in string.punctuation:
        title = title.replace(p, "")
    title = title.strip()
    return title.replace(" ", "_")


def create_directory(n_page):
    dir_name = f"Page_{n_page}"
    os.mkdir(dir_name)
    return dir_name


def link_pages_article(n_page):
    return f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={n_page}"


def get_articles_by_type(parser, art_type):
    articles = parser.find_all("article")
    for a in articles:
        if a.find("span", {"data-test": "article.type"}).text.strip() == art_type:
            yield a


def get_art_title_art_link(art, url):
    tag_a = art.find("a", {"data-track-action": "view article"})
    title = tag_a.text
    link = urljoin(url, tag_a.get("href"))
    return title, link


def get_art_body(art_link):
    art = request_url_bs_parser(art_link)
    res = art.find("div", {"class": "c-article-body"})
    if res is None:
        res = art.find("div", {"class": "article-item__body"})
    if res is None:
        res = art.find("article")
    return res.text.strip()


def save_art(title, art_content, directory):
    with open(directory + "/" + create_filename(title) + ".txt", "wb") as file:
        file.write(art_content.encode("utf-8"))


def main():
    url = "https://www.nature.com/nature/articles"
    n_pages, art_type = ask_inputs()
    for n_p in range(n_pages):
        dir = create_directory(n_p + 1)
        page = request_url_bs_parser(url)
        articles = get_articles_by_type(page, art_type)
        for a in articles:
            title, link = get_art_title_art_link(a, url)
            content = get_art_body(link)
            save_art(title, content, dir)
        url = link_pages_article(n_p + 2)


if __name__ == "__main__":
    main()
