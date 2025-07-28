from django.shortcuts import redirect
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView, DetailView


PER_PAGE = 9

class PostListView(ListView):
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE

    queryset = Post.objects.get_published()

    def get_context_data(self, **kwargs):

        contexto = super().get_context_data(**kwargs)

        contexto.update({
            'page_title': 'Home - '
        })

        return contexto


class CreatedByListView(PostListView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._temp_context = dict()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        author = self._temp_context['author']

        author_full_name = author.username
        if author.first_name:
            author_full_name = f'{author.first_name} {author.last_name}'
        
        page_title = f'Posts de {author_full_name} - '
        
        ctx.update({
            'page_title': page_title
        })

        return ctx
    
    def get_queryset(self):
        qs = super().get_queryset()

        qs = qs.filter(created_by__pk=self._temp_context['author_pk'])
        return qs
    
    
    

    def get(self, request, *args, **kwargs):
        
        author_pk = self.kwargs['author_pk']
        author = User.objects.filter(pk=author_pk).first()

        if author is None:
            raise Http404()

        self._temp_context.update({
            'author_pk': author_pk,
            'author': author,
        })

        return super().get(request, *args, **kwargs)
    


class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self):
        return super().get_queryset().filter(category__slug=self.kwargs.get('slug'))
    
    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)

        page_title = self.object_list[0].category.name

        ctx.update({
            'page_title': f'{page_title} - Categoria - ',
        })

        return ctx
    

class TagListView(PostListView):
    def get_queryset(self):
        
        return super().get_queryset().filter(tags__slug=self.kwargs['slug'])
    
    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)
     
        page_title = f'{self.object_list[0].tags.filter(slug=self.kwargs['slug']).first().name} - Tag - '

        ctx.update({
            'page_title': page_title,
        })

        return ctx

class PageDetailView(DetailView):
    model = Page
    template_name = 'blog/pages/page.html'
    slug_field = 'slug'
    context_object_name = 'page'

    def get_context_data(self, *args, **kwargs):
        
        ctx = super().get_context_data(*args, **kwargs)
        page = self.get_object()

        page_title = f'{page.title} - Página - '

        ctx.update({
            'page_title': page_title,
        })

        return ctx
    
    def get_queryset(self):

        return super().get_queryset().filter(is_published=True)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/pages/post.html'
    slug_field = 'slug'
    context_object_name = 'post'

    def get_queryset(self):
        qs = super().get_queryset().filter(is_published=True)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        post = self.get_object()
        
        page_title = f'{post.title} - Post - '

        ctx.update({
            'page_title': page_title,
        })

        return ctx


class SearchListView(PostListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._search_value = ''

    def setup(self, request, *args, **kwargs):
        
        self._search_value = request.GET.get('search', '').strip()

        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        
        search_value = self._search_value

        qs = super().get_queryset().filter(
            Q(title__icontains=search_value) |
            Q(excerpt__icontains=search_value) |
            Q(content__icontains=search_value)
        )[:PER_PAGE]

        return qs
    
    def get_context_data(self, *args, **kwargs):

        ctx = super().get_context_data(*args, **kwargs)
        search_value = self._search_value
        page_title = f'{search_value[:30]} - Search - '

        ctx.update({
            'page_title': page_title,
            'search_value': search_value,
        })

        return ctx
    
    def get(self, request, *args, **kwargs):

        if self._search_value == '':
            return redirect('blog:index')

        return super().get(request, *args, **kwargs)