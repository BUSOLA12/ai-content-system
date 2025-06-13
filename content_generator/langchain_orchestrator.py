from langchain.prompts import PromptTemplate
from langchain_together import Together
import os
import json
from datetime import datetime
from .trend_service import TrendDetectionService
from .topic_extractor import TopicExtractor
from .content_generator import ContentGenerator

from langchain_core.runnables import RunnableSequence
from langchain_core.runnables.config import RunnableConfig


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
        self.content_generator = ContentGenerator()
        self.together_api_key = os.environ.get("TOGETHER_API_KEY")
        logger.info(f"together_api: {self.together_api_key}")
        self.llm = Together(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            together_api_key=self.together_api_key,
            max_tokens=1000
        )
    def create_topic_selection_chain(self):

        template = """
                    You are an expert content strategist. 

                    Below is a list of trending topics:
                    {topics}

                    Select the top 3 most engaging and promising topics for social media content. For each, provide:
                    1. Topic name
                    2. Why it's engaging
                    3. Best content format (article/social_post)

                    **Critical Instructions:**
                    - Return ONLY a SINGLE valid JSON list
                    - STRICTLY avoid markdown, code blocks, or backticks
                    - No extra text before/after the JSON
                    - Never add explanations
                    - Never wrap JSON in parentheses

                    Example of allowed format:
                    [{{"topic": "...", "reason": "...", "best_format": "..."}}]

                    Your response must be EXACTLY like the example above but with real data.
                    """



        prompt = PromptTemplate(template=template, input_variables=["topics"])

        chain = prompt | self.llm
        

        return chain

    def run_content_workflow(self):

        print("Fetching trends...")
        trends_data = self.trend_service.get_all_trends()

        print("Extracting Topics...")
        topics = self.topic_extractor.extract_topics_from_trends(trends_data)

        print("Selecting best topics...")
        topic_chain = self.create_topic_selection_chain()
        topics_str ="\n".join([f"- {topic}" for topic in topics])
        logger.info(f"topics_str: {topics_str}")

        try:
            selection_result = topic_chain.invoke({"topics": topics_str})
            selection_result = selection_result.strip('\n').strip('```')
        except Exception as e:
            logger.error(f"Error for LLM: {str(e)}")
        logger.info(f"selection_result: {selection_result}")

        try:
            logger.info(f"selection_result new: {selection_result}")
            selected_topics = json.loads(selection_result)
            logger.info(f"selected_topics: {selected_topics}")

        except json.JSONDecodeError:
            logger.error("Failed to pass topic selection. Using default selection")

            selected_topics = [{"topic": topics[0], "best_format": "article"}] if topics else []


        generated_contents = []

        for topic_info in selected_topics:
            topic = topic_info["topic"]
            # logger.info(f"topic: {topic}")
            content_type = topic_info.get("best_format", "article")
            # logger.info(f"content_type: {content_type}")

            print(f"Generating {content_type} about {topic}...")

            content = self.content_generator.generate_content(topic, content_type)
            # logger.info(f"content: {content}")

            if content:
                generated_contents.append(content)
                logger.info(f"generated_contents: {generated_contents}")

        return {
            "workflow_id": f"content-gen-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "generated_at": datetime.now().isoformat(),
            "topics_analyzed": len(topics),
            "contents_generated": generated_contents
        }

        

# def main():
#     AI = ContentWorkflow()
#     output = AI.create_topic_selection_chain()
#     logger.info(f"AI_output: {output}")

# if __name__ == "__main__":
#     main()
