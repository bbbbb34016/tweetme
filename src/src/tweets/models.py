from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.urls import reverse

# Create your models here.

from .validators import validate_content


class Tweet(models.Model):
    # def validate_content(value):
    #     content = value
    #     if content == "abc":
    #         raise ValidationError("Content cannot be abc")
    #     return value
    #User
    user      = models.ForeignKey(settings.AUTH_USER_MODEL)    
    content   = models.CharField(max_length=140,validators=[validate_content])  
    timestamp = models.DateTimeField(auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.content.encode('utf-8')

    #display on tweet content
    #def __str__(self):
        # return str(self.content)

    def get_absolute_url(self):
        return reverse("tweet:detail", kwargs={"pk":self.pk})

    class Meta:
        ordering = ['-timestamp']
    # def clean(self,*args,**kwargs):
    #     content = self.content
    #     if content == "abc":
    #         raise ValidationError("Content cannot be abc")
    #     return super(Tweet,self).clean(*args,**kwargs)