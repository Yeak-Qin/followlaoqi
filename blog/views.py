from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail

from .forms import EmailPostForm, CommentForm
from .models import Post

def post_list(request):
    object_list = Post.objects.filter(status="published")
    paginator = Paginator(object_list, 1)
    page = request.GET.get('page')

    try:
        current_page = paginator.page(page)
        posts = current_page.object_list

    except PageNotAnInteger:
        current_page = paginator.page(1)
        posts = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        posts = current_page.object_list

    return render(request, 'blog/post/list.html', {'posts': posts, "page": current_page})

#def post_detail(request, post_id):
def post_detail(request, year, month, day, post):
    #post = get_object_or_404(Post, id=post_id)
    post = get_object_or_404(Post, slug=post, status="published", published__year=year, published__month=month, published__day=day)
    comments = post.comments.filter(active=True)
    
    if request.method == 'GET':
        comment_form = CommentForm()

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()

    return render(request, 'blog/post/detail.html', {"post":post, "comments":comments, "comment_form":comment_form})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="published")
    sent = False

    if request.method == 'GET':
        form = EmailPostForm()

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = "{0} ({1}) recommends you reading '{2}'".format(cd['name'], cd['email'], post.title)
            message = "Read '{0}' at {1}\n\n{2}\'s comments:{3}".format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, "qiwsir@qq.com", [cd['to']])
            sent = True

    return render(request, 'blog/post/share.html', {'post':post, "form":form, 'sent': sent},)
