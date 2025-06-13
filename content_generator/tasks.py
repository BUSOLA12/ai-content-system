from .models import GeneratedContent
from .langchain_orchestrator import ContentWorkflow
from celery import shared_task
from django.conf import settings
import logging
import json
from .models import GeneratedContent, User, Notification
from fcm_django.models import FCMDevice
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

# @shared_task
# def add(x, y):
#     return x + y



@shared_task
def generate_content_task():

    logger.info("Starting scheduled content generation workflow")

    try:
        workflow = ContentWorkflow()
        result = workflow.run_content_workflow()
        logger.info(f"result: {result}")


        saved_contents = []

        # content_data = result.get('contents_generated')
        # logger.info(f"content_data: {content_data}")
        # logger.info(f"topic: {content_data['topic']}")
        # logger.info(f"content_type: {content_data['content_type']}")
        # logger.info(f"content: {content_data['content']}")
        # logger.info(f"metadata: {content_data['metadata']}")

        
        for content_data in result.get('contents_generated'):
            logger.info(f"content_data: {content_data}")
            content = GeneratedContent(
                topic=content_data['topic'],
                content_type=content_data['content_type'],
                content=content_data['content'],
                metadata=content_data['metadata']
            )
            content.save()
            saved_contents.append(str(content.id))


        # send_content_notifications.delay(saved_contents)

        logger.info(f"Content generation completed. Generated {len(saved_contents)} pieces of content")
        return {
            "status": "success",
            "workflow_id": result["workflow_id"],
            "generated_contents": saved_contents
        }
    except Exception as e:
        logger.error(f"Error in content generation task: {str(e)}")
        return {"status": "error", "message": str(e)}

@shared_task
def publish_content_to_facebook(content_id):
    import requests
    import os

    try:
        content = GeneratedContent.objects.get(id=content_id)
        if content.published:
            return {"status": "skipped", "reason": "already_published"}

        page_id = os.environ['FACEBOOK_PAGE_ID']
        logger.info(f"page_id: {page_id}")
        page_access_token = os.environ['FACEBOOK_PAGE_TOKEN']
        logger.info(f"page_access_token: {page_access_token}")
        api_version = 'v22.0'

        # Prepare post data
        if content.content_type == 'article':
            message = f"{content.topic}\n\n{content.content}..."
            link = f"https://mydomain.com/content/{content.id}"
            post_data = {"message": message, "link": link}
            logger.info(f"post_data: {post_data}")
            payload = {
                "message": message,
                # "link": link,
                "access_token": page_access_token
                }
        else:
            payload = {
                "message": content.content,
                "access_token": page_access_token
            }
        logger.info(f"payload: {payload}")
        # Post to Facebook
        endpoint = f"https://graph.facebook.com/{api_version}/{page_id}/feed"
        
        response = requests.post(endpoint, data=payload)
        logger.info(f"response.status_code: {response.status_code} and {response.text}")

        result = response.json()
        logger.info(f"response.status_code: {response.status_code} and {response.text}")

        # Handle response
        if response.status_code == 200 and 'id' in result:
            content.published = True
            content.published_url = f"https://facebook.com/{result['id']}"
            content.save()
            return {"status": "success", "post_id": result['id'], "url": content.published_url}

        return {"status": "error", "api_response": response.text}

    except GeneratedContent.DoesNotExist:
        return {"status": "error", "message": "Content not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}



