from . import views
from django.conf.urls import url
from django.shortcuts import redirect


urlpatterns = [
    url(r'^email/$', views.email, name='email'),
    url(r'^success/$', views.success, name='success'),
    url(r'^concediu/$', views.concediu, name='concediu'),
    url(r'^concediuManagement/$', views.ConcediuView.as_view(), name='concediuManagement'),
    url(r'^concediuManagement/(?P<pk>[0-9]+)/$', views.ConcediuDetailsView.as_view(), name='concediuManagementDetails'),
    url(r'^oohrequestManagement/$', views.OOHRequestView.as_view(), name='oohrequestManagement'),
    url(r'^oohrequestManagement/(?P<pk>[0-9]+)/$', views.OOHRequestDetailsView.as_view(), name='oohrequestManagementDetails'),
    url(r'^signup', views.signup, name='signup'),
    url(f'^profile', views.profile, name='profile'),
    url(r'^concediuManagement/[0-9]+/edit', views.edit, name='edit'),
    url(r'^oohrequestManagement/[0-9]+/validate', views.validate, name='validate'),
    url(r'^[a-zA-Z]+/inPending.html/$', views.InPendingView.as_view(), name='inPending'),
    url(r'^[a-zA-Z]+/approved.html/$', views.ApprovedView.as_view(), name='approved'),
    url(r'^generatePontaj.html/$', views.generatePontaj, name='generatePontaj'),
    url(r'^generatePontaj.html/pont$', views.pont, name='pont'),
    url(r'^oohrequest/$',views.oohrequest, name='oohrequest'),
    url(r'^[a-zA-Z]+/oohrequestInPending.html/$', views.InPendingOOHView.as_view(), name='oohrequestInPending'),
    url(r'^[a-zA-Z]+/oohrequestApproved.html/$', views.ApprovedOOHView.as_view(), name='oohrequestApproved'),
]