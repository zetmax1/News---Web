import slugify

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaulttags import comment, querystring
from .models import News, Category
from .forms import ContactForm, CommentsForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
import random
from news_project.costum_permessions import OnlyLoggedSuperUsers
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.text import slugify
# from hitcount.models import HitCountMixin, get_hitcount_model
# from hitcount.views import HitCountDetailView

def news_detail(request, news):
    news = get_object_or_404(News, slug=news)
    # context = {}
    # hit_count = get_hitcount_model().objects.get_for_object(news)
    # hits = hit_count.hits
    # hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    # hit_count_response = HitCountMixin.hit_count(request, hit_count)
    # if hit_count_response.hit_counted:
    #     hits += 1
    #     hitcontext['hitcounted'] = hit_count_response.hit_counted
    #     hitcontext['hit_message'] = hit_count_response.hit_message
    #     hitcontext['total_hits'] = hits

    categories = Category.objects.prefetch_related('news').all()
    lastest_news = News.published.all().order_by('-publish_time')[:5]
    shuffle_news = list(News.published.all())
    random.shuffle(shuffle_news)
    comments = news.comments.filter(active= True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentsForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            return redirect('news_detail', news=news.slug)
    else:
        comment_form = CommentsForm()
    comment_count = comments.count()
    context = {
        'news': news,
        'latest_news': lastest_news,
        'categories': categories,
        'shuffle_news': shuffle_news,
        'comment_form': comment_form,
        'comments': comments,
        'new_comment': new_comment,
        'comment_count': comment_count,
    }

    return render(request, 'news/news_detail.html', context=context)

# def homePageView(request):
#     first_news = News.published.all().order_by('-publish_time')[:1]
#     news_list = News.published.all().order_by('-publish_time')[1:5]
#     sport_news = News.published.filter(category__name='sport').order_by('-publish_time')[:4]
#     world_news = News.published.filter(category__name='world').order_by('-publish_time')[:4]
#     local_news = News.published.filter(category__name='local').order_by('-publish_time')[:4]
#     technology_news = News.published.filter(category__name='technology').order_by('-publish_time')[:4]
#     second_news_list = News.published.all().order_by('-publish_time')[5:9]
#     third_news_list = News.published.all().order_by('-publish_time')[1:3]
#     categories = Category.objects.all()
#     context = {
#         'news_list': news_list,
#         'sport_news': sport_news,
#         'world_news': world_news,
#         'local_news': local_news,
#         'technology_news': technology_news,
#         'categories': categories,
#         'first_news': first_news,
#         'second_news_list': second_news_list,
#         'third_news_list': third_news_list,

#     }

#     return render(request, 'news/index.html', context=context)


class HomePageView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:5]
        context['sport_news'] = News.published.filter(category__name='sport').order_by('-publish_time')[:4]
        context['world_news'] = News.published.filter(category__name='world').order_by('-publish_time')[:4]
        context['local_news'] = News.published.filter(category__name='local').order_by('-publish_time')[:4]
        context['technology_news'] = News.published.filter(category__name='technology').order_by('-publish_time')[:4]
        context['second_news_list'] = News.published.all().order_by('-publish_time')[5:9]
        context['third_news_list'] = News.published.all().order_by('-publish_time')[1:3]
        context['news_list_3'] =  News.published.all().order_by('-publish_time')[:3]
        return context

# def contactPageView(request):
#     form = ContactForm(request.POST or None)
#     if request.method == "POST" and form.is_valid():
#         form.save()
#         return HttpResponse('<h2> Thanks for contacting us')

#     context = {
#         'form': form,
#     }
#     return render(request, 'news/contact.html', context=context)

class ContactPageView(TemplateView):
    template_name = 'news/contact.html'
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form,
        }
        return render(request, 'news/contact.html', context)
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponse('<h2><i> Thanks for contacting us </i></h2>')
        context = {
                'form': form,
        }
        return render(request, 'news/contact.html', context)
    

class LocalNewsView(ListView):
    model = News
    template_name = 'news/local_news.html'
    context_object_name = 'local_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="local")[:10]
        return news
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shuffle_list = list(context['local_news'])[:15]
        random.shuffle(shuffle_list)
        context['shuffle_news'] = shuffle_list

        return context
    

    
class ForeignNewsView(ListView):
    model = News
    template_name = 'news/world_news.html'
    context_object_name = 'world_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="world")
        return news
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shuffle_news = list(context['world_news'])
        random.shuffle(shuffle_news)
        context['shuffle_news'] = shuffle_news

        return context
    
class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/technology_news.html'
    context_object_name = 'technology_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="technology")
        return news   
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shuffle_news = list(context['technology_news'])
        random.shuffle(shuffle_news)
        context['shuffle_news'] = shuffle_news

        return context
    

class SportNewsView(ListView):
    model = News
    template_name = 'news/sport_news.html'
    context_object_name = 'sport_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name="sport")
        return news
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shuffle_news = list(context['sport_news'])
        random.shuffle(shuffle_news)
        context['shuffle_news'] = shuffle_news

        return context
    

class NewsUpdateView(OnlyLoggedSuperUsers, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'status', )
    template_name = 'crud/news_update.html'

class NewsDeleteView(OnlyLoggedSuperUsers, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(OnlyLoggedSuperUsers, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ['title', 'body','image', 'category', 'publish_time', 'status']  # Slugni ko'rsatmang

    def form_valid(self, form):
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

@login_required()
@user_passes_test(lambda u: u.is_superuser)
def admin_page_view(request):
    admins_list = User.objects.all().filter(is_superuser=True)
    context = {
        'admins_list': admins_list,
    }
    return render(request, 'pages/admin_page.html', context)

class SearchResultsView(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return News.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
        return News.objects.none()
