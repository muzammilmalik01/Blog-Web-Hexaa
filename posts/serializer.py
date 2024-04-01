from rest_framework import serializers
from .models import Like, Comment, Post, PostHistory, Category, Tag, Notifications
from accounts.models import CustomUser
from django.utils import timezone
from django.core.exceptions import ValidationError

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
    
    def validate(self, data):
        """
        Validates the data for the serializer.

        Args:
            data (dict): The data to be validated.

        Raises:
            serializers.ValidationError: If the user has already liked the post or comment.

        Returns:
            dict: The validated data.

        ! BUG: Multiple Likes with same user on same post can be added using Admin Panel bcs admin panel don't serialize the data !
        * Working perfectly if same user tries to like a Post or Comment multiple times *
        """
        liked_by = data.get('liked_by')
        post = data.get('post')
        comment = data.get('comment')

        if post == None and comment == None: # Checking if it is a blank like.
            raise serializers.ValidationError("Please select either a post or a comment to like .")
        
        elif post and comment: # Checking if post and comment both are selected.
            raise serializers.ValidationError("Can't like both.")
        
        elif post: # checking if it is a like for a post.
            if timezone.is_aware(post.posted_at) and post.posted_at > timezone.now():
                raise ValidationError('Post has not been published yet.')
        
        return data # Returning data if above conditions are not met.

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer class for Comment model.

    Attributes:
        total_likes (int): The total number of likes for the comment.
        total_replies (int): The total number of replies for the comment.
    """

    total_likes = serializers.SerializerMethodField()
    total_replies = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    author = serializers.PrimaryKeyRelatedField(queryset = CustomUser.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'author', 'comment_text', 'post','parent_comment', 'commented_on', 'total_likes', 'total_replies', 'likes']

    def get_total_likes(self, obj):
        """
        Get the total number of likes for the comment.

        Args:
            obj (Comment): The Comment object.

        Returns:
            int: The total number of likes for the comment.
        """
        return Like.objects.filter(comment=obj).count()

    def get_total_replies(self, obj):
        """
        Get the total number of replies for the comment.

        Args:
            obj (Comment): The Comment object.

        Returns:
            int: The total number of replies for the comment.
        """
        return Comment.objects.filter(parent_comment=obj).count()
    
    def get_likes(self, obj):
        likes = Like.objects.filter(comment = obj)
        # print(like)
        return [l.liked_by.id for l in likes]

    def validate(self, data):
        """
        Validates the data for the serializer.

        Args:
            data (dict): The data to be validated.

        Raises:
            serializers.ValidationError: If the post has not been published, comment will not be added.

        Returns:
            dict: The validated data.
        """
        post = data.get('post')

        # Check if post is provided
        if not post:
            raise ValidationError('Post is required.')

        # Check if post.posted_at is timezone-aware and if the post has been published
        if timezone.is_aware(post.posted_at) and post.posted_at > timezone.now():
            raise ValidationError('Post has not been published yet.')

        return data

    def to_representation(self, instance):
        """
        Overrid this function to show:
            - Author = Author.username
        """
        representation = super().to_representation(instance)
        representation['author'] = {
        'id': instance.author.id,
        'username': instance.author.username
    }
        return representation
        
class PostSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Post model.

    Attributes:
        total_likes (int): The total number of likes for the post.
        total_comments (int): The total number of comments for the post.
    """

    total_likes = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    eng_score  = serializers.SerializerMethodField()
    author = serializers.PrimaryKeyRelatedField(queryset = CustomUser.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset = Category.objects.all())

    class Meta:
        model = Post
        fields = ['id', 'author', 'post_title','post_image','category','views', 'post_slug', 'post_text','tags','total_likes','total_comments','is_featured', 'is_top_post','posted_at', 'eng_score','is_premium_post']
    
    def to_representation(self, instance):
        """
        Overrid this function to show:
            - Author = Author.username
            - Category = Category.title
        Have to add Tags as title. Not added yet.
        """
        representation = super().to_representation(instance)
        representation['author'] = representation['author'] = {
        'id': instance.author.id,
        'username': instance.author.username
    }
        representation['category'] = instance.category.title
        representation['tags'] = [tag.title for tag in instance.tags.all()]
        return representation

    # TODO: How the response will look like, will depend on the requirement.
    # TODO: Still have to figure the problem on how to manage POST, UPDATE, PATCH request. (Fields do not appear when depth = 1)
    # TODO: POST, UPDATE, PATCH will cause issue when depth = 1. API Response should not return Foreign Key as an ID.
    # Init function override: https://stackoverflow.com/questions/32202824/depth-1-doesnt-work-properly-and-its-saves-null-in-manytomanyfield-and-forei
    # def __init__(self, *args, **kwargs):
    #     super(PostSerializer, self).__init__(*args, **kwargs)
    #     request = self.context.get('request')
    #     if request and request.method=='POST':
    #         self.Meta.depth = 0
    #     else:
    #         self.Meta.depth = 1
        
    # def get_depth(self):
    #     """
    #     Override to dynamically determine the depth based on the request method.
    #     """
    #     request = self.context.get('request')
    #     if request and request.method == 'POST':
    #         return 0  # Set depth to 0 for POST requests
    #     return 1  # Use default depth for other requests

    # def to_representation(self, instance):
    #     """
    #     Override to customize the serialized representation of the Post instance.
    #     """
    #     data = super().to_representation(instance)
    #     depth = self.get_depth()
    #     if depth == 1:
    #         # If depth is 1, exclude related User fields
    #         data.pop('author')
    #     return data

    def get_total_likes(self, obj):
        """
        Get the total number of likes for the post.

        Args:
            obj (Post): The Post object.

        Returns:
            int: The total number of likes for the post.
        """
        return Like.objects.filter(post=obj).count()

    def get_total_comments(self, obj):
        """
        Get the total number of comments for the post.

        Args:
            obj (Post): The Post object.

        Returns:
            int: The total number of comments for the post.
        """
        return Comment.objects.filter(post=obj).count()
    
    def get_eng_score(self, obj):
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
        total_likes = Like.objects.filter(post=obj).count() 
        total_comments = Comment.objects.filter(post=obj).count()
        total_views = obj.views
        post_date = obj.posted_at
        current_date = timezone.now()

        total_views = total_views if total_views is not None else 0
        total_likes = total_likes if total_likes is not None else 0
        total_comments = total_comments if total_comments is not None else 0

        if post_date is not None:
            days_difference = (current_date - post_date).days # Preventing division by 0 ahead.
        else:
            days_difference = 0
        # If Days Difference is 0, it will automatically return 0, so ZeroDivisionError is not raise.
        eng_score = (total_views * view_weight) + (total_likes * like_weight) + (total_comments * comment_weight) + (date_weight/days_difference if days_difference else 0)
        return eng_score
    

class PostHistorySerializer(serializers.ModelSerializer):
    """
    Serializer Class for PostHistory
    """
    class Meta:
        model = PostHistory
        fields = '__all__'

class NotificationsSerializier(serializers.ModelSerializer):
    """
    Serializer Class for PostHistory
    """
    class Meta:
            model = Notifications
            fields = '__all__'