from django.shortcuts import render, redirect
from django.http import HttpResponse
from pro.models import Post,Comment
from pro.form import CommentForm
# Create your views here.
def home(req):
    post_list = Post.objects.all()
    context={'post':post_list}
    return render(req,'home.html',context)

def postDetail(req,pk):
    post = Post.objects.get(pk=pk)
    comments = post.comments.filter(active=True, parent__isnull=True)
    if req.method=='POST':
        comment_form = CommentForm(data=req.POST)
        print('come in side of comment form',comment_form)
        if comment_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(req.POST.get('parent_id'))
            except:
                parent_id=None
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    replay_comment = comment_form.save(commit=False)
                    replay_comment.parent = parent_obj
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            url = '/comment/postDetail/'+str(pk)
            return redirect(url)
            print('save is complite')
        else:
            print('error',comment_form.errors)
    else:
        comment_form = CommentForm()

    context = {'post':post,'comments':comments,'comment_form':comment_form}
    return render(req,'post_detail.html',context)
