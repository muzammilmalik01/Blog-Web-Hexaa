from rest_framework import generics, views, status, permissions
from django.core.mail import send_mail
from accounts.models import CustomUser, PremiumUser
from accounts.serializer import PremiumUserSerializer
from .models import Like, Comment, Post, PostHistory
from .serializer import LikeSerializer, CommentSerializer, PostSerializer, PostHistorySerializer
from django.utils.text import slugify
from django.http import Http404
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.db.models import Count
from django.utils import timezone
from .permissions import PostPermissions, CommentPermissions, LikePermissions, PostHistoryPermissions
from django.conf import settings
import stripe
from rest_framework.pagination import PageNumberPagination

# Post Views #
class ScheduledPostPremiumUserMixin: # Implementing DRY.
    
    def get_queryset(self):
        """
        This method filters posts based on scheduled time and non-premium post.
        * Applied at all Post View * 
        * Tested on all views - working *
        * Working on Lists Views and Detail Views  *

        GET LIST:
            - UnAuthenticated Anonymous GET List Request -> All posts - Premium Posts
            - Authenticated NON - PREM User GET List Request -> All posts - Premium Posts
            - Authenticated PREM User GET List Request -> All posts + Premium Posts
        
        GET DETAILED POST:
            - UnAuthenticated Anonymous GET Detail Request -> Returns NO Premium Post
            - Authenticated NON - PREM User GET Detail Request -> Returns NO Premium Post
            - Authenticated PREM User GET List Request -> Returns Premium Post
        """
        user = self.request.user

        if user.is_anonymous: # Checking for anonymous (Unauthenticated Read-Only) requets.
            return super().get_queryset().filter(posted_at__lte=timezone.now(), is_premium_post=False)

        # The request if from some authenticated user so, check if the user if premium user or not.
        premium_user = PremiumUser.objects.filter(user=user).first()

        # If the user is Authenticated but not Premium User or does not have premium subscription - No Premium Posts.
        if not premium_user or not premium_user.has_active_subscription():
            return super().get_queryset().filter(posted_at__lte=timezone.now(), is_premium_post=False)

        # If the user is a premium user and has an active subscription, return all posts
        return super().get_queryset().filter(posted_at__lte=timezone.now())

class PremiumPostMixin:
    def get_queryset(self):
        """
        This Mixin checks if the user is premium of not, and the returns Premium Posts accordingly.
        """
        user = self.request.user

        if user.is_anonymous: # Checking for anonymous (Unauthenticated Read-Only) requets.
            raise PermissionDenied('Permission Denied - Not Premium User')

        # The request if from some authenticated user so, check if the user if premium user or not.
        premium_user = PremiumUser.objects.filter(user=user).first()

        # If the user is Authenticated but not Premium User or does not have premium subscription - No Premium Posts.
        if not premium_user or not premium_user.has_active_subscription():
            raise PermissionDenied('Permission Denied - Not Premium User')

        # If the user is a premium user and has an active subscription, return all posts
        return super().get_queryset().filter(posted_at__lte=timezone.now(), is_premium_post=True)

class PaginationMixin:
    pagination_class = PageNumberPagination
class CreatePostAPI(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [PostPermissions]

    def perform_create(self, serializer):
        """
        Gets 'post_slug' from the post data.

        If 'post_slug' is an empty String (Blank), it will automatically create a slug for the post based on the title.
        """
        slug_blank = serializer.validated_data.get('post_slug') # get the slug.
        if slug_blank == '': # if slug == empty string (blank)
            #! BUG: If the title is same for 2 posts, it will cause an error while saving the record, as it is set to be Unique Field in the models.
            raw_slug = serializer.validated_data.get('post_title') # get post_title
            slug = slugify(raw_slug) # create the new slug
            serializer.save(post_slug = slug) # save record to DB.

        else: 
            serializer.save() # else, simply save it.

class ListAllPostsAPI(ScheduledPostPremiumUserMixin,PaginationMixin,generics.ListAPIView):
    """
    List view using Generics.

    Gets all Published posts. (Implementation of content scheduling)

    * Scheduling enabled *
    * Premium Posts Enabled *
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-posted_at')
    permission_classes = [PostPermissions]

class DetailPostAPI(ScheduledPostPremiumUserMixin,generics.RetrieveUpdateDestroyAPIView):
    """
    Detail (GET, PUT, POST, DELETE) view using Generics with PK (id).

    ! Time check not implemented yet !
    """
    # queryset = Post.objects.filter(is_premium_post = False)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostPermissions]

    def retrieve(self, request, *args, **kwargs):
        """
        Overriding the retrieve function.

        Increments the 'views' by +1 when detailed post is retrieved and saves into the database.

        ! BUG: Users can simply perform refresh the window to increase the views count !
        * How to Fix: Use Sessions to keep track of viewed Posts or Track the user's view count using IP Address. * 
        """
        instance = self.get_object() # Getting the instance of the object.
        if instance.views is None:
            instance.views = 1 
            instance.save(update_fields=['views']) # Updating the value in the database.
            serializer = self.get_serializer(instance) # Serializing the data.
            return Response(serializer.data) # Returning the object.
        
        instance.views += 1 # Incrementing the view.
        instance.save(update_fields=['views']) # Updating the value in the database.
        serializer = self.get_serializer(instance) # Serializing the data.
        return Response(serializer.data) # Returning the object.
        
class SlugPostAPI(ScheduledPostPremiumUserMixin,generics.RetrieveAPIView):
    """
    GET View using post_slug instead for PK.

    Uses 'post_slug' as the look-up field.

    * Scheduling enabled *
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostPermissions]
    lookup_field = 'post_slug'

    def get_object(self):
        """
        Overriding get_object() to get object using Slug.

        Args: str (Slug)
        Returns: obj (Post): The post object.
        """
        queryset = self.get_queryset()
        slug = self.kwargs.get(self.lookup_field) # Get the value of slug from URL Params.
        obj = queryset.filter(post_slug=slug).first() # Performing Look-up

        if obj is None: # Check if the Obj with the requested Slug exists or not.
            raise Http404("Post Not Found") # Return 404 if not found.
        
        return obj # Returning Object if found. 
    
    def retrieve(self, request, *args, **kwargs):
        """
        Overriding the retrieve function.

        Increments the 'views' by +1 when detailed post is retrieved and saves into the database.

        ! BUG: Users can simply perform refresh the window to increase the views count !
        * How to Fix: Use Sessions to keep track of viewed Posts or Track the user's view count using IP Address. * 
        """
        instance = self.get_object() # Getting the instance of the object. 
        instance.views += 1 # Incrementing the view.
        instance.save(update_fields=['views']) # Updating the value in the database.
        serializer = self.get_serializer(instance) # Serializing the data.

        # Get the queryset that excludes premium posts
        queryset = self.get_queryset()

        post_type = request.GET.get('type')

        if post_type == 'featured':
            queryset = queryset.filter(is_featured = True).order_by('id')
        elif post_type == 'top':
            queryset = queryset.filter(is_top_post = True).order_by('id')
        

         # Get the next and previous posts
        next_post = queryset.filter(id__gt=instance.id).order_by('id').first()
        previous_post = queryset.filter(id__lt=instance.id).order_by('-id').first()

        # Add the post_slug of the next and previous posts to the response
        # ! Not thoughrouly tested - Only works for Slug Post View. !
        response = serializer.data
        response['next_post_slug'] = next_post.post_slug if next_post else None
        response['next_post_id'] = next_post.id if next_post else None
        response['previous_post_slug'] = previous_post.post_slug if previous_post else None


        return Response(response) # Returning the object.
    
class GetFeaturedPosts(ScheduledPostPremiumUserMixin,PaginationMixin,generics.ListAPIView):
    """
    Getting all Featured posts by field 'is_featured' = True.
    
    * Scheduling enabled *
    """
    queryset = Post.objects.filter(is_featured = True).order_by('id')
    serializer_class = PostSerializer
    permission_classes = [PostPermissions]

class GetTopPosts(ScheduledPostPremiumUserMixin,PaginationMixin,generics.ListAPIView):
    """
    Getting all LATEST Published Top Posts by field 'is_top_post' = True.

    * Scheduling enabled *
    """
    queryset = Post.objects.filter(is_top_post = True).order_by('id')
    serializer_class = PostSerializer
    permission_classes = [PostPermissions]

class GetPopularPosts(ScheduledPostPremiumUserMixin,PaginationMixin,generics.ListAPIView):
    """
    Getting all Published Popular Posts by Highest Likes and Highest Comments.

    * Scheduling enabled *
    """
    queryset = Post.objects.annotate(total_likes=Count('likes')).annotate(total_comments=Count('comments')).order_by('-total_likes', '-total_comments')
    serializer_class = PostSerializer
    permission_classes = [PostPermissions]

class GetTrendingPosts(ScheduledPostPremiumUserMixin,PaginationMixin,generics.ListAPIView):
    """
    This view, calls 'get_eng_score' to calculate eng_score for all posts.

    ! Issue 1: This method will cause performance issues if there are to many posts ! 
    TODO: For now, Trending Published Posts are being processed but will have to work for an efficient solution.
    * Scheduling enabled *
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [PostPermissions]
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = sorted(queryset, key=lambda obj: obj.get_eng_score(), reverse=True)
        return queryset
    
# Post Views End #
    
# Comments View #

class ListComments(generics.ListAPIView):
    """
    List all comments. (GET)

    Permissions: 
        Comment Permissions.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CommentPermissions]

class CreateComment(generics.CreateAPIView):
    """
    Create a new comment. (POST)
    ! BUG: We can add a reply to a Parent Comment of a Post A and in Post ID we can pass Post B. !
    ! The user should be able to only reply to a comment of Post A, which is not addresses as of now. !
    ! Add functionality, if DateTime is not provided, it should automatically add the DateTime.
    
    Permissions: 
        Comment Permissions.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CommentPermissions]

class DetailComment(generics.RetrieveUpdateDestroyAPIView):
    """
    Access a detailed comment. (GET, DELETE, PUT, PATCH)
    
    Permissions: 
        Comment Permissions.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CommentPermissions]

class GetPostComments(generics.ListAPIView):
    """
    A view to retrieve comments for a specific post.

    This view returns a list of comments associated with a specific post.
    The comments are serialized using the CommentSerializer class.

    Attributes:
        serializer_class (CommentSerializer): The serializer class used to serialize the comments.
        queryset (QuerySet): The queryset used to retrieve the comments.

    Permissions: 
        Comment Permissions.
    """

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    # permission_classes = [CommentPermissions]

    def get_queryset(self):
        """
        Retrieves the comments for the specified post.

        Returns:
            QuerySet: The queryset containing the comments for the specified post.

        Raises:
            Http404: If no comments are found for the specified post.
        """
        post_id = self.kwargs.get('post')
        post_obj = Post.objects.get(id=post_id)
        queryset = self.queryset.filter(post=post_obj)

        if not queryset.exists():
            raise Http404("No comments found for this post.")

        return queryset


class GetPostCommentsbySlug(generics.ListAPIView):
    """
    A view to retrieve comments for a specific post using Slug.

    This view returns a list of comments associated with a specific post.
    The comments are serialized using the CommentSerializer class.

    Attributes:
        serializer_class (CommentSerializer): The serializer class used to serialize the comments.
        queryset (QuerySet): The queryset used to retrieve the comments.

    Permissions: 
        Comment Permissions.
    ! Bug: Does not return exact number of Comments as number of Replies is not included.
    """

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    pagination_class = None
    # permission_classes = [CommentPermissions]

    def get_queryset(self):
        """
        Retrieves the comments for the specified post.

        Returns:
            QuerySet: The queryset containing the comments for the specified post.

        Raises:
            Http404: If no comments are found for the specified post.
        """
        slug = self.kwargs.get('slug')
        post_obj = Post.objects.get(post_slug=slug)
        queryset = self.queryset.filter(post=post_obj)

        if not queryset.exists():
            raise Http404("No comments found for this post.")

        return queryset


# Comments View End #

# Like Views #
    
class ListAllLikes(generics.ListAPIView):
    """
    List all comments. (GET)
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [LikePermissions]

class CreateLike(generics.CreateAPIView):
    """
    Create / Add a Like. (POST)
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    # permission_classes = [LikePermissions]

class DestroyPostLike(generics.DestroyAPIView):
    """
    Unlike / Remove a Like from the Post. (DELETE)
    """

    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    # permission_classes = [LikePermissions]

    def get_object(self):
        queryset = self.get_queryset()
        post_id= self.kwargs.get('post') 
        user_id = self.kwargs.get('user')
        
        # Get the Post and User instances
        post_obj = Post.objects.get(id=post_id)
        user_obj = CustomUser.objects.get(id=user_id)

        obj = queryset.filter(post=post_obj, liked_by=user_obj).first()  # Performing Look-up

        if obj is None: 
            raise Http404("Like Not Found") # Return 404 if not found.
        
        return obj # Returning Object if found. 

class DestroyCommentLike(generics.DestroyAPIView):
    """
    Unlike / Remove a Like from the Post. (DELETE)
    """

    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    # permission_classes = [LikePermissions]

    def get_object(self):
        queryset = self.get_queryset()
        comment_id= self.kwargs.get('comment') 
        user_id = self.kwargs.get('user')
        
        # Get the Post and User instances
        comment_obj = Comment.objects.get(id=comment_id)
        user_obj = CustomUser.objects.get(id=user_id)

        obj = queryset.filter(comment=comment_obj, liked_by=user_obj).first()  # Performing Look-up

        if obj is None: 
            raise Http404("Like Not Found") # Return 404 if not found.
        
        return obj # Returning Object if found. 

# Like Views End #
    
# PostHistory Views #

class ListAllPostsHistory(generics.ListAPIView):
    """
    List all Logs of PostHistory. (GET)
    """
    queryset = PostHistory.objects.all()
    serializer_class = PostHistorySerializer
    permission_classes = [PostHistoryPermissions]

class ListSinglePostHistory(generics.ListAPIView):
    
    """
    List all Editing History of a single post. 

    Args: Post (PK)

    Returns: All Editing history of a post ordered by latest ones.
    """
    lookup_field = 'post_id'
    serializer_class = PostHistorySerializer
    permission_classes = [PostHistoryPermissions]
    def get_queryset(self):
        post_id = self.kwargs.get(self.lookup_field)
        return PostHistory.objects.filter(post = post_id).order_by('-updated_at')

# PostHistory Views End #
    
# Send Mail View #

class SendEmailView(views.APIView):
    """
    A view for sending emails.

    This view requires authentication and expects a POST request with the following parameters:
    - subject: The subject of the email.
    - message: The content of the email.
    - user_email: The email address of the user sending the email.

    If all the required parameters are provided, the view sends an email to the specified recipient
    and returns a success message. Otherwise, it returns an error message.

    Note: The email is sent from the 'admin@blog.site' address.

    Example usage:
    POST /send-email/
    {
        "subject": "Hello",
        "message": "This is a test email",
        "user_email": "user@example.com"
    }
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Handle POST requests to send an email.

        Returns:
        - If the email is sent successfully, returns a JSON response with a success message and status code 200.
        - If the input is invalid or any required parameter is missing, returns a JSON response with an error message
          and status code 400.
        """
        subject = request.data.get('subject')
        message = request.data.get('message')
        user_email = request.data.get('user_email')
        author_email = 'admin@blog.site'

        if subject and message and user_email:
            send_mail(
                subject,
                message,
                user_email,
                [author_email],
                fail_silently=False,
            )
            return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)
    
# Send Mail Views End #
        
# Stripe Subscription Views #
        
 # TODO: Have to create a Unsubscribe / Cancel Subscription API.       

stripe.api_key = settings.STRIPE_SECRET_KEY
class CreateSubscriptionView(generics.CreateAPIView):
    """
    API view to handle creation of a new subscription for a user.
    Each PremiumUser corresponds to a Stripe Customer with a Subscription.
    ! Products (Premium Post) is hard coded !
    ! Have to provide users with option to Cancel the subscription !
    """
    queryset = PremiumUser.objects.all()
    serializer_class = PremiumUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Overriding create() to create a Stripe Customer and Subscription,
        and a corresponding PremiumUser in the database.
        """
        data = request.data
        customers = stripe.Customer.list(email=request.user.email).data

        if customers:  # If the customer already exists in Stripe
            customer = customers[0]
            customer = stripe.Customer.retrieve(customer.id, expand=['subscriptions'])

            # Check if the customer already has an active subscription
            for subscription in customer.subscriptions.data:
                if subscription.plan.id == "price_1Oqs9jLbIWA3Cm6Ek5D2k46i" and subscription.status == 'active':
                    return Response({'message': 'You are already subscribed to this plan'}, status=status.HTTP_400_BAD_REQUEST)

            # Else Create a new subscription for the customer
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{"price": "price_1Oqs9jLbIWA3Cm6Ek5D2k46i"}],
            )

            # Update or create the corresponding PremiumUser
            PremiumUser.objects.update_or_create(
                user=request.user,
                defaults={
                    'stripe_customer_id': customer.id,
                    'stripe_subscription_id': subscription.id,
                    'has_active_subscription': True,
                }
            )
            return Response({'message': 'Successfully Subscribed'}, status=status.HTTP_201_CREATED)

        else:  # If the customer doesn't exist in Stripe, create a new customer and subscription
            customer = stripe.Customer.create(email=request.user.email, source=data['source'])
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{"price": "price_1Oqs9jLbIWA3Cm6Ek5D2k46i"}],
            )

            # Create the corresponding PremiumUser
            PremiumUser.objects.create(
                user=request.user,
                stripe_customer_id=customer.id,
                stripe_subscription_id=subscription.id,
                has_active_subscription=True,
            )
            return Response({'message': 'Successfully Subscribed'}, status=status.HTTP_201_CREATED)
        
class PremiumPostsList(PremiumPostMixin,PaginationMixin,generics.ListAPIView):
    """
    This view returns list of Premium Posts to the Premium Users.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer