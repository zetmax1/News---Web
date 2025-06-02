from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import News, Category
from .forms import ContactForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
import random
# Create your views here.

def news_list(request):
    news_list = News.objects.all()
    context = {
        'news_list': news_list,
    }

    return render(request, 'news/news_list.html', context=context)

def news_detail(request, news):
    news = get_object_or_404(News, slug=news)
    categories = Category.objects.all()
    lastest_news = News.published.all().order_by('-publish_time')[:5]
    context = {
        'news': news,
        'latest_news': lastest_news,
        'categories': categories,
    }

    return render(request, 'news/news_detail.html', context=context)

def homePageView(request):
    first_news = News.published.all().order_by('-publish_time')[:1]
    news_list = News.published.all().order_by('-publish_time')[1:5]
    sport_news = News.published.filter(category__name='sport').order_by('-publish_time')[:4]
    world_news = News.published.filter(category__name='world').order_by('-publish_time')[:4]
    local_news = News.published.filter(category__name='local').order_by('-publish_time')[:4]
    technology_news = News.published.filter(category__name='technology').order_by('-publish_time')[:4]
    second_news_list = News.published.all().order_by('-publish_time')[5:9]
    third_news_list = News.published.all().order_by('-publish_time')[1:3]
    categories = Category.objects.all()
    context = {
        'news_list': news_list,
        'sport_news': sport_news,
        'world_news': world_news,
        'local_news': local_news,
        'technology_news': technology_news,
        'categories': categories,
        'first_news': first_news,
        'second_news_list': second_news_list,
        'third_news_list': third_news_list,

    }

    return render(request, 'news/index.html', context=context)


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
    

class NewsUpdateView(UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'status', )
    template_name = 'crud/news_update.html'

class NewsDeleteView(DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')