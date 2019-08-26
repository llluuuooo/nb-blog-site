from django.shortcuts import render
from django.core.serializers import json
from django.shortcuts import render, redirect
from django.http import Http404
from datetime import *
import time
from app.DatabaseAPI import *
from django.contrib.auth.hashers import make_password, check_password
from app.models import *
from django.core.mail import *
from d3.settings import *


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        psw = request.POST.get('password')
        message = None
        if username and psw:
            try:
                user = Users.objects.get(user_name=username)
                if user.user_password == psw:
                    request.session['username'] = username
                    tp = user.user_state
                    if tp == "-1":
                        message = "账户已被封禁"
                    elif tp == "0":
                        return redirect('/')
                    else:
                        return redirect('/')
                else:
                    message = "密码错误"
            except:
                message = '用户不存在'
        return render(request, "login.html", locals())
    return render(request, "login.html")


def logout(request):
    del request.session['username']
    return redirect('/')


def index(request):
    username = request.session.get('username')
    blogset = Blog.objects.filter(blog_state=1)
    tagset = Tag.objects.all()
    if request.method == "POST":
        keyword = request.POST.get('s')
        if 'searchblog' in request.POST:
            blogset = Blog.objects.filter(blog_name__icontains=keyword)
            return render(request, 'searchresult.html', context={'blogset': blogset})
        elif 'searchuser' in request.POST:
            return redirect('/searchresult/', 'user', keyword)
    return render(request, "index.html", context={'blogset': blogset, 'tagset': tagset,'username':username})


def register(request):
    if request.method == "POST":
        msg = "951481"
        if 'send' in request.POST:
            email = request.POST.get("email")
            title = "欢迎注册nb博客"
            email_from = "nbblog@163.com"
            receiver = [email]
            send_mail(title, msg, email_from, receiver)
        elif 'submit' in request.POST:
            message = None
            username = request.POST.get('username')
            password1 = request.POST.get('password')
            password2 = request.POST.get('repassword')
            email = request.POST.get('email')
            captcha = request.POST.get('captcha')
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_name_user = Users.objects.filter(user_name=username)
                if same_name_user:  # 用户名不唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'register.html', locals())
                same_email_user = Users.objects.filter(user_mail=email)
                if same_email_user:  # 邮箱地址不唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'register.html', locals())
                if msg != captcha:
                    message = "验证码错误"
                    return render(request, 'register.html', locals())
                # 合法，创建新用户
                Users.objects.create(user_name=username, user_password=password1, user_mail=email, user_state=1)
                return redirect('/')  # 自动跳转到主页面
    return render(request, 'register.html', locals())


def editor(request):
    username = request.session.get('username')
    if request.method=='POST':
        if 'fabu' in request.POST:
            text = request.POST.get('text')
            title = request.POST.get('title')
            time  = datetime.now()
            user = Users.objects.filter(user_name=username)[0]
            Blog.objects.create(blog_name=title,blog_state=1,blog_body=text,blog_time=time,user=user,blog_likenumber=0,blog_viewnumber=0)
            redirect('/')
    return render(request, 'editor.html',context={'username':username})


def blogread(request, blog_id):
    username = request.session.get('username')
    blog = BlogData.searchBlog(blog_id)
    Blog.objects.filter(blog_id=blog_id).update(blog_viewnumber=blog.blog_viewnumber + 1)
    tags = BlogData.getTags(blog_id)
    reviews = ReviewData.getReviews(blog_id)
    blog_time = blog.blog_time.strftime('%Y-%m-%d %H:%M')
    if request.method == 'POST':
        if 'review' in request.POST:
            rev = request.POST.get('rev')
            username=request.session.get('username')
            review_time = datetime.now()
            return_user = BlogData.searchBlog(blog_id).user_id
            ReviewData.addReview(blog_id, username, review_time, rev, return_user)
            reviews = ReviewData.getReviews(blog_id)
            return render(request, 'blogRead.html',
                          context={'username':username,'title': blog.blog_name, 'body': blog.blog_body, 'time': blog_time, \
                                   'viewNumber': blog.blog_viewnumber, 'likeNumber': blog.blog_likenumber,
                                   'writer': blog.user.user_name, 'tags': tags, 'reviews': reviews})
        elif 'blogLikeButton' in request.POST:
            Blog.objects.filter(blog_id=blog_id).update(blog_likenumber=blog.blog_likenumber + 1)
            return render(request, 'blogRead.html',
                          context={'username':username,'title': blog.blog_name, 'body': blog.blog_body, 'time': blog_time, \
                                   'viewNumber': blog.blog_viewnumber, 'likeNumber': blog.blog_likenumber,
                                   'writer': blog.user.user_name, 'tags': tags, 'reviews': reviews})
    return render(request, 'blogRead.html', context={'username':username,'title': blog.blog_name, 'body': blog.blog_body, 'time': blog_time, \
                                                     'viewNumber': blog.blog_viewnumber,
                                                     'likeNumber': blog.blog_likenumber, 'writer': blog.user.user_name,
                                                     'tags': tags, 'reviews': reviews})
