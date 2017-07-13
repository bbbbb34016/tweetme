from rest_framework import generics
from rest_framework import permissions
from django.db.models import Q
from tweets.models import Tweet

from .pagination import StandardResultsPagination
from .serializers import TweetModelSerializer


class TweetCreateAPIView(generics.CreateAPIView):
    serializer_class = TweetModelSerializer
    permisstion_classes = [permissions.IsAuthenticated]
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)



class TweetListAPIView(generics.ListAPIView):
    serializer_class = TweetModelSerializer
    pagination_class = StandardResultsPagination

    def get_queryset(self,*args,**kwargs):
        qs = Tweet.objects.all().order_by("-timestamp")#order by(something)
        #print(self.request.GET)
        query = self.request.GET.get('q',None)
        if query is not None:
            qs = qs.filter(
                #https://docs.djangoproject.com/en/1.11/topics/db/queries/#complex-lookups-with-q-objects
                    #search contains
                    Q(content__icontains=query)|
                    #search username
                    Q(user__username__icontains=query)
                )
        return qs