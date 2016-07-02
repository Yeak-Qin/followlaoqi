# coding:utf-8

from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, widget = forms.TextInput(attrs={"class": "", "placeholder": "please input your name"}), )
    email = forms.EmailField(widget = forms.EmailInput(attrs={"placeholder":"your email",}),)
    to = forms.EmailField(widget = forms.EmailInput(attrs={"placeholder":"email that you sent",}),)
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    name = forms.CharField(max_length=25, widget = forms.TextInput(attrs={"class": "", "placeholder": "please input your name"}), )
    body = forms.CharField(required=False, widget=forms.Textarea)
    class Meta:
        model = Comment
        fields = ('name', 'body')