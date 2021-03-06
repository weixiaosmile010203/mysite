from django.shortcuts import render_to_response, get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator
from django.db.models import Count


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

    # 博客日期分类中的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_dates_dict[blog_date] = Blog.objects.filter(created_time__year=blog_date.year,
                                                         created_time__month=blog_date.month).count()

    context = {}
    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict
    return render_to_response('blog_list.html', context)


def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    if not request.COOKIES.get(str(blog_pk)):
        blog.read_num += 1
        blog.save()
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    response = render_to_response('blog_detail.html', context)
    response.set_cookie('%s' % blog_pk, True)
    print(response)
    return response


def blog_with_type(request, blog_type_pk):
    context = {}
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
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_dates_dict[blog_date] = Blog.objects.filter(created_time__year=blog_date.year,
                                                         created_time__month=blog_date.month).count()

    context['blog_type'] = blog_type
    context['blogs'] = blogs_all_list
    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict
    return render_to_response('blog_with_type.html', context)


def blog_with_date(request, year, month):
    context = {}
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    paginator = Paginator(blogs_all_list, 10)
    page_num = request.GET.get('page', 1)  # 获取URL的页面参数（GET请求）
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

    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_dates_dict[blog_date] = Blog.objects.filter(created_time__year=blog_date.year,
                                                         created_time__month=blog_date.month).count()

    context['blogs'] = blogs_all_list
    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_with_date'] = "%s年%s月" % (year, month)
    context['blog_dates'] = blog_dates_dict
    return render_to_response('blog_with_date.html', context)