from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from movies.models import Movie
from .models import Watchlist, WatchlistItem
from .forms import WatchlistForm, WatchlistItemForm, WatchlistItemUpdateForm

@login_required
def user_watchlists(request):
    watchlists = request.user.watchlists.all()
    return render(request, 'watchlists/user_watchlists.html', {
        'watchlists': watchlists,
    })

@login_required
def create_watchlist(request):
    if request.method == 'POST':
        form = WatchlistForm(request.POST)
        if form.is_valid():
            watchlist = form.save(commit=False)
            watchlist.owner = request.user
            watchlist.save()
            form.save_m2m()  # Save collaborators
            messages.success(request, "Watchlist created successfully!")
            return redirect('watchlists:user_watchlists')
    else:
        form = WatchlistForm()
    
    return render(request, 'watchlists/create_watchlist.html', {
        'form': form,
    })

@login_required
def watchlist_detail(request, watchlist_id):
    watchlist = get_object_or_404(Watchlist, pk=watchlist_id)
    if not (watchlist.owner == request.user or request.user in watchlist.collaborators.all() or watchlist.privacy == 'PU'):
        messages.error(request, "You don't have permission to view this watchlist")
        return redirect('watchlists:user_watchlists')
    
    items = watchlist.items.select_related('movie').order_by('priority', '-added_at')
    return render(request, 'watchlists/watchlist_detail.html', {
        'watchlist': watchlist,
        'items': items,
    })

@login_required
def edit_watchlist(request, watchlist_id):
    watchlist = get_object_or_404(Watchlist, pk=watchlist_id, owner=request.user)
    
    if request.method == 'POST':
        form = WatchlistForm(request.POST, instance=watchlist)
        if form.is_valid():
            form.save()
            messages.success(request, "Watchlist updated successfully!")
            return redirect('watchlists:watchlist_detail', watchlist_id=watchlist.id)
    else:
        form = WatchlistForm(instance=watchlist)
    
    return render(request, 'watchlists/edit_watchlist.html', {
        'form': form,
        'watchlist': watchlist,
    })

@login_required
def delete_watchlist(request, watchlist_id):
    watchlist = get_object_or_404(Watchlist, pk=watchlist_id, owner=request.user)
    watchlist.delete()
    messages.success(request, "Watchlist deleted successfully!")
    return redirect('watchlists:user_watchlists')

@login_required
def add_to_watchlist(request, watchlist_id):
    watchlist = get_object_or_404(Watchlist, pk=watchlist_id)
    if not (watchlist.owner == request.user or request.user in watchlist.collaborators.all()):
        messages.error(request, "You don't have permission to add to this watchlist")
        return redirect('watchlists:user_watchlists')
    
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        if movie_id:
            movie = get_object_or_404(Movie, pk=movie_id)
            if not WatchlistItem.objects.filter(watchlist=watchlist, movie=movie).exists():
                WatchlistItem.objects.create(
                    watchlist=watchlist,
                    movie=movie,
                    status='WT',
                    priority=2
                )
                messages.success(request, f"Added {movie.title} to your watchlist!")
            else:
                messages.warning(request, f"{movie.title} is already in this watchlist")
            return redirect('watchlists:watchlist_detail', watchlist_id=watchlist.id)
    
    return redirect('watchlists:watchlist_detail', watchlist_id=watchlist.id)

@login_required
def update_watchlist_item(request, item_id):
    item = get_object_or_404(WatchlistItem, pk=item_id)
    if not (item.watchlist.owner == request.user or request.user in item.watchlist.collaborators.all()):
        messages.error(request, "You don't have permission to update this item")
        return redirect('watchlists:user_watchlists')
    
    if request.method == 'POST':
        form = WatchlistItemUpdateForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item updated successfully!")
            return redirect('watchlists:watchlist_detail', watchlist_id=item.watchlist.id)
    else:
        form = WatchlistItemUpdateForm(instance=item)
    
    return render(request, 'watchlists/update_item.html', {
        'form': form,
        'item': item,
    })

@login_required
def delete_watchlist_item(request, item_id):
    item = get_object_or_404(WatchlistItem, pk=item_id)
    watchlist_id = item.watchlist.id
    if not (item.watchlist.owner == request.user or request.user in item.watchlist.collaborators.all()):
        messages.error(request, "You don't have permission to delete this item")
        return redirect('watchlists:user_watchlists')
    
    item.delete()
    messages.success(request, "Item removed from watchlist")
    return redirect('watchlists:watchlist_detail', watchlist_id=watchlist_id)