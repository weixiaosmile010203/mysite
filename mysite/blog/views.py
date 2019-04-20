from django.shortcuts import render_to_response, get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator


def blog_list(request):
    page_num = request.GET.get('page', 1)  # 获取URL的页面参数（GET请求）得到页码
    blogs_all_list = Blog.objects.all()  # 获取所有博客
    paginator = Paginator(blogs_all_list, 10)  # 多所有的博客进行分页，每10篇分为一页
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
    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog_list.html', context)


def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
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
    context['blogs'] = blogs_all_list
    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()
    return render_to_response('blog_with_type.html', context)
