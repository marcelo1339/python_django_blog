from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404

PER_PAGE = 9

def index(request):

    posts = Post.objects.get_published()       

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': 'Home - '
        }
    )

def created_by(request, author_pk):

    author = User.objects.filter(pk=author_pk).first()

    if author is None:
        raise Http404()

    author_full_name = author.username

    if author.first_name:
        author_full_name = f'{author.first_name} {author.last_name}'

    page_title = f'Posts de {author_full_name} - '

    posts = Post.objects.get_published().filter(created_by__pk=author_pk)     

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )

def category(request, slug):

    posts = Post.objects.get_published().filter(category__slug=slug)

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    if len(page_obj) == 0:
        raise Http404()
    
    page_title = f'{page_obj[0].category.name} - Categoria - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )

def tag(request, slug):

    posts = Post.objects.get_published().filter(tags__slug=slug)     

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404()
    
    page_title = f'{page_obj[0].tags.filter(slug=slug).first().name} - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title,
        }
    )

def page(request, slug):

    requested_page = Page.objects.get_published().filter(slug=slug).first()

    if requested_page is None:
        raise Http404()

    page_title = f'{requested_page.title} - Página - '
    return render(
        request,
        'blog/pages/page.html',
        {
            'page': requested_page,
            'page_title': page_title,
        }
    )


def post(request, slug):

    requested_post = (
        Post.objects
        .get_published()
        .filter(slug=slug)
        .first()
    )

    if requested_post is None:
        raise Http404()
    
    page_title = f'{requested_post.title} - Post - '

    return render(
        request,
        'blog/pages/post.html',
        {
           'post': requested_post,
            'page_title': page_title,
        }
    )

def search(request):
    search_value = request.GET.get('search', '').strip()
    posts = (
        Post.objects.get_published()
        .filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value) 
        )[:PER_PAGE]
    )

    page_title = f'{search_value[:30]} - Search - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value': search_value,
            'page_title': page_title,
        }
    )