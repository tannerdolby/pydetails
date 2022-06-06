from typing import TypeVar, NamedTuple, Match, Dict, List
from collections import defaultdict
import requests
import re

class TagInfo(NamedTuple):
    content: str
    html: str

class MetaTagToken(NamedTuple):
    element: str
    match: str
    start: int
    end: int

class PyDetails:
    """
    Class representing document metadata details for a given URL.
    """
    doc: dict[str, TagInfo]

    def __init__(self, page_url: str=None, request_headers: dict=None):
        self.url= page_url
        self.headers = request_headers or {'Content-Type': 'text/html', 'accept': 'text/html'}
        self.doc = defaultdict(dict)
        self.tokenized = []

    def get(self, key: str):
        if key in self.doc:
            return self.doc[key]
        if key in self.doc["meta"]:
            return self.doc["meta"][key]
        return ""

    def get_details(self, url=None) -> dict:
        """
        Fetch page metadata details.
        """
        if not self.url and not url:
            return {}
        
        if not self.url and url is not None:
            self.url = url
        
        attr_re = r'="(.*)"'
        attr_type_re = rf'(property=".+?"|name=".+?"|http-equiv=".+?")'
        content_re = rf'content{attr_re}'
        host_re = r"https:\/\/(.*\.\w+)"
        unsecure_host_re = r"http:\/\/(.*\.\w+)"

        try:
            html = requests.get(self.url, headers=self.headers).text
            title = re.search(elem_regex("title"), html)

            self.doc["title"] = TagInfo(title.group(1), title.group(0))
            self.doc["meta"] = {}
            self.tokenized.append(title)

            # iterate over all the <meta> tag matches in <head> and store them in the table
            for match in re.finditer(r"<meta\s.*?\>", html):
                if not match: continue
                metatag = re.search(attr_type_re, match.group(0))
                if not metatag: continue
                if re.search(attr_type_re, match.group(0)):
                    tag_type = re.search(attr_re, metatag.group(1)).group(1)
                    if tag_type in ["viewport", "X-UA-Compatible"]:
                        continue
                    if tag_type == "description":
                        self.doc["description"] = tag(search_match(content_re, match), match.group(0))

                    self.doc["meta"][tag_type] = tag(search_match(content_re, match), match.group(0))

                self.tokenized.append(MetaTagToken("meta", match.group(0), match.start(), match.end()))
            
            twitter_url = self.get("twitter:url")
            og_url = self.get("og:url")
            twitter_img = self.get("twitter:image")
            twitter_img_alt = self.get("twitter:image:alt")
            og_img = self.get("og:image")
            og_img_alt = self.get("og:image:alt")

            self.doc["image"] = twitter_img or og_img
            self.doc["image_alt"] = twitter_img_alt or og_img_alt
            self.doc["url"] = self.url or twitter_url.content or og_url.content

            ssl_url = re.search(host_re, self.doc["url"])
            non_ssl_url = re.search(unsecure_host_re, self.doc["url"])

            if ssl_url:
                ssl_url = ssl_url.group(1)
            
            if non_ssl_url:
                non_ssl_url = non_ssl_url.group(1)

            self.doc["display_url"] = ssl_url or non_ssl_url

        except Exception as exc:
            print(f"Error fetching '{self.url}' - {exc}'")

        print(self.doc["meta"].keys())
        return self.doc
    
    def get_content(self, key: str):
        """
        Perform a lookup on the `doc` table and return the element content
        from a `TagInfo` object.
        """
        def helper():
            if type(self.doc[key]) == TagInfo:
                return self.doc[key].content
            return self.doc[key]

        if key in self.doc:
            return helper()
        elif key in self.doc["meta"]:
            return helper()
        else:
            return ""


    def render_card(self, card_type: str, doc: dict):
        return f'''
        {self.get_style()}
        <a class="card-link" href="{self.doc["url"]}" aria-label="Link to website">
            <div class="card {card_type}">
                <img src="{self.get_content("image")}" alt="{self.get_content("image_alt")}" />
                <div>
                    <h2>{self.get_content("title")}</h2>
                    <p>{self.get_content("description")}</p>
                    <p>{self.doc["display_url"]}</p>
                </div>
            </div>
        </a>
        '''

    def get_style(self) -> str:
        """Styles for twitter "summary_large_image" cards"""
        return '''
        <style>
        *,
        *::before,
        *::after {
            box-sizing: border-box;
        }

        :root {
            --twitter-macOS-font: Helvetica Neue, Helvetica;
            --twitter-windows-font: Segoe UI, Arial;
        }

        .card-link {
            color: inherit;
            text-decoration: none;
        }

        .twitter {
            font-family: var(--twitter-macOS-font, sans-serif);
        }

        .card {
            display: flex;
            flex-direction: column;
            max-width: 35ch;
            border: 1px solid lightgray;
            border-radius: 10px;
            font-size: clamp(.9rem, 3vw, 1rem);
        }

        .card div {
            padding: 10px 10px;
            margin: 0 auto;
            text-overflow: ellipsis;
            overflow: hidden;
            width: 100%;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        }

        .card h2,
        .card div p {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .card h2 {
            font-size: clamp(.9rem, 1vw, 1rem);
            margin: 0 0 5px 0;
        }

        .card div p {
            font-size: 14px;
            margin: 0;
        }

        .card img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            min-height: 210px;
            max-height: 215px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }

        .card h2 + p {
            margin: 4px 0;
        }

        .card p:last-child {
            margin-top: 6px;
            color: #888;
        }
        </style>
        '''

def tag(content: str, html: str) -> TagInfo:
    """
    Create a new instance of `TagInfo`.
    """
    return TagInfo(content, html)

def elem_regex(head: str, tail: str=None) -> str:
    """
    Generate a regular expression for HTML element matching.
    """
    if not tail:
        tail = head

    return rf"<{head}>(.*)<\/{tail}>"

def search_match(regex: str, m: Match):
    """
    Helper to search a match object and return second group match
    """
    return re.search(regex, m.group(0)).group(1)
    
# pydetail = PyDetails("https://developer.mozilla.org/en-US/")
# pydetail = PyDetails("https://11ty.dev")
# pydetail = PyDetails("https://www.zachleat.com/web/lighthouse-in-footer/")
# pydetail = PyDetails("https://tannerdolby.com")
# pydetail = PyDetails("https://chriscoyier.net/2022/06/04/silence-unknown-callers/")
# print(pydetail.doc)

# print(pydetail.render_card("twitter", pydetail.get_details()))
