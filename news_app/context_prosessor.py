from .models import News, Comments

def latest_news(request):
    latest_news = News.published.all().order_by('-publish_time')[:2]
    context = {
        'latest_news': latest_news
    }

    return context

def latest_comments(request):
    latest_comments = Comments.objects.filter(active=True).order_by('-created_time')[:3]
    context = {
        'latest_comments': latest_comments
    }
    return context

