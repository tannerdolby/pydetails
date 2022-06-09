"""
A module for fetching document metadata from a webpage 
and provides the utility to display social share cards via 
generated HTML.
"""

from typing import NamedTuple, Match
from collections import defaultdict
import re
import requests

class TagInfo(NamedTuple):
    """
    Represents <meta> tag matches from document metadata.
    """
    content: str
    html: str

class TagToken(NamedTuple):
    """
    Represents the tokenized <meta> tag matches.
    """
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
        self.doc = dict()
        self.tokenized = []

    def get(self, key: str):
        """
        Helper function to perform a lookup in the `doc` table.
        """
        if key in self.doc:
            return self.doc[key]
        if key in self.doc["twitter"]:
            return self.doc["twitter"][key]
        if key in self.doc["open_graph"]:
            return self.doc["open_graph"][key]

        return ""

    def match_metatags(self, html: str) -> None:
        """
        Iterate over all the <meta> tag matches within <head> and store them in `doc`.
        """
        attr_re = r'="(.*)"'
        attr_type_re = r'(property=".+?"|name=".+?")'
        content_re = rf'content{attr_re}'

        for match in re.finditer(r"<meta\s.*?\>", html):
            if not match:
                continue

            metatag = re.search(attr_type_re, match.group(0))

            if not metatag:
                continue

            if re.search(attr_type_re, match.group(0)):
                tag_type = re.search(attr_re, metatag.group(1)).group(1)

                if tag_type in ["description", "og:description", "twitter:description"]:
                    self.doc["description"] = TagInfo(
                        search_match(content_re, match),
                        match.group(0)
                    )
                elif tag_type.find("twitter:") != -1:
                    self.doc["twitter"][tag_type] = TagInfo(
                        search_match(content_re, match),
                        match.group(0)
                    )
                elif tag_type.find("og:") != -1:
                    self.doc["open_graph"][tag_type] = TagInfo(
                        search_match(content_re, match),
                        match.group(0)
                    )

            self.tokenized.append(TagToken("meta", match.group(0), match.start(), match.end()))

    def get_details(self, url=None) -> dict:
        """
        Fetch document metadata details. Defaults to fetching 
        from `self.url` if the `url` parameter is not specified.
        """
        if not self.url and not url:
            return {}

        if not self.url and url is not None:
            self.url = url

        host_re = r"https:\/\/(.*\.\w+)"
        unsecure_host_re = r"http:\/\/(.*\.\w+)"

        try:
            html = requests.get(self.url, headers=self.headers).text
            title = re.search(elem_regex("title"), html)

            # init fields to preserve this ordering of keys in `doc`
            self.doc["title"] = TagInfo(title.group(1), title.group(0))
            self.doc["description"] = ""
            self.doc["image"] = ""
            self.doc["image_alt"] = ""
            self.doc["url"] = ""
            self.doc["display_url"] = ""
            self.doc["twitter"] = {}
            self.doc["open_graph"] = {}

            self.tokenized.append(title)

            # collect_metatags and populate `doc`
            self.match_metatags(html)

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

        return self.doc

    def get_content(self, key: str):
        """
        Perform a lookup on the `doc` table and return the content
        from a `TagInfo` object.
        """
        if key in self.doc:
            if isinstance(self.doc[key], TagInfo):
                return self.doc[key].content
            return self.doc[key]

        # if key exists and corresponds to a TagInfo instance, then get the contents
        if key in self.doc["twitter"] and isinstance(self.doc["twitter"][key], TagInfo):
            return self.doc["twitter"][key].content

        if key in self.doc["open_graph"] and isinstance(self.doc["open_graph"][key], TagInfo):
            return self.doc["open_graph"][key].content

        return ""
    
    def build_card(self, card_type: str, doc: dict):
        """
        Generate HTML and styles for a social share card of type `card_type`.
        """
        if not doc:
            doc = self.doc

        card_styles= {
            "summary": {
                "css": "twitter-summary-image.css",
                "html": f'''
                <a href="{doc["url"]}">
                    <div class="card {card_type}">
                        <img src="{self.get_content("image")}" alt="{self.get_content("image_alt")}" />
                        <div>
                            <p>{doc["display_url"]}</p>
                            <h2>{self.get_content("title")}</h2>
                            <p>{self.get_content("description")}</p>
                        </div>
                    </div>
                </a>
                '''
            },
            "summary_large_image": {
                "css": "twitter-summary-large-image.css",
                "html": f'''
                <a class="card-link" href="{doc["url"]}" aria-label="Link to website">
                    <div class="card {card_type}">
                        <img src="{self.get_content("image")}" alt="{self.get_content("image_alt")}" />
                        <div>
                            <h2>{self.get_content("title")}</h2>
                            <p>{self.get_content("description")}</p>
                            <p>{doc["display_url"]}</p>
                        </div>
                    </div>
                </a>
                '''
            },
            # TODO: LinkedIn and Facebook cards
        }

        css = html = ""
        twitter_card_type = self.get_content("twitter:card")
        
        # compare card_type and get the correct html/css
        if card_type == "twitter" and twitter_card_type in card_styles:
            css = self.get_style(card_styles[twitter_card_type].get("css"))
            html = card_styles[twitter_card_type].get("html")

        elif card_type == "twitter" and twitter_card_type not in card_styles:
            # default to twitter:card = summary if a 
            # <meta name="twitter:card" /> tag isn't specified.
            css = self.get_style(card_styles["summary"].get("css"))
            html = card_styles["summary"].get("html")
        
        return f'''<style>\n{css}\n</style>\n{html}'''

    def get_style(self, stylesheet: str) -> str:
        """Read a stylesheets contents from card-styles directory."""
        with open(f"./card-styles/{stylesheet}", 'rt') as file:
            return file.read()


def elem_regex(head: str, tail: str=None) -> str:
    """
    Generate a regular expression for HTML element matching.
    """
    if not tail:
        tail = head

    return rf"<{head}>(.*)<\/{tail}>"

def search_match(regex: str, match: Match):
    """
    Helper to search first group of match object and return second group match.
    """
    return re.search(regex, match.group(0)).group(1)

# pydetail = PyDetails("https://developer.mozilla.org/en-US/")
# pydetail = PyDetails("https://11ty.dev")
# pydetail = PyDetails("https://www.zachleat.com/web/lighthouse-in-footer/")
# pydetail = PyDetails("https://tannerdolby.com")
# pydetail = PyDetails("https://chriscoyier.net/2022/06/04/silence-unknown-callers/")
# doc = pydetail.get_details()
# print(pydetail.get_details())
# print(doc["twitter"].keys())
# print(pydetail.get_style("twitter-summary-large-image.css"))
# print(pydetail.get("twitter:card").content)
# print(pydetail.build_card("twitter", pydetail.get_details()))
