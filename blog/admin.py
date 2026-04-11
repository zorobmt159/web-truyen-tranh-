from django.contrib import admin
from .models import Comic, Chapter, Tag, UserProfile, Subscription

# --- Inline Chapter trong trang Comic ---
class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1
    fields = ('chapter_number', 'title', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('chapter_number',)

@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    list_display = ('title', 'views', 'likes', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('tags', 'created_at')
    inlines = [ChapterInline]

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('comic', 'chapter_number', 'title', 'created_at')
    list_filter = ('comic',)
    search_fields = ('comic__title', 'title')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'plan_expires_at', 'created_at')
    list_filter = ('plan',)
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'started_at', 'expires_at', 'is_active', 'is_expired')
    list_filter = ('plan', 'is_active')
    search_fields = ('user__username',)
    readonly_fields = ('started_at',)
