from django.db import models
from users.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    path = models.ImageField(upload_to="img/%Y/%m/%d/", blank=True)
    description = models.TextField()

    def total_likes(self):
        return Like.objects.filter(book=self).count()
    
    def total_comments(self):
        return Comment.objects.filter(book=self).count()
    
    def user_commented(self, user):
        return Comment.objects.filter(book=self, user=user).exists()
    
    def user_liked(self, user):
        return Like.objects.filter(book=self, user=user).exists()
    
    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'book')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f'{self.user} on {self.book}'