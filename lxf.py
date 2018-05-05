import requests
from bs4 import BeautifulSoup
import pdfkit
from concurrent.futures import ThreadPoolExecutor
import os
import re

import proxy

domain = "https://www.liaoxuefeng.com"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWeb"
    "Kit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
}

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{body}
</body>
</html>
"""

count = 0
retry = 0
ban = 0


def parse_url():

    python = "/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000"
    rsp = requests.get(domain + python, headers=headers)

    soup = BeautifulSoup(rsp.text, "html.parser")
    divs = soup.find_all(depth=re.compile("\d"))
    urls = []
    for div in divs:
        urls.append(domain + div.a.get("href"))
    return urls


def parse_body(url):
    global retry
    try:
        rsp = requests.get(url, headers=headers, proxies=proxy.get(), timeout=15)
    except Exception:
        retry += 1
        print("重爬次数：{}".format(retry))
        return parse_body(url)

    if rsp.status_code == 503:
        global ban
        ban += 1
        print("封IP次数：{}".format(ban))
        return parse_body(url)

    soup = BeautifulSoup(rsp.text, "html.parser")
    title = soup.find_all("h4")[-1].text
    body = soup.find(class_="x-wiki-content x-main-content")

    # 标题居中，h1 样式，添加到 body
    center_tag = soup.new_tag("center")
    title_tag = soup.new_tag("h1")
    title_tag.string = title
    center_tag.insert(0, title_tag)
    body.insert(0, center_tag)

    html = html_template.format(body=str(body))
    global count
    count += 1
    print("爬取页面成功数：{}".format(count))
    html = html.replace("data-src", "src")
    return html


def make_pdf(htmls):
    html_files = []
    for index, html in enumerate(htmls):
        file = str(index) + ".html"
        html_files.append(file)
        with open(file, "w", encoding="utf-8") as f:
            f.write(html)

    options = {
        "page-size": "Letter",
        "margin-top": "0.75in",
        "margin-right": "0.75in",
        "margin-bottom": "0.75in",
        "margin-left": "0.75in",
        "encoding": "UTF-8",
        "custom-header": [("Accept-Encoding", "gzip")],
        "cookie": [
            ("cookie-name1", "cookie-value1"), ("cookie-name2", "cookie-value2")
        ],
        "outline-depth": 10,
    }
    try:
        pdfkit.from_file(html_files, "python.pdf", options=options)
    except Exception:
        pass

    for file in html_files:
        os.remove(file)

    print("已制作电子书 python.pdf 在当前目录！")


if __name__ == "__main__":
    urls = parse_url()
    with ThreadPoolExecutor(max_workers=16) as executor:
        htmls = executor.map(parse_body, urls)
    make_pdf(htmls)
