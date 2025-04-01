from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    image = models.ImageField(upload_to='movies/', blank=True, null=True)
    
    def __str__(self):
        return self.title
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
    
    class Meta:
        unique_together = ('user', 'movie')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sentiment = models.CharField(max_length=20, blank=True, null=True)

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(rating__gte=1, rating__lte=10),
                name='rating_range',
                violation_error_message='Rating should be between 1 and 10'
            ),
        ]

    