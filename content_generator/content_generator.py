import requests
import json
import os
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

class ContentGenerator:
    def __init__(self):
        self.together_api_key = os.environ.get("TOGETHER_API_KEY")
        logger.info(f"TOGETHER_API_KEY: {self.together_api_key}")

        self.api_url = "https://api.together.xyz/v1/completions"

    def generate_content(self, topic, content_type="article", word_count=500):

        headers = {
            "Authorization": f"Bearer {self.together_api_key}",
            "Content-Type": "application/json"
        }

        if content_type == "article":

            prompt = f"""Write an engaging article about {topic}.
            The article should be informative, well-structured, and around {word_count} words.
            Include a catchy title, introduction, several key points with explanations, and a conclusion.
            Keep the tone professional but accessible. 
            """

        elif content_type == "social_post":

            prompt = f"""Write an engaging social media post about {topic}.
            The post should be concise, use appropriate hashtags, and encourage engagement.
            include a hook, key information, and a call to action.
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

        if response.status_code == 200:
            content = response.json()["choices"][0]["text"]

            return {
                "topic": topic,
                "content_type": content_type,
                "content": content,
                "metadata": {
                    "model":"Llama-4-Maverick-17B-128E-Instruct-FP8",
                    "word_count": len(content.split()),
                    "generated_at": datetime.datetime.now().isoformat()
                }
            }
        
        else:
            logger.error(f"Error generating content: {response.text}")
            return None
# def main():
#     content = ContentGenerator()
    
# if __name__ == "__main__":
#     main()