import os
import django
import sys

from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_content_system.settings')  

django.setup()

from content_generator.models import GeneratedContent
from content_generator.tasks import publish_content_to_facebook, generate_content_task


def main():
    
    contents = GeneratedContent.objects.all()
    content_ids = [item.id for item in contents]
    content_id = content_ids[0]
    publish_content_to_facebook(content_id)

    # generate_content_task()

if __name__ == "__main__":
    main()