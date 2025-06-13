import requests
import json
import os
import logging
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',  # Log messages will be saved to 'app.log'
    filemode='a'  # Append to the log file instead of overwriting
)

logger = logging.getLogger(__name__)

class ContentGenerator:
    def __init__(self):
        self.together_api_key = os.environ.get("TOGETHER_API_KEY")
        logger.info(f"TOGETHER_API_KEY: {self.together_api_key}")

        self.api_url = "https://api.together.xyz/v1/completions"

    def generate_content(self, topic, content_type="article", word_count=500):

        logger.info(f"From generate_content method: {topic} and {content_type}")

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
            "Content-Type": "application/json"
        }

        if content_type == "article":

            prompt = f"""
                        Write a well-structured, engaging, and informative article about {topic}, around {word_count} words.

                        The article should include:
                        - A catchy and relevant title that draws reader interest.
                        - An introduction that clearly presents the topic and its importance.
                        - Several key points, each with clear explanations and relevant examples or data to support them.
                        - A concise conclusion that summarizes the main ideas and provides a closing thought or call to action.

                        Use a professional yet accessible tone that is easy to read.
                        Vary sentence length to maintain reader interest, mixing short and long sentences.
                        Avoid repetition, unclear phrases, or awkward sentence structures.
                        Ensure smooth transitions between paragraphs and ideas.
                        Write in clear, concise language suitable for a broad audience.
                        """


        elif content_type == "social_post":

            prompt = f"""
                        Write a highly engaging social media post about {topic}.

                        The post should:
                        - Start with a strong hook that grabs attention in the first line.
                        - Clearly convey the main idea or key information in a concise and compelling way.
                        - Use an informal, friendly tone suitable for platforms like Facebook or Instagram.
                        - Include 3–5 relevant and trending hashtags placed naturally.
                        - End with a call to action (e.g., comment, share, follow, click a link, etc.).
                        - Keep the total length under 100–150 words.

                        Focus on making it relatable and easy to read, with line breaks for better readability.
                        Avoid sounding robotic or too promotional—make it feel like a real person is posting.
                        """

        else:

            prompt = f"""Write about {topic} in a {content_type} format.
            """

        data = {
            "model": "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
            "prompt": prompt,
            "max_tokens": min(1500, word_count*2),
            "temperature": 0.7,
            "top_p": 0.9,
            "frequency_penalty": 0.5
        }

        response = requests.post(self.api_url, headers=headers, data=json.dumps(data))
        # logger.info(f"response from generate content method: {response.json()["choices"][0]["text"]}")

        if response.status_code == 200:
            content = response.json()["choices"][0]["text"]

            return {
                "topic": topic,
                "content_type": content_type,
                "content": content,
                "metadata": {
                    "model":"Llama-4-Maverick-17B-128E-Instruct-FP8",
                    "word_count": len(content.split()),
                    "generated_at": datetime.now().isoformat()
                }
            }
        
        else:
            logger.error(f"Error generating content: {response.text}")
            return None
# def main():
#     content = ContentGenerator()
    
# if __name__ == "__main__":
#     main()