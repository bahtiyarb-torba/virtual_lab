from django.http import HttpResponse
import logging
logger = logging.getLogger(__name__)
from vital.forms import Course_Details_Form,Network_creation_Form
from django.contrib.auth import login as django_login, authenticate,logout as django_logout
from vital.utils import audit,get_notification_message,SneakyXenLoadBalancer
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from vital.models import VLAB_User,Course,Admin_Network_Configuration

def designate_admin(request):
    logger.debug("At designate an admin page")
    message = 'Designate user as administrator'
    error_message =''
    users = []
    if request.method == 'POST':
        logger.debug("In designate admin POST")
        checked = request.POST.getlist('checks')
        logger.debug(request.POST)
        logger.debug(checked)
        VLAB_User.objects.filter(email__in=checked).update(is_admin = True)
    else:
        logger.debug("In designate admin GET")
    try:
        users = VLAB_User.objects.filter(is_admin__exact=False)
    except VLAB_User.DoesNotExist:
        error_message = 'No candidate users found'
    return render(request, 'admin_mod/designate_admin.html', {'message': message,'users':users,'error_message':error_message})

def remove_admin(request):
    logger.debug("At remove an admin page")
    message = 'Remove user as administrator'
    error_message = ''
    users = []
    try:
        users = VLAB_User.objects.filter(is_admin='t')
    except VLAB_User.DoesNotExist:
        error_message = 'No candidate users found'
    return render(request, 'admin_mod/remove_admin.html', {'message': message,'users':users,'error_message':error_message})

def course_details(request):
    logger.debug("At course details page")

def network_definition(request):
    logger.debug("At network definition page")
    message = 'Custom Course - Network definition'
    error_message = ''
    if request.method =='POST':
        course_form = Course_Details_Form(request.POST)
        network_form = Network_creation_Form(request.POST)
        if course_form.is_valid() and network_form.is_valid():
            logger.debug(course_form.cleaned_data['course_number'] + '<>' + course_form.cleaned_data['course_name'])
            temp_course = Course(course_number = course_form.cleaned_data['course_number'],name = course_form.cleaned_data['course_name'],registration_code=course_form.cleaned_data['course_number']+'CODE',status = 'ACTIVE')
            temp_course.save()
            id = temp_course.id
            network = Admin_Network_Configuration(course_vlan_id=id,
                                                  subnet_start=network_form.cleaned_data['subnet_start'],
                                                  subnet_end=network_form.cleaned_data['subnet_end'],
                                                  networks_per_user=network_form.cleaned_data['networks_per_user'])
            network.save()
            message = 'Network information saved successfuly'
            return render(request, 'admin_mod/success page.html',{'message': message, 'error_message': error_message})
        else:
            error_message = 'Error encountered while submitting information.Please try again.'
            return render(request, 'admin_mod/network_definition.html',{'message': message, 'error_message': error_message})
    else:
        course_form = Course_Details_Form()
        network_form = Network_creation_Form()
        return render(request, 'admin_mod/network_definition.html',
                      {'message': message,'error_message':error_message,'course_form':course_form,'network_form':network_form})

def image_creation(request):
    logger.debug("At image creation page")
    message = 'Create a custom VM image'
    return render(request, 'admin_mod/image_creation.html', {'message': message})

def course_design(request):
    logger.debug("At course design page")
    message = 'Design a Course'
    return render(request, 'admin_mod/course_design.html', {'message': message})

def monitoring(request):
    logger.debug("At monitoring page")
    message = 'Monitor users'
    return render(request, 'admin_mod/monitoring.html', {'message': message})

def edit_course(request):
    logger.debug("At edit course page")
    message = 'Edit a course'
    return render(request, 'admin_mod/edit_course.html', {'message': message})

def delete_course(request):
    logger.debug("At course deletion page")
    message = 'Delete a course'
    return render(request, 'admin_mod/delete_course.html', {'message': message})