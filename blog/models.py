from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Comic(models.Model):
title = models.CharField(max_length=200)
description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='comics')

    # --- THÊM DÒNG NÀY ĐỂ LÀM THEO DÕI ---
    followers = models.ManyToManyField(User, related_name='followed_comics', blank=True)

    def __str__(self):
        return self.title

    @property
    def latest_chapter_number(self):
        latest_chapter = self.chapters.order_by('-chapter_number').first()
        return latest_chapter.chapter_number if latest_chapter else None

class Chapter(models.Model):
    comic = models.ForeignKey(Comic, related_name='chapters', on_delete=models.CASCADE)
    chapter_number = models.FloatField()
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['chapter_number']

class Tag(models.Model):
name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    PLAN_CHOICES = [('free', 'Free'), ('pro', 'Pro'), ('premium', 'Premium')]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    plan_expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - {self.plan}"

class Subscription(models.Model):
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('pro', 'Pro - 49,000đ/tháng'),
        ('premium', 'Premium - 99,000đ/tháng'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.user.username} - {self.plan}"
    @property
    def is_expired(self):
        return self.expires_at and timezone.now() > self.expires_at
