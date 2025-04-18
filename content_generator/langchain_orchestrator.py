from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_together import Together
import os
import json
from datetime import datetime

from .trend_service import TrendDetectionService
from .topic_extractor import TopicExtractor
from .content_generator import ContentGenerator

from dotenv import load_dotenv
load_dotenv()

import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',  # Log messages will be saved to 'app.log'
    filemode='a'  # Append to the log file instead of overwriting
)

logger = logging.getLogger(__name__)


class ContentWorkflow:
    def __init__(self):
        self.trend_service = TrendDetectionService()
        self.topic_extractor = TopicExtractor()
        self. content_generator = ContentGenerator()
        self.together_api_key = os.environ.get("TOGETHER_API_KEY")
        self.llm = Together(
            model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
            together_api_key=self.together_api_key
        )

    
    def create_topic_selection_chain(self):

        template = """
                You are an expect content strategist. Below is a list of trending topics:
                {topics}

                Select the top 3 most engaging and promising topics for creating content that would perform well on social media.
                For each selected topic, provide:
                1. The topic name
            `   2. Why it would be engaging
                3. What content format would work best (article, social post, video script)

                Respond in JSON format like:
                ```json
                [
                    {{
                        "topic": "topic name",
                        "reason": "why this topic is engaging",
                        "best_format": "article|social_post|video_script"
                    }},
                    ...
                
                ]
                ```
        """

        prompt = PromptTemplate(template=template, input_variables=["topics"])

        return LLMChain(llm=self.llm, prompt=prompt)

    def run_content_workflow(self):

        print("Fetching trends...")
        trends_data = self.trend_service.get_all_trends()

        print("Extracting Topics...")
        topics = self.topic_extractor.extract_topics_from_trends()

        print("Selecting best topics...")
        topic_chain = self.create_topic_selection_chain()
        topics_str ="\n".join([f"- {topic}" for topic in topics])
        selection_result = topic_chain.invoke({"topics": topics_str})

        try:

            selected_topics = json.loads(selection_result)

        except json.JSONDecodeError:
            logger.error("Failed to pass topic selection. Using default selection")

            selected_topics = [{"topic": topics[0]}, {"best_format": "article"}] if topics else []


        genarated_contents = []

        for topic_info in selected_topics:
            topic = topic_info["topic"]
            content_type = topic_info.get("best_format", "article")

            print(f"Generating {content_type} about {topic}...")

            content = self.content_generator.generate_content(topic, content_type)

            if content:
                generated_contents.append(content)

            return {
                "workflow_id": f"content-gen-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                "generated_at": datetime.now().isoformat(),
                "topics_analyzed": len(topics),
                "contents_generated": generated_contents
            }

        

                