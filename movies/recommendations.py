from django.db.models import Count, Q, Avg
from .models import Movie, Rating, UserProfile


def get_genre_recommendations(user, limit=5):
    """Get movie recommendations based on user's favorite genres"""
    try:
        favorite_genres = user.profile.favorite_genres.all()
    except UserProfile.DoesNotExist:
        return Movie.objects.none()
    
    if not favorite_genres:
        return Movie.objects.none()
    
    rated_movies = Rating.objects.filter(user=user).values_list('movie_id', flat=True)
    
    recommendations = (
        Movie.objects
        .filter(genres__in=favorite_genres)
        .exclude(id__in=rated_movies)
        .annotate(relevance=Count('genres', filter=Q(genres__in=favorite_genres)))
        .order_by('-avg_rating', '-relevance', '-release_date')[:limit]
    )
    
    return recommendations


def get_collaborative_recommendations(user, limit=5):
    """Get movie recommendations based on similar users' ratings"""
    # Get movies the user has rated highly (7+)
    user_high_ratings = Rating.objects.filter(user=user, value__gte=7)
    
    if not user_high_ratings.exists():
        return Movie.objects.none()
    
    # Find users who rated the same movies highly (6+)
    similar_users = (
        Rating.objects
        .filter(
            movie__in=user_high_ratings.values('movie'),
            value__gte=6,
        )
        .exclude(user=user)
        .values('user')
        .annotate(common_movies=Count('user'))
        .filter(common_movies__gte=1)
        .values_list('user', flat=True)
    )
    
    if not similar_users:
        return Movie.objects.none()
    
    # Get movies that similar users rated highly (7+) but user hasn't rated
    user_rated_movies = user_high_ratings.values_list('movie', flat=True)
    
    recommendations = (
        Movie.objects
        .filter(
            ratings__user__in=similar_users,
            ratings__value__gte=7
        )
        .exclude(id__in=user_rated_movies)
        .annotate(
            similar_users_count=Count('ratings__user', 
                                   filter=Q(ratings__user__in=similar_users)),
            avg_similar_rating=Avg('ratings__value', 
                                 filter=Q(ratings__user__in=similar_users))
        )
        .order_by('-similar_users_count', '-avg_similar_rating', '-avg_rating')[:limit]
    )
    
    return recommendations


def get_recommendations(user, limit=10):
    """Get combined recommendations for a user"""
    genre_recs = list(get_genre_recommendations(user, limit=limit//2))
    collab_recs = list(get_collaborative_recommendations(user, limit=limit//2))
    
    # Combine avoiding duplicates
    all_recs = genre_recs.copy()
    movie_ids = {m.id for m in all_recs}
    
    for movie in collab_recs:
        if movie.id not in movie_ids:
            all_recs.append(movie)
            movie_ids.add(movie.id)
    
    return all_recs[:limit]