from django.shortcuts import get_object_or_404, render  # 自定义404错误,
from django.core.paginator import Paginator  # django自带的分离器
from django.conf import settings  # 导入django自带的自定义内容
from django.db.models import Count  # 导入django自带的统计系统
from django.contrib.contenttypes.models import ContentType

from .models import Blog, BlogType
from read_statistics.utils import read_statistics_once_read  # 导入read_statistics的方法


def get_blog_list_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)  # 每10页进行分页
    page_num = request.GET.get('page', 1)  # 获取url的页面参数（GET请求）
    page_of_blogs = paginator.get_page(page_num)
    currentr_page_num = page_of_blogs.number  # 获取当前页码
    # 获取当前页码前后各2页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:  # 如果首页不为1
        page_range.insert(0, 1)  # 插入首页为1
    if page_range[-1] != paginator.num_pages:  # 同理
        page_range.append(paginator.num_pages)  # 添加

    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    # 找寻时间模块,返回时间
    context['blog_dates'] = blog_dates_dict
    return context


def blog_list(request):
    blogs_all_list = Blog.objects.all()   # 获取这个模板的全部信息
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog_list.html', context)


def blogs_with_type(request, blog_type_pk):
    # 如果查询的页面不存在,则抛出404错误
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    # 获取这个博客的全部信息
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog_with_type.html', context)


def blogs_with_date(request, year, month):
    # 获取这个博客的年月
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    return render(request, 'blogs_with_date.html', context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)

    context = {}
    # pk 主键
    # 时间找到当前博客的上所有博客 last最后一条
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    # 时间找到当前博客的所有博客 first第一条
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] = blog
    response = render(request, 'blog_detail.html', context)  # 响应
    response.set_cookie(read_cookie_key, 'true')  # 阅读cookie标记
    return response
