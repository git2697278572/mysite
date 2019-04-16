import datetime
from django.contrib.contenttypes.models import ContentType   # 导入django自带的库
from django.utils import timezone
from django.db.models import Sum   # 求和
from .models import ReadNum, ReadDetail


# 博客阅读数
def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)

    if not request.COOKIES.get(key):
        # 总阅读数 +1
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        # 当天阅读数 +1
        date = timezone.now().date()
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num += 1
        readDetail.save()
    return key


# 找寻7天的数据浏览量
def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7, 0, -1):   # 找寻7天的值
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))  # 将date格式化
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)  # 如果没有则显示为0
    return dates, read_nums


# 找寻24小时的数据浏览量
def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    return read_details[:7]   # 只显示7条数据


# 获取昨天的浏览数据
def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return read_details[:7]