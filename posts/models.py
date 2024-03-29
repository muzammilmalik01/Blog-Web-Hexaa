from django.db import models
from accounts.views import CustomUser
from category.models import Category
from tag.models import Tag
from django.utils import timezone

class Like(models.Model):
    liked_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name = 'likes',on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey('Comment', related_name = 'likes',on_delete=models.CASCADE, null=True, blank=True)

    # def __str__(self):
    #     if self.post:
    #         return f'Comment by {self.liked_by.username}'
    # ! __str__ NOT WORKING ! 
        
    class Meta:
        """
        Added unique_together to avoid Multiple like on same post or comment by same user.
        """
        unique_together = (('liked_by', 'post'), ('liked_by', 'comment'))
    
    def __str__(self) -> str:
        return f'Like by {self.liked_by} on post {self.post}'
    
class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    post_title = models.CharField(max_length = 200)
    post_slug = models.SlugField(unique = True, blank = True)
    post_text = models.CharField(max_length=3000)
    tags = models.ManyToManyField(Tag)
    is_featured = models.BooleanField(default = False)
    is_top_post = models.BooleanField(default = False)
    is_premium_post = models.BooleanField(default  = False)
    views = models.PositiveBigIntegerField(default = 0, blank = True, null = True)
    posted_at = models.DateTimeField(blank = True, null = True)
    post_image = models.ImageField(upload_to='posts/', null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.post_title} by {self.author}'
    
    def get_eng_score(self):
        """
        Calculates Engagement Score, used for browsing Trending Posts.
        Weights = Dummy for now.

        Formula: (total_views * view_weight) + (total_likes * like_weight) + (total_comments * comment_weight) + (date_weight/(current_date - post_date))
        
        Returns = Engagement Score (float) 
        """
        # Weights
        view_weight = 3
        like_weight = 1
        comment_weight = 2
        date_weight = 4
        # Gettings all Posts Metrics.
        total_likes = Like.objects.filter(post=self).count() 
        total_comments = Comment.objects.filter(post=self).count()
        total_views = self.views
        post_date = self.posted_at
        current_date = timezone.now()

        days_difference = (current_date - post_date).days # Preventing division by 0 ahead.
        # If Days Difference is 0, it will automatically return 0, so ZeroDivisionError is not raise.
        eng_score = (total_views * view_weight) + (total_likes * like_weight) + (total_comments * comment_weight) + (date_weight/days_difference if days_difference else 0)
        return eng_score 

    def save(self, *args, **kwargs):
        if not self.posted_at:
            self.posted_at = timezone.now()
        super().save(*args, **kwargs)

class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=2000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,null = True, blank = True, related_name='comments') 
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    commented_on = models.DateTimeField(auto_now_add=True, blank = True, null = True)

    def __str__(self) -> str:
        if self.parent_comment is None:
            return f'Comment on: {self.post.post_title} by user: {self.author.username}'
        else:
            return f'Reply to: {self.parent_comment.author.username} by {self.author.username}'

class PostHistory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    post_title = models.CharField(max_length = 50)
    post_slug = models.SlugField(blank = True)
    post_text = models.CharField(max_length=3000)
    tags = models.ManyToManyField(Tag)
    is_featured = models.BooleanField(default = False)
    is_top_post = models.BooleanField(default = False)
    views = models.PositiveBigIntegerField(default = 0)
    posted_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Post: {self.post.pk} by {self.author} edited at {self.updated_at}"

class Notifications(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    message = models.CharField(max_length = 255)
    notification_type = models.CharField(max_length = 30)
    is_read = models.BooleanField(default = False)
    created_at = models.DateTimeField(default = timezone.now)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, null = True, blank = True)
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE, null = True, blank = True)