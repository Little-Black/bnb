from django.conf.urls import patterns, include, url
from django.contrib import admin

import settings 
from volunteers import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bnbvolunteer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^volunteer/home/$', views.volunteerHome, name="volunteerHome"),
    url(r'^volunteerStaff/home/$', views.volunteerStaffHome, name="volunteerStaffHome"),
    url(r'^volunteerStaff/home/user/$', views.volunteerStaffUser, name="volunteerStaffUser"),
    url(r'^volunteerStaff/home/activity/$', views.volunteerStaffActivity, name="volunteerStaffActivity"),
    url(r'^volunteerStaff/home/log/$', views.volunteerStaffLog, name="volunteerStaffLog"),
    url(r'^volunteerStaff/home/userSearchResult/$', views.volunteerStaffUserSearchResult, name="volunteerStaffUserSearchResult"),
    url(r'^volunteer/home/submit/$', views.volunteerSubmit, name="submitNewLog"),
    url(r'^login/$', views.userLogin, name="userLogin"),
    url(r'^logout/$', views.userLogout, name="logout"),
    url(r'^register/$', views.userRegistration, name="userRegistration"),
    url(r'^forgetPassword/$', views.forgetPassword, name="forgetPassword"),
    url(r'^profile/$', views.editProfile, name="editProfile"),
    url(r'^verify/(?P<code>.*)$', views.verify, name="verifyRequest"),
    url(r'^deleteAccount/$', views.deleteAccount, name="deleteAccount"),
    url(r'^search/$', views.search, name="search"),
    url(r'^updateProfile/$', views.updateProfile, name="updateProfile"),
    url(r'^codeGenerator/$', views.codeGenerator, name="codeGenerator"),
    url(r'^generateCodes/$', views.generateCodes, name="generateCodes"),
    url(r'^viewGeneratedCodes/$', views.viewGeneratedCodes, name="viewGeneratedCodes"),
    url(r'^exportCodes/$', views.exportCodes, name="exportCodes"),
)
