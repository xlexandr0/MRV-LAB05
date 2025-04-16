from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie

class Watchlist(models.Model):
    PRIVACY_CHOICES = [
        ('PR', 'Private'),
        ('FR', 'Friends Only'),
        ('PU', 'Public'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlists')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    privacy = models.CharField(max_length=2, choices=PRIVACY_CHOICES, default='PR')
    collaborators = models.ManyToManyField(User, related_name='collaborative_watchlists', blank=True)
    
    class Meta:
        ordering = ['-updated_at']
        unique_together = ('owner', 'name')
    
    def __str__(self):
        return f"{self.owner.username}'s {self.name}"

class WatchlistItem(models.Model):
    STATUS_CHOICES = [
        ('WT', 'Want to Watch'),
        ('WG', 'Watching'),
        ('WD', 'Watched'),
    ]
    
    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]
    
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name='items')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='WT')
    priority = models.PositiveSmallIntegerField(choices=PRIORITY_CHOICES, default=2)
    notes = models.TextField(blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['priority', '-added_at']
        unique_together = ('watchlist', 'movie')
    
    def __str__(self):
        return f"{self.movie.title} in {self.watchlist.name}"