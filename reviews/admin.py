from django.contrib import admin
from .models import Review, ReviewVote, ReviewComment, Badge, UserBadge

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'overall_rating', 'created_at')
    list_filter = ('overall_rating', 'created_at')
    search_fields = ('movie__title', 'user__username', 'content')
    raw_id_fields = ('movie', 'user')

@admin.register(ReviewVote)
class ReviewVoteAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'helpful', 'created_at')
    list_filter = ('helpful',)
    raw_id_fields = ('review', 'user')

@admin.register(ReviewComment)
class ReviewCommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'user', 'created_at')
    search_fields = ('content',)
    raw_id_fields = ('review', 'user')

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'awarded_at')
    list_filter = ('badge',)
    raw_id_fields = ('user', 'badge')