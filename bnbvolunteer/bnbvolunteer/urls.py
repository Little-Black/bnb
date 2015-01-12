from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings 
from volunteers import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bnbvolunteer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^volunteer/home/$', views.volunteerHome, name="volunteerHome"),
    url(r'^volunteer/home/submit/$', views.volunteerSubmit, name="submitNewLog"),
    url(r'^login/$', views.userLogin, name="userLogin"),
    url(r'^register/$', views.userRegistration, name="userRegistration"),
    url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/login/'}, name="logout"),
    url(r'^profile/$', views.editProfile, name="editProfile"),
)
