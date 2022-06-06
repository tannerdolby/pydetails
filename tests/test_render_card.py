from src.metadata import PyDetails

page = PyDetails("https://tannerdolby.com")


def test_twitter_card():
    card = page.render_card("twitter", page.get_details())
    print(card)
    html = """<style>
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
        
        <a class="card-link" href="https://tannerdolby.com" aria-label="Link to website">
            <div class="card twitter">
                <img src="https://tannerdolby.com/images/arch-spiral-large.jpg" alt="An Archimedean Spiral generated with JavaScript" />
                <div>
                    <h2>Tanner Dolby</h2>
                    <p>Hi, I'm Tanner. A software engineer and mathematician with a passion for building things for the web.</p>
                    <p>tannerdolby.com</p>
                </div>
            </div>
        </a>
    """
    
    assert html == card