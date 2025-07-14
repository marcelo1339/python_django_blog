from django.db import models
from utils.rands import slugify_new
from utils.images import resize_image
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, default=None, null=True, blank=True)


    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify_new(self.name, 4)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, default=None, null= True, blank=True, max_length=255,)

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify_new(self.name, 4)
        
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Page(models.Model):
    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    title = models.CharField(max_length=65,)
    slug = models.SlugField(unique=True, default=None, null= True, blank=True, max_length=255,)
    is_published = models.BooleanField(
        default=False,
        help_text='Marque para a página ficar visível públicamente.'
    )
    content = models.TextField()
    
    
    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify_new(self.title, 4)
        
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    title = models.CharField(max_length=65,)
    slug = models.SlugField(unique=True, default='', null=False, blank=True, max_length=255)
    exerpt = models.CharField(max_length=150)
    is_published = models.BooleanField(
        default=False,
        help_text='Marque para o post ficar visível públicamente.'
    )
    content = models.TextField()
    cover = models.ImageField(upload_to='posts/%Y/%m/', blank=True, default='',)
    cover_in_post_content = models.BooleanField(
        default=True,
        help_text='Exibir a imagem de capa também dentro do conteúdo do post?'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='post_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='post_updated_by')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None,
    )
    tags = models.ManyToManyField(Tag, blank=True, default='')

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify_new(self.title, 4)
    
        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)

        cover_changed = False

        if self.cover:
            # print(">>current_cover_name", current_cover_name)
            # print("")
            # print(">>self.cover.name", self.cover.name)
            cover_changed = current_cover_name != self.cover.name
            # print(">>cover_changed", cover_changed)

        if cover_changed:
            # print(">>>>>>>>>>Cai no Cover Changed")
            resize_image(self.cover, 900, True, 70)

        return super_save