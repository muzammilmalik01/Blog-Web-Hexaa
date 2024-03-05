from rest_framework import views, generics, status
from rest_framework.response import Response 
from .models import Subscribers
from .serializer import NewsletterSerializer
from django.core.mail import send_mail
from django.http import Http404


class AddSubscriberAPI(generics.CreateAPIView):
    """
    This view adds an email to the subscribers list.
    """
    queryset = Subscribers.objects.all()
    serializer_class = NewsletterSerializer

class SendNewsLetterAPI(views.APIView):
    """
    Args:
    This POST method accepts data having subject and message.

    Returns:
    Newsletter to all the subscribers in the list.
    
    """
    def post(self, request):
        subject = request.data.get('subject')
        message = request.data.get('message')
        if subject and message:
            subscribers = Subscribers.objects.all()
            for subscriber in subscribers:
                send_mail(
                    subject,
                    message,
                    'admin@blog.site',
                    [subscriber.email],
                    fail_silently=False,
                )
            return Response({'message':"Newsletter sent successfully."})
        else:
            return Response({'message':'Invalid inputs'}, status=status.HTTP_400_BAD_REQUEST)

class UnsubscribeAPI(generics.DestroyAPIView):
    queryset = Subscribers.objects.all()
    serializer_class = NewsletterSerializer

    def get_object(self):
        """
        Args: Email address that needs to be unsubscibed.

        Uses email arg to look for the subscriber

        DELETE if found. 
        """
        querset = self.get_queryset()
        email = self.kwargs.get('email')
        obj = querset.filter(email = email).first()

        if obj is None: # If subscriber not found.
            raise Http404('Subscriber not found.')
        return obj 