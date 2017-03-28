from . import views
from django.conf.urls import url
app_name = 'admin_mod'
urlpatterns = [
    url(r'^$', views.admin_index, name='admin_index'),
    url(r'^login/$', views.admin_login, name='admin_login'),
    url(r'^unauthorized/$', views.unauthorized, name='admin_unauthorized'),
    url(r'^home/$', views.home, name='admin_home'),
    url(r'^logout/$', views.admin_logout, name='admin_logout'),
    url(r'^designate_admin/$', views.designate_admin, name='designate_admin'),
    url(r'^network_definition/$', views.network_definition, name='network_definition'),
    url(r'^image_creation/$', views.image_creation, name='image_creation'),
    url(r'^course_design/$', views.course_design, name='course_design'),
    url(r'^monitoring/$', views.monitoring, name='monitoring'),
    url(r'^edit_course/$', views.edit_course, name='edit_course'),
    url(r'^delete_course/$', views.delete_course, name='delete_course'),
]