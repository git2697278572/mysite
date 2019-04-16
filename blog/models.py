# coding:utf-8
from django.db import models
from django.contrib.auth.models import User  # model自己的user
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField  # 副文本编辑器
from read_statistics.models import ReadNumExpandMethod, ReadDetail  # 自己写的model


# 博客类型
class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)  # 外键表(on_delete必填项)
    content = RichTextUploadingField()  # 文章内容
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 显示后台用户名,添加修改
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True)  # 发表时间
    last_updated_time = models.DateTimeField(auto_now=True)  # 可更改的时间

    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})

    def get_email(self):
        return self.author.email

    def __str__(self):
        return "<Blog: %s>" % self.title

    class Meta:
        ordering = ['-created_time']  # 通过时间来排序

