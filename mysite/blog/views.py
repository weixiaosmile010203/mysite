from django.shortcuts import render_to_response, get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator


def blog_list(request):
    page_num = int(request.GET.get('page', 1))#获取URL的页面参数（GET请求）
    blogs_all_list = Blog.objects.all()
    paginator = Paginator(blogs_all_list, 10)
    page_of_blogs = paginator.get_page(page_num)
    if paginator.num_pages > 7:
        if page_num - 3 < 1:
            page_ran = range(1, 8)
        elif page_num + 3 > paginator.num_pages:
            page_ran = range(paginator.num_pages - 6, paginator.num_pages + 1)
        else:
            page_ran = range(page_num - 3, page_num + 4)
        page_range = page_ran
    else:
        page_range = paginator.page_range
    context = {}
    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog_list.html', context)


def blog_detail(request, blog_pk):
    context = {}
    context['blog'] = get_object_or_404(Blog, pk=blog_pk)
    return render_to_response('blog_detail.html', context)


def blog_with_type(request, blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    context['blog_type'] = blog_type
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog_with_type.html', context)

