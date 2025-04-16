from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from movies.models import Movie
from .models import Review, ReviewVote, ReviewComment
from .forms import ReviewForm, ReviewCommentForm, ReviewVoteForm

@login_required
def movie_reviews(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    reviews = Review.objects.filter(movie=movie).select_related('user').prefetch_related('votes', 'comments')
    return render(request, 'reviews/movie_reviews.html', {
        'movie': movie,
        'reviews': reviews,
    })

@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    if Review.objects.filter(movie=movie, user=request.user).exists():
        messages.warning(request, "You've already reviewed this movie!")
        return redirect('reviews:movie_reviews', movie_id=movie.id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            messages.success(request, "Review added successfully!")
            return redirect('reviews:movie_reviews', movie_id=movie.id)
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/add_review.html', {
        'form': form,
        'movie': movie,
    })

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Review updated successfully!")
            return redirect('reviews:movie_reviews', movie_id=review.movie.id)
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'reviews/edit_review.html', {
        'form': form,
        'review': review,
    })

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    movie_id = review.movie.id
    review.delete()
    messages.success(request, "Review deleted successfully!")
    return redirect('reviews:movie_reviews', movie_id=movie_id)

@login_required
def review_vote(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    existing_vote = ReviewVote.objects.filter(review=review, user=request.user).first()
    
    if request.method == 'POST':
        form = ReviewVoteForm(request.POST)
        if form.is_valid():
            if existing_vote:
                existing_vote.helpful = form.cleaned_data['helpful']
                existing_vote.save()
            else:
                ReviewVote.objects.create(
                    review=review,
                    user=request.user,
                    helpful=form.cleaned_data['helpful']
                )
            messages.success(request, "Vote submitted!")
            return redirect('reviews:movie_reviews', movie_id=review.movie.id)
    else:
        initial = {'helpful': True} if not existing_vote else {'helpful': existing_vote.helpful}
        form = ReviewVoteForm(initial=initial)
    
    return render(request, 'reviews/review_vote.html', {
        'form': form,
        'review': review,
    })

@login_required
def add_comment(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    
    if request.method == 'POST':
        form = ReviewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()
            messages.success(request, "Comment added!")
            return redirect('reviews:movie_reviews', movie_id=review.movie.id)
    else:
        form = ReviewCommentForm()
    
    return render(request, 'reviews/add_comment.html', {
        'form': form,
        'review': review,
    })