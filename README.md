# pydetails
Fetch a URL and return the pages document metadata in a dictionary along with the option to render HTML previews of social share cards. The `doc` field on new instances of `PyDetails` represents the metadata table consisting of `<meta>` tags and document metadata from the `<head>` of a webpage. The class instance provides two main functionalites, `get_details` to populate the metadata table in `self.doc` and `render_card` to render social share card HTML for quick page previews.

_Note: logic still a work in progress, utility works best on URLs with "well-formatted" document metadata in the `<head>`_

## Usage

```python
page = PyDetails("https://tannerdolby.com")

print(page.get_details())

defaultdict(<class 'dict'>,
{
    'title': TagInfo(content='Tanner Dolby', html='<title>Tanner Dolby</title>'),
    'description': TagInfo(content="Hi, I'm Tanner. A software engineer and mathematician with a passion for building things for the web.", html='<meta name="description" content="Hi, I\'m Tanner. A software engineer and mathematician with a passion for building things for the web.">'), 
    'image': TagInfo(content='https://tannerdolby.com/images/arch-spiral-large.jpg', html='<meta name="twitter:image" content="https://tannerdolby.com/images/arch-spiral-large.jpg">'),
    'image_alt': TagInfo(content='An Archimedean Spiral generated with JavaScript', html='<meta name="twitter:image:alt" content="An Archimedean Spiral generated with JavaScript">'),
    'url': 'https://tannerdolby.com', 
    'display_url': 'tannerdolby.com', 
    'open_graph': List[TagInfo],
    'twitter': List[TagInfo]
}
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
```

generating the following card HTML:

```html
<style>
...
</style>
<a href="https://tannerdolby.com" aria-label="Link to website">
    <div class="card twitter">
        <img src="https://tannerdolby.com/images/arch-spiral-large.jpg" alt="An Archimedean Spiral generated with JavaScript" />
        <div>
            <h2>Tanner Dolby</h2>
            <p>Hi, I'm Tanner. A software engineer and mathematician with a passion for building things for the web.</p>
            <p>tannerdolby.com</p>
        </div>
    </div>
</a>
```

Each social share card will have associated styling generated with it. The specific [styles](/card-styles/) can be viewed from `/card-styles/`.


### Preview of cards
HTML rendered in browser for a "twitter" social share card and in particular "summary_large_image" card type:

![browser demo](https://user-images.githubusercontent.com/48612525/172103997-bff16a70-0143-474d-b7cf-137690cd5d4b.png)

See the [card previews](/previews/) directory for more example cards.


## TODO
- [ ] Support LinkedIn card
- [ ] Support Facebook card

## License
[MIT](/LICENSE)
