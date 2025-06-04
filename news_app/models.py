from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.

class PublishedManeger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status= News.Status.Published)

class Category(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name

class News(models.Model):

    class Status(models.TextChoices):
        Draft = 'DF', 'Draft'
        Published = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    image = models.ImageField(upload_to='news/images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news' )
    publish_time = models.DateTimeField(default=timezone.now)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.Draft)

    objects = models.Manager()
    published = PublishedManeger()

    class Meta:
        ordering = ['-publish_time']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('news_detail', args=[self.slug])

class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    subject = models.CharField(max_length=150)
    website = models.CharField(max_length=150)
    message = models.TextField()

    def __str__(self):
        return self.name
    

# class Comment(models.Model):
    # name = models.CharField(max_length=120)
    # website = models.EmailField(max_lenth=150)
    # message = models.TextField()
    # posted_time = models.DateTimeField(default=timezone.now)

    # class Meta:
    #     ordering = ['posted_time']

    # def __str__(self):
    #     return self.name