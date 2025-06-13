from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import GeneratedContent, UserProfile
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',  # Log messages will be saved to 'app.log'
    filemode='a'  # Append to the log file instead of overwriting
)
logger = logging.getLogger(__name__)

def sendHtmlEmail(subject, to_emails, template_name, context):

    html_content = render_to_string(template_name, context)

    text_content = context.get('plain_text', 'This is a plain text version of the email.')

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to_emails,
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)




@receiver(post_save, sender=GeneratedContent)
def handleGeneratedContentSignals(sender, instance, created, **kwargs):
    logger.info("Send email Worked!")

    Users = UserProfile.objects.all()
    User_emails = [user.user.email for user in Users if user.user.email]
    logger.info(f"Users email: {User_emails}")

    if created:

        sendHtmlEmail(
                subject='The content with topic "{previous.topic}" has been created. Please login and vote',
                to_emails=User_emails,
                template_name='ai_content/New_content.html',
                context={
                    'content_type': instance.content_type,
                    'content_topic': instance.topic,
                    'plain_text': f'The content with the topic "{instance.topic}" has been created. Please login and vote',
                }

            )

    else:
        previous = GeneratedContent.objects.get(pk=instance.pk)

        if previous.published:
            sendHtmlEmail(
                subject='The content with topic "{previous.topic}" has been published',
                to_emails=User_emails,
                template_name='ai_content/Content_Published.html',
                context={
                    'content_type': instance.content_type,
                    'content_topic': instance.topic,
                    'plain_text': f'The content with the topic "{instance.topic}" has been published.',
                }

            )

        if not previous.published and previous.rejected_count > previous.approved_count:
            sendHtmlEmail(
                subject='The content with topic "{previous.topic}" has been rejected',
                to_emails=User_emails,
                template_name='ai_content/Content_Rejected.html',
                context={
                    'content_type': instance.content_type,
                    'content_topic': instance.topic,
                    'plain_text': f'The content with the topic "{instance.topic}" has been rejected.',
                }

            )