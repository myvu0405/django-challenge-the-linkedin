from django.shortcuts import render,redirect

from django.contrib import messages

from .forms import *
from .models import *
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required

def joinPage(request):
    if request.user.is_authenticated:
        return redirect('members')

    form = UserRegisterForm()

    context ={'form':form}

    if request.method=='POST' and request.POST["form_type"]=='Login':
        email=request.POST['email']
        password=request.POST['password']

        user = authenticate(request,email=email, password=password)

        if user is not None:
            login(request, user)
            try: 
                next_url = request.GET['next']
                next_url=next_url.replace('/','')
                if next_url!= '':
                    return redirect(next_url)
                else:
                    return redirect('members')
                
            except:
                return redirect('members')

        else:
            messages.error(request,'Email or Password is incorrect!')

    elif request.method=='POST' and request.POST["form_type"]=='Register':

        form = UserRegisterForm(request.POST)

        if form.is_valid():
            if any(char.isdigit() for char in request.POST['name']):
                messages.error(request, "Member's name should only contain letters.")
                return render(request, 'accounts/login.html',{'form':form})
            elif len(request.POST['name']) <4:
                messages.error(request, "Member's name should contain at least 4 letters.")
                return render(request, 'accounts/login.html',{'form':form})

            elif any(char.isdigit() for char in request.POST['job_title']):
                messages.error(request, "Member's job title should only contain letters.")
                return render(request, 'accounts/login.html',{'form':form})

            elif len(request.POST['job_title']) <14:
                messages.error(request, "Member's job title should contain at least 14 letters.")
                return render(request, 'accounts/login.html',{'form':form})

            else:
                form.save()
                user = form.cleaned_data.get('name')
                messages.success(request, 'Member was registered and saved to database for '+user)
                return redirect('login')

        context = {'form':form}


    return render(request,'accounts/login.html',context)
    


def registerPage(request):
    form = UserRegisterForm()

    if request.method=='POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            if any(char.isdigit() for char in request.POST['name']):
                messages.error(request, "Member's name should only contain letters.")
                return render(request, 'accounts/register.html',{'form':form})
            elif len(request.POST['name']) <4:
                messages.error(request, "Member's name should contain at least 4 letters.")
                return render(request, 'accounts/register.html',{'form':form})

            elif any(char.isdigit() for char in request.POST['job_title']):
                messages.error(request, "Member's job title should only contain letters.")
                return render(request, 'accounts/register.html',{'form':form})

            elif len(request.POST['job_title']) <14:
                messages.error(request, "Member's job title should contain at least 14 letters.")
                return render(request, 'accounts/register.html',{'form':form})

            else:
                form.save()
                user = form.cleaned_data.get('name')
                messages.success(request, 'Member was registered and saved to database for '+user)
                return redirect('login')

    context = {'form':form}

    return render(request, 'accounts/register.html',context)

def loginPage(request):

    if request.user.is_authenticated:
        return redirect('members')

    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        user = authenticate(request,email=email, password=password)

        if user is not None:
            login(request, user)
            try: 
                next_url = request.GET['next']
                next_url=next_url.replace('/','')
                if next_url!= '':
                    return redirect(next_url)
                else:
                    return redirect('members')
                
            except:
                return redirect('members')

        else:
            messages.info(request,'Email or Password is incorrect!')

    context ={}

    return render(request,'accounts/login.html',context)

def logoutUser(request):

    logout(request)
    return redirect('login')

@login_required(login_url='/login')
def membersPage(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')

    members = LinkedinUser.objects.all().order_by('name')
    count=members.count()
    # form = MemberForm()

    return render(request,'accounts/members.html', {'members':members,'count':count})

@login_required(login_url='/login')
def profilePage(request,pk):
    member = LinkedinUser.objects.get(id=pk)

    return render(request,'accounts/profile.html',{'member':member})