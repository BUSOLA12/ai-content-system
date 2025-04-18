from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import GeneratedContent, Vote, Notification
import json
from django.contrib.auth.forms import UserCreationForm





def home(request):

    contents = GeneratedContent.objects.order_by('-created_at')[:10]
    return render(request, 'ai_content/home.html', {'contents': contents})

@login_required
def content_detail(request, content_id):

    content = get_object_or_404(GeneratedContent, id=content_id)
    user_vote = None

    if request.user.is_authenticated:
        try:
            user_vote = Vote.objects.get(user=request.user, content=content).vote

        except Vote.DoesNotExist:
            pass
    return render(request, 'ai_content/content_detail.html', {'content': content, 'user_vote': user_vote})

@login_required
def notifications(request):

    notifications = Notifications.objects.filter(user=request.user).oreder_by('-created_at')
    if request.GET.get('mark_read'):
        notifications.update(read=True)

    return render(request, 'ai_content/notifications.html', {'notifications': notifications})

@login_required
def dashboard(request):
    user_votes = Vote.objects.filter(user=request.user).order_by('-created_at')
    unread_notifications = Notification.objects.filter(user=request.user, read=False).count()

    return render(request, 'ai_content/dashboard.html', {'user_vote': user_votes, 'unread_notifications': unread_notifications})

@login_required
@require_POST
def update_profile(request):
    profile = request.user.profile
    profile.receive_notification = 'reveive_notifications' in request.POST
    profile.save()

    messages.success(request, "Your settings have been update.")
    return redirect('dashboard')

def api_vote_content(request, content_id):
    return vote_content(request, content_id)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            profile = user.profile
            profile.receive_notifications = 'receive_notifications' in request.POST

            login(request, user)
            messages.success(request, "Registration successful! Welcome to AI Content Generator.")
            return redirect('home')

    else:
        form = UserCreationForm()
    return render(request, 'ai_content/reqister.html', {'form': form})
@login_required
@require_POST
def vote_content(request, content_id):

    content = get_object_or_404(GeneratedContent, id=content_id)
    vote_type = request.POST.get('vote')

    if vote_type not in ['approve', 'reject']:
        return JsonResponse({"status": "error", "message": "Invalid vote type"})

    vote, created = Vote.objects.update_or_create(
        user=request.user,
        content=content,
        defaults={'vote': vote_type}
    )

    Notification.objects.filter(user=request.user, content=content).update(read=True)


    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            "status": "success",
            "vote": vote_type,
            "approved_count": content.approved_count,
            "rejected_count": content.rejected_count
            }
        )

    else:
        message.success(request, f"Your vote has been recorded: {vote_type}")
        return redirect('content_detail', content_id=content_id)

