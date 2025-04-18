import requests
import os
from bs4 import BeautifulSoup
from newspaper import Article
import datetime
import logging

from dotenv import load_dotenv
load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',  # Log messages will be saved to 'app.log'
    filemode='a'  # Append to the log file instead of overwriting
)

logger = logging.getLogger(__name__)

class TrendDetectionService:
    def __init__(self):
        self.news_api_key = os.environ.get("NEWS_API_KEY")
        # logger.info("TrendDetectionService initialized.")
        # logger.info(f"NEWS_API_KEY: {self.news_api_key}")

    def get_news_api_trends(self, category="technology"):
        url = f"https://newsapi.org/v2/top-headlines?category={category}&language=en&apiKey={self.news_api_key}"
        response = requests.get(url)
        # logger.info(f"Response: {response.status_code}")
        # logger.info(f"Response Content: {response.content}")
        if response.status_code == 200:
            return response.json()["articles"]
        return []
    
    def get_tech_blogs_trends(self):

        tech_blogs = [
                        "https://techcrunch.com/",
                        "https://www.theverge.com/",
                        "https://www.wired.com/"
                      ]
        articles = []

        for blog in tech_blogs:
            try:
                response = requests.get("https://techcrunch.com/")
                soup = BeautifulSoup(response.text, 'html.parser')
                links = soup.find_all('a', href=True)

                article_links = [link['href'] for link in links if 'article' in link['href'] or '/20' in link['href']]
                # logger.info(f"article_links: {article_links[:3]}")
                for link in article_links[:3]:
                    if not link.startswith('http'):
                        link = blog + link
                    logger.info(f"link: {link}")
                    article = Article(link)
                    article.download()
                    article.parse()
                    # logger.info(f"articles: {article.title} & {article.text}")
                    if article.title and article.text:
                        articles.append({
                            "title": article.title,
                            "url": link,
                            "source": blog,
                            "summary":  article.text[:200] + "...",
                            "published_at": article.publish_date or datetime.datetime.now()
                        })
                        # logger.info(f"articles: {articles}")
            except Exception as e:
                    logger.error(f"Error processing blog {blog}: {e}")

        logger.info(f"link: {links[45]['href']}")
        

        return articles

    def get_all_trends(self):

        trends = {
            "news_api": self.get_news_api_trends(),
            "tech_blogs": self.get_tech_blogs_trends()
        }
        logger.info(f"trends: {trends}")
        return trends

            
# def main():
#     trend_service = TrendDetectionService()
#     articles = trend_service.get_news_api_trends()

#     # logger.info(f"Fetched {len(articles)} articles from News API.")
#     # logger.info(f"Articles: {articles[0]}")

#     blogs = trend_service.get_tech_blogs_trends()

#     trends = trend_service.get_all_trends()

#     # logger.info(f"Blog content: {blogs.text}")

# if __name__ == "__main__":