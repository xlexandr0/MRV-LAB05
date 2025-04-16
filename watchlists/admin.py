from django.contrib import admin
from .models import Watchlist, WatchlistItem

class WatchlistItemInline(admin.TabularInline):
    model = WatchlistItem
    extra = 1
    raw_id_fields = ('movie',)

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'privacy', 'updated_at')
    list_filter = ('privacy', 'updated_at')
    search_fields = ('name', 'owner__username', 'description')
    inlines = [WatchlistItemInline]
    filter_horizontal = ('collaborators',)
    raw_id_fields = ('owner',)

@admin.register(WatchlistItem)
class WatchlistItemAdmin(admin.ModelAdmin):
    list_display = ('movie', 'watchlist', 'status', 'priority', 'updated_at')
    list_filter = ('status', 'priority')
    search_fields = ('movie__title', 'watchlist__name')
    raw_id_fields = ('movie', 'watchlist')