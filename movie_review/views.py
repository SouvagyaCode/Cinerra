from django.shortcuts import render, redirect
from .models import Movie,Review,Wishlist,Comment
from django.shortcuts import get_object_or_404
from .forms import ReviewForm
from django.db.models import Avg
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .utils import analyze_sentiment, get_sentiment_label

from django.db.models import Q 

def home(request):
    query = request.GET.get('query', '')
    movies = Movie.objects.all()
    
    if query:
        movies = movies.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) 
        ).distinct()

    return render(request, 'base.html', {
        'movies': movies,
        'search_query': query
    })

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie,id = movie_id)
    reviews = Review.objects.filter(movie=movie)
    comments = Comment.objects.filter(movie=movie).order_by('-created_at')

    comments = Comment.objects.filter(movie=movie).order_by('-created_at')

    user_review = Review.objects.filter(movie=movie, user=request.user)

    avg_rating = Review.objects.filter(movie=movie).aggregate(Avg('rating'))['rating__avg'] or 0 

    sentiment_label = get_sentiment_label(avg_rating) if avg_rating else "No Sentiment"

    in_wishlist = Wishlist.objects.filter(user = request.user , movie = movie_id).exists()
    return render(request, 'movie_detail.html',
                   {'movie': movie,
                    'reviews': reviews,
                    'user_review':user_review,
                    'comments':comments,
                    'in_wishlist':in_wishlist ,
                    'avg_rating':avg_rating,
                    'sentiment_label':sentiment_label,}
                    )


def add_comment(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')

        if comment_text:
            Comment.objects.create(user=request.user, movie=movie, comment_text=comment_text)

        return redirect('movie_detail', movie_id=movie.id)



@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    review = movie.reviews.filter(user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if review:
                review.update(rating=form.cleaned_data['rating'], review_text=form.cleaned_data['review_text'])   
            else:
                review = form.save(commit=False)
                review.movie = movie
                review.user = request.user
                review.save()

            return redirect('movie_detail', movie_id=movie.id)
        
    else:
        form = ReviewForm()
    return render(request, 'movie_review.html', {'form': form, 'movie': movie, 'review': review,'rating_range':range(1,11)})


def add_to_wishlist(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    wishlist, created = Wishlist.objects.get_or_create(user=request.user, movie=movie)
    if not created:
        wishlist.delete()
        return redirect('movie_detail', movie_id
        =movie.id)

    return redirect('movie_detail', movie_id=movie.id)


def wishlist(request):
    wishlists = Wishlist.objects.filter(user=request.user)
    return render (request,'wishlist.html',{'wishlists':wishlists})