# -*- -coding: utf8 -*-
from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm

register = template.Library()


# 自定义模板标签
# 访问量
@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()


# 评论量
@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    form = CommentForm(initial={
        'content_type': content_type.model,
        'object_id': obj.pk,
        'reply_comment_id': 0})
    return form


# 获得具体某篇博客列表
@register.simple_tag
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)  # 评论所用
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    return comments.order_by('-comment_time')

