from .models import GeneratedContent
from .langchain_orchestrator import ContentWorkflow
from celery import shared_task
from django.conf import settings
import logging
import json
from .models import GeneratedContent, User, Notification
from fcm_django.models import FCMDevice

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
def send_content_notifications(content_ids):

    try:
        for content_id in content_ids:
            content = GeneratedContent.objects.get(id=content_id)

            users = User.objects.filter(profile_reveive_notifications=True)

            for user in users:

                notification = Notification.objects.create(
                    user=user,
                    content=content
                )

                devices = FCMDevice.objects.filter(user=user)
                if devices.exists():
                    devices.send_message(
                        title=f"New Content: {content.topic}",
                        body=f"New {content.content_type} is available for voting",
                        data={
                            "content_id": str(content.id),
                            "notification_id": str(notification.id),
                            "type": "new_content"
                        }
                    )
        
        return {"status": "success", "notified_users": users.count()}
    except Exception as e:
        logger.error(f"Error sending notifications: {str(e)}")
        return {"status": "error", "message": str(e)}


@shared_task
def generate_content_task():

    logger.info("Starting scheduled content generation workflow")

    try:
        workflow = ContentWorkflow()
        result = workflow.run_content_workflow()


        saved_contents = []

        for content_data in result.get("contents_generated"):
            content = GeneratedContent(
                topic=content_data["topic"],
                content_type=content_data["content_type"],
                content=content_data["content"],
                metadata=content_data["metadata"]
            )
            content.save()
            saved_contents.append(str(content.id))


        send_content_notifications.delay(saved_contents)

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

        page_id = os.environ.get('FACEBOOK_PAGE_ID')
        access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
        api_version = 'v22.0'

        if content.content_type == 'article':

            message = f"{content.topic}\n\n{content.content[:200]}..."
            url = f"https://mydomain.com/content/{content.id}"

            post_data = {
                "message": message,
                "link": url
            }
        else:

            post_data = {
                "message": content.content
            }

        endpoint = f"https://graph.facebook.com/{api_version}/{page_id}/feed"
        params = {
            "access_token": access_token,
            **post_data
        }

        response = requests.post(endpoint, params=params)
        result = response.json()

        if response.status_code == 200 and 'id' in result:

            content.published = True
            content.published_url = f"https://facebook.com/{result['id']}"
            content.save()

            return {
                "status": "success",
                "post_id": result['id'],
                "url": content.published_url
            }

        else:
            logger.error(f"Facebook API error: {response.text}")
            return {"status": "error", "api_response": response.text}
    
    except Exception as e:
        logger.error(f"Error publishing to Facebook: {str(e)}")
        return {"status": "error", "message": str(e)}


# def main():
    
#     generate_content_task()

# if __name__ == "__main__":
#     main()
