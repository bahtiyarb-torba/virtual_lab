from django.http import HttpResponse
import logging
logger = logging.getLogger(__name__)
from vital.forms import Authentication_Form,User_Activation_Form
from django.contrib.auth import login as django_login, authenticate,logout as django_logout
from vital.utils import audit,get_notification_message
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from vital.models import VLAB_User, Course

def admin_login(request):
    logger.debug("In Administrator Login")
    error_message = ''
    if request.method == 'POST':
        logger.debug("In Administrator Login POST")
        form = Authentication_Form(request.POST)
        if form.is_valid():
            logger.debug(form.cleaned_data['email']+'<>'+form.cleaned_data['password'])
            user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    if user.is_admin:
                        django_login(request, user)
                        audit(request, 'User logged in')
                        return redirect('/admin/home')
                    else:
                        error_message = "User is not an authorised administrator"
                        audit(request, 'User not an authorised administrator')
                else:
                    form = User_Activation_Form(initial={'user_email': user.email})
                    return render(request, 'vital/user_registration_validate.html', {'message': 'User is not active. ' +
                                                                                        'Please check your mail(' +
                                                                                        user.email+') for ' +
                                                                                        'activation code',
                                                                             'form': form})
            else:
                error_message = 'Login failed! Check your username and password.'
        else:
            error_message = 'Login failed! Check your username and password.'
    else:
        form = Authentication_Form()
        # to display common notification messages like system maintenance plans on all pages
        request.session['notification'] = get_notification_message()
    return render(request, 'admin_mod/admin_login.html', {'form': form, 'error_message': error_message})

@login_required(login_url='/admin/login/')
def admin_logout(request):
    logger.debug("At admin logout")
    logger.debug(">>>>>>>>>>>>>>>>>>" + str(request.user))
    audit(request, 'User logged out')
    django_logout(request)
    return redirect('/admin/login')

@login_required(login_url='/admin/login/')
def admin_index(request):
    logger.debug("At Administrator index")
    user = request.user
    if not user.is_admin:
        return redirect('/admin/unauthorized')  # change here to home page
    else:
        logger.debug('User is an authorized admin')
        return redirect('/admin/home')  # change here to home page

def unauthorized(request):
    logger.debug("At Unauthorized access to Admin Site")
    message = 'This user is not an Authorized Administrator'
    return render(request, 'admin_mod/unauthorized_access.html', {'message':message})

def home(request):
    logger.debug("At Admin Home")
    message = 'Admin System'
    user = request.user
    #user = VLAB_User.objects.get(email=user.email)
    username = user.get_short_name()
    options_list = ["Designate user as admin","Network Definition Utility" ,"VM Image Creation Utility","Course Design Utility","Monitoring Utility","Edit Course","Delete Course"]
    options_url = ["designate_admin","network_definition","image_creation","course_design","monitoring","edit_course","delete_course"]
    len = options_url.__len__()
    for y in range(0,len):
        options_url[y] = "admin_mod:"+ options_url[y]
    options = zip(options_url,options_list)
    return render(request, 'admin_mod/admin_home.html', {'message': message,'username':username,'options':options})


