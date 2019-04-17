from django.shortcuts import render_to_response, get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator


def blog_list(request):
    page_num = request.GET.get('page', 1)#获取URL的页面参数（GET请求）
    blogs_all_list = Blog.objects.all()
    paginator = Paginator(blogs_all_list, 10)
    page_of_blogs = paginator.get_page(page_num)
    currentr_page_num = page_of_blogs.number
    if paginator.num_pages > 7:
        if currentr_page_num - 3 < 1:
            page_ran = range(1, 8)
        elif currentr_page_num + 3 > paginator.num_pages:
            page_ran = range(paginator.num_pages - 6, paginator.num_pages + 1)
        else:
            page_ran = range(currentr_page_num - 3, currentr_page_num + 4)
        page_range = list(page_ran)
    else:
        page_range = list(paginator.page_range)

    if page_range[0] -1 > 1:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] > 1:
        page_range.append('...')

    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

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
    page_num = request.GET.get('page', 1)  # 获取URL的页面参数（GET请求）
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    paginator = Paginator(blogs_all_list, 10)
    page_of_blogs = paginator.get_page(page_num)
    currentr_page_num = page_of_blogs.number
    if paginator.num_pages > 7:
        if currentr_page_num - 3 < 1:
            page_ran = range(1, 8)
        elif currentr_page_num + 3 > paginator.num_pages:
            page_ran = range(paginator.num_pages - 6, paginator.num_pages + 1)
        else:
            page_ran = range(currentr_page_num - 3, currentr_page_num + 4)
        page_range = list(page_ran)
    else:
        page_range = list(paginator.page_range)

    if page_range[0] - 1 > 1:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] > 1:
        page_range.append('...')

    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['blog_type'] = blog_type
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog_with_type.html', context)

