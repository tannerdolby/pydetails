# pydetails
Fetch a URL and return the pages document metadata in a dictionary along with the option to render HTML previews of social share cards. 

The `doc` field on new instances of `PyDetails` will provide methods to vuewrender the social share card HTML for quick page previews.

_Note: logic still a work in progress, utility works best on URLs with "well-formatted" document metadata in the `<head>`_

## Usage

```python
page = PyDetails("https://tannerdolby.com")

print(page.get_details())
# defaultdict(<class 'dict'>,
# {
    # 'description': TagInfo(content="Hi, I'm Tanner. A software engineer and mathematician with a passion for building things for the web.", html='<meta name="description" content="Hi, I\'m Tanner. A software engineer and mathematician with a passion for building things for the web.">'),
    # 'display_url': 'tannerdolby.com',
    # 'image': TagInfo(content='https://tannerdolby.com/images/arch-spiral-large.jpg', html='<meta name="twitter:image" content="https://tannerdolby.com/images/arch-spiral-large.jpg">'),
    # 'image_alt': TagInfo(content='An Archimedean Spiral generated with JavaScript', html='<meta name="twitter:image:alt" content="An Archimedean Spiral generated with JavaScript">'),
    # 'meta': {
    #   'author': TagInfo(content='Tanner Dolby', html='<meta name="author" content="Tanner Dolby">'),
#     'generator': TagInfo(content='eleventy', html='<meta name="generator" content="eleventy">'),
#     ...
# }
```
Or define an instance of PyDetails without any parameters in the constructor to then provide a URL in the `get_details` call:

```python
page = PyDetails()

print(page.get_details("https://tannerdolby.com"))
# defaultdict(<class 'dict'>,
# ...
```

## Preview Social Share Cards
Generate social share card HTML for quick page previews.

Use `render_card(card_name, doc)` to generate social share HTML specific platforms i.e. Twitter, LinkedIn, etc. The following represents a generated "twitter" card:


```python
page = PyDetails("https://tannerdolby.com")

print(page.render_card("twitter", page.get_details()))
# <style>
# ...
# </style>
# <a href="https://tannerdolby.com" aria-label="Link to website">
#     <div class="card twitter">
#         <img src="https://tannerdolby.com/images/arch-spiral-large.jpg" alt="An Archimedean Spiral generated with JavaScript" />
#         <div>
#             <h2>Tanner Dolby</h2>
#             <p>Hi, I'm Tanner. A software engineer and mathematician with a passion for building things for the web.</p>
#             <p>tannerdolby.com</p>
#         </div>
#     </div>
# </a>
```

The following styles are added above the `<a>` tag when generated:

```css
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
```

### Preview of cards
HTML rendered in browser for a "twitter" social share card and in particular "summary_large_image" card type:

![browser demo](https://user-images.githubusercontent.com/48612525/172103997-bff16a70-0143-474d-b7cf-137690cd5d4b.png)

See the [card previews](/previews/) directory for more example cards.


## TODO
- [ ] Support LinkedIn card
- [ ] Support Facebook card

## License
[MIT](/LICENSE)
