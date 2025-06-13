# AI Content System

Welcome to the **AI Content System**, a Django-based application designed to automate content generation, voting, and publishing workflows. This system leverages AI-powered tools to create engaging content, allows users to vote on its quality, and publishes approved content to social media platforms like Facebook.

## Features

### Content Generation

- Automatically generates content based on trending topics using AI models.
- Supports multiple content formats, including articles, social media posts, and video scripts.

### Voting System

- Registered users can vote to approve or reject generated content.
- Tracks approval and rejection counts for each piece of content.

### Publishing Workflow

- Automatically publishes approved content to Facebook once it meets the required approval threshold.
- Includes metadata such as word count, AI model used, and generation timestamp.

### Notifications

- Sends email notifications to users about new content, published content, and rejected content.
- Displays notifications in the user dashboard.

### User Dashboard

- Provides an overview of user activity, including votes, notifications, and account settings.
- Displays content statistics and voting distribution charts.

### Admin Panel

- Manage users, content, and notifications through the Django admin interface.

## Technologies Used

- **Backend**: Django 5.2
- **Frontend**: Bootstrap 5
- **Database**: SQLite (default, can be switched to PostgreSQL)
- **Task Queue**: Celery with Redis as the broker
- **AI Integration**: LangChain and Together API
- **Social Media API**: Facebook Graph API
- **Email Notifications**: SMTP (Gmail)

## Installation

### Prerequisites

- Python 3.10 or higher
- Docker (optional for containerized deployment)
- Redis (for Celery task queue)

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ai-content-system.git
   cd ai-content-system
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:

   - Create a `.env` file in the project root.
   - Add the following variables:
     ```env
     DJANGO_SECRET_KEY=your_secret_key
     DEBUG=True
     NEWS_API_KEY=your_news_api_key
     TOGETHER_API_KEY=your_together_api_key
     FACEBOOK_PAGE_ID=your_facebook_page_id
     FACEBOOK_PAGE_TOKEN=your_facebook_page_token
     EMAIL_HOST_USER=your_email@gmail.com
     EMAIL_HOST_PASSWORD=your_email_password
     ```

5. Apply migrations:

   ```bash
   python manage.py migrate
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000`.

## Docker Deployment

1. Build and start the containers:

   ```bash
   docker-compose up --build
   ```

2. Access the application at `http://localhost:8000`.

## Usage

### User Workflow

1. **Register/Login**: Create an account or log in to access the dashboard.
2. **Vote on Content**: Approve or reject AI-generated content.
3. **View Notifications**: Stay updated on new content and publishing status.
4. **Dashboard**: Monitor your activity and update account settings.

### Admin Workflow

1. **Manage Content**: View and edit generated content.
2. **Monitor Votes**: Track voting statistics for each piece of content.
3. **Publish Content**: Ensure approved content is published to Facebook.

## Project Structure

```
ai_content_system/
├── accounts/                # User management app
├── content_generator/       # Core app for content generation and voting
├── ai_content_system/       # Project settings and configurations
├── templates/               # HTML templates for the frontend
├── staticfiles/             # Static assets (CSS, JS, images)
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
├── requirements.txt         # Python dependencies
└── manage.py                # Django management script
```

## Contributing

We welcome contributions to improve the AI Content System! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For questions or support, please contact:

- **Email**: iyiolaolubusola@gmail.com
- **GitHub**: [yourusername](https://github.com/yourusername)

---

Thank you for using the AI Content System! 🚀
