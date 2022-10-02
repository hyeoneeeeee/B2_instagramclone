from django.shortcuts import render, redirect
from user.models import UserModel
from django.contrib import auth
import re
from django.contrib.auth.decorators import login_required




def sign_in_view(request):
    if request.method == "GET":
        user = request.user.is_authenticated
        if user:
            return render(request, 'post/post.html')
        else:
            return render(request, 'user/signin.html')

    elif request.method == "POST":
        is_email = re.compile(r"^[a-zA-Z]+[!#$%&'*+-/=?^_`(){|}~]*[a-zA-Z0-9]*@[\w]+\.[a-zA-Z0-9-]+[.]*[a-zA-Z0-9]+$")
        is_phone_num = re.compile(r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})')

        username = request.POST.get('username','')
        username.replace(' ','')
        password =request.POST.get('password','')
        print(username)
        print(password)
        if username == '' or password =='':
            return render(request,'user/signin.html', {'error':'아이디와 비밀번호는 공백 일 수 없습니다!!'})

        elif is_email.match(username) or is_phone_num.match(username):
            me = auth.authenticate(request, username=username, password=password)
            print(0)
            if me:
                auth.login(request, me)
                print(1)
                return redirect('/')
            else:
                print(2)
                return render(request, 'user/signin.html', {"error":'아이디와 비밀번호를 확인해 주세요!'})
        else:
            print(3)
            return render(request, 'user/signin.html', {"error":'아이디와 비밀번호를 확인해 주세요!'})


def sign_up_view(request):
    if request.method == "GET":
        user = request.user.is_authenticated
        if user:
            return render(request, 'home.html')
        else:
            return render(request, 'user/signup.html')

    elif request.method == "POST":
        is_email = re.compile(r"^[a-zA-Z]+[!#$%&'*+-/=?^_`(){|}~]*[a-zA-Z0-9]*@[\w]+\.[a-zA-Z0-9-]+[.]*[a-zA-Z0-9]+$")
        is_phone_num = re.compile(r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})')

        username = request.POST.get('username','')
        password = request.POST.get('password','')
        password2 = request.POST.get('password2','')
        nick_name = request.POST.get('user_nick_name','')

        if not is_email.fullmatch(username) and not is_phone_num.fullmatch(username):
            return render(request, 'user/signup.html', {'error': '아이디를 확인해 주세요!'})
        elif password != password2:
            return render(request, 'user/signup.html', {'error':'비밀번호가 맞지 않습니다!'})
        else:
            if username == '' or password == '' or nick_name == '':
                return render(request, 'user/signup.html',{'error':'사용자 이름, 비밀번호, 닉네임은 필수 값 입니다!'})
            already_using_name = UserModel.objects.filter(user_nick_name=nick_name)
            if already_using_name:
                return render(request,'user/signup.html', {'error':'닉네임이 이미 사용중입니다!'})
            else:
                new_user = UserModel()
                new_user.set_password(password)
                new_user.username = username
                new_user.user_nick_name = nick_name
                new_user.save()
    return redirect('/sign_in')

@login_required
def log_out(request):
    auth.logout(request)
    return redirect('/')

