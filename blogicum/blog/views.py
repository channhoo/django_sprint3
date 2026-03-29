from django.shortcuts import render
from django.http import Http404
from django.utils import timezone
from .models import Post, Category


def index(request):
    """Главная страница - 5 последних публикаций"""
    post_list = Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    ).order_by('-pub_date')[:5]
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, post_id):
    """Страница отдельной публикации"""
    try:
        post = Post.objects.get(
            id=post_id,
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )
    except Post.DoesNotExist:
        raise Http404("Публикация не найдена")
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    """Страница категории"""
    try:
        category = Category.objects.get(
            slug=category_slug,
            is_published=True
        )
    except Category.DoesNotExist:
        raise Http404("Категория не найдена")
    
    post_list = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')
    
    return render(
        request, 
        'blog/category.html', 
        {'category': category, 'post_list': post_list}
    )
