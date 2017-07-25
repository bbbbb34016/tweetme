from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic import DetailView, ListView, CreateView,UpdateView,DeleteView
from django.db.models import Q
from .forms import TweetModelForm
from .models import Tweet
from .mixins import FormUserNeededMixin,UserOwnerMixin
from django.urls import reverse_lazy,reverse
# Create your views here.


class RetweetView(View):
    def get(self,request,pk,*args,**kwargs):
        tweet = get_object_or_404(Tweet,pk=pk)
        if request.user.is_authenticated():
            new_tweet = Tweet.objects.retweet(request.user,tweet)
            return HttpResponseRedirect("/")
        return HttpResponseRedirect(tweet.get_absolute_url())

#Create
class TweetCreateView(LoginRequiredMixin,FormUserNeededMixin,CreateView):
    form_class = TweetModelForm
    template_name = 'tweets/create_view.html'
    #success_url = '/tweet/create/'
    #https://docs.djangoproject.com/en/1.11/topics/auth/default/#the-loginrequired-mixin
    login_url = '/admin/'

    #cut to mixins.py
    # def form_valid(self, form):
    #     if self.request.user.is_authenticated():
    #         form.instance.user = self.request.user
    #         return super(TweetCreateView, self).form_valid(form)
    #     else:
    #         form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["User must be logged in to continue."])
    #         return self.form_invalid(form)

#Update
class TweetUpdateView(UserOwnerMixin,UpdateView):
    queryset = Tweet.objects.all()
    form_class = TweetModelForm
    template_name = 'tweets/update_view.html'
    #success_url = '/tweet/'

#Delete
class TweetDeleteView(LoginRequiredMixin,DeleteView):
    model = Tweet
    template_name = 'tweets/delete_view.html'
    success_url = reverse_lazy("tweet:list")


#Retrieve
class TweetDetailView(DetailView):    
    queryset = Tweet.objects.all()
    #template_name = "tweets/detail_view.html"
    # def get_object(self):
    #     print(self.kwargs)
    #     pk = self.kwargs.get("pk")
    #     obj = get_object_or_404(Tweet, pk=pk)
    #     return Tweet.objects.get(id=pk)

class TweetListView(ListView):
    #template_name = "tweets/list_view.html"
    #queryset = Tweet.objects.all()

    #search function
    def get_queryset(self,*args,**kwargs):
        qs = Tweet.objects.all()

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

    def get_context_data(self,*args,**kwargs):
        context = super(TweetListView,self).get_context_data(*args,**kwargs)

        #tweet_list.html
        context['create_form'] = TweetModelForm()
        context['create_url'] = reverse_lazy("tweet:create")

        return context

def tweet_detail_view(request,pk=None): #pk == id
    #Get from database
    # obj = Tweet.objects.get(pk=pk)
    obj = get_object_or_404(Tweet, pk=pk)
    print(obj)
    context = {
        "object":obj,
    }
    return render(request,"tweets/detail_view.html",context)



# def tweet_list_view(request):
#     queryset = Tweet.objects.all()
#     print(queryset)
#     for obj in queryset:
#         print(obj.content)
#     context = {
#         "object_list":queryset
#     }
#     return render(request,"tweets/list_view.html",context)