from bs4 import BeautifulSoup


async def process_html(html: str) -> str:
    soup = BeautifulSoup(html)
    body = soup.find("body")
    body_inner_text = "".join(body.findAll(text=True))
    return body_inner_text


__all__ = ["process_html"]
