from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile, FollowersCount


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)   #instantiates a user form
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created successfully!')
            return redirect('login')
    else:
        form = UserRegisterForm()   #creating a blank form
    return render(request, 'accounts/register.html', {'form': form})

#user must be logged in to view this page
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES, 
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated successfully!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'accounts/profile.html', context)


def follow_unfollow(request):
    user = request.user
    if request.method == "POST":
        prof_id = request.POST.get('prof_id')
        prof_objj = Profile.objects.get(id=prof_id)

        if user in prof_objj.followed.all():
            prof_objj.followed.remove(user)
        else:
            prof_objj.followed.add(user)

        follow, created = FollowersCount.objects.get_or_create(user=user, post_id=prof_id)
        if not created:
            if follow.value == 'Follow':
                follow.value = 'Unfollow'
            else:
                follow.value = 'Follow'
        follow.save()
    return redirect('/')


#messages
"""
message.debug
message.info
message.success
message.warning
message.error
"""