from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from tweets.models import Tweet

from tweets.api.pagination import StandardResultsPagination
from tweets.api.serializers import TweetModelSerializer
from hashtags.models import HashTag

class TagTweetAPIView(generics.ListAPIView):
    queryset = Tweet.objects.all().order_by("-timestamp")
    serializer_class = TweetModelSerializer
    pagination_class = StandardResultsPagination

    def get_seriailizer_context(self,*args,**kwargs):
        context = super(TagTweetAPIView, self).get_serializer_context(*args,**kwargs)
        context['request'] = self.request
        return context
    def get_queryset(self,*args,**kwargs):
        hashtag = self.kwargs.get("hashtag")
        hashtag_obj = None
        try:
            hashtag_obj = HashTag.objects.get_or_create(tag=hashtag)[0]
        except:
            pass
        if hashtag_obj:
            qs = hashtag_obj.get_tweets()
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
        return None