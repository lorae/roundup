from src.scraper.session import web_session
import requests

url: str = "https://www.bea.gov/research/papers"
headers: dict[any, any] = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
}
session_arguments = requests.Request(method='GET', url=url, headers=headers)
# Should this information be partially encapsulated in structured data?

if __name__ == "__main__":
    response = web_session(session_arguments)
    content = response.content
    print(content)
