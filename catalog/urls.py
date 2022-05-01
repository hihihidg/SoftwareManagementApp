from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.conf.urls import include
import catalog.views 


urlpatterns = [
    path('softwarerequest/', views.CreateSoftwareRequest.as_view(), name='softwarerequest-create'),
    path('', TemplateView.as_view(template_name='dashboard/home.html'), name='home'),
    path('accounts/', include('allauth.urls')),
    path('mysoftware/', views.AvailableSoftwareByUser.as_view(template_name = 'catalog/availablesoftwarelicense.html'), name='mysoftware'),
    path('availablesoftware/', views.AvailableSoftwareByUser.as_view(), name='availablesoftware'),
    path('software/<int:pk>', views.SoftwareDetailView.as_view(), name='software-detail'),
    path('softwarerequests/manage/', views.SoftwareRequestsManager.as_view(), name='softwarerequests-manager'),
    path('softwarerequests/<uuid:pk>', views.SoftwareRequestsDetailView.as_view(), name='softwarerequests-detail'),
    path('softwarerequests/<uuid:pk>/delete/', views.DeleteRequestingSoftware.as_view(), name='softwarerequests-decline'),
    path('softwarerequests/<uuid:pk>/accept/', views.accept_button, name='softwarerequests-accept'),
    path('softwarerequests/<uuid:pk>/process/', views.process, name='softwarerequests-forward'),
    path('mysoftware/<int:pk>/', views.softwarelicensekeys, name='mysoftware-instances'),
]
#software manager
urlpatterns += [
    path('software/manage/', views.SoftwareManager.as_view(), name='software-manager'),
    path('software/create/', views.CreateSoftware.as_view(), name='software-create'),
    path('software/<int:pk>/update/', views.UpdateSoftware.as_view(), name='software-update'),
    path('software/<int:pk>/delete/', views.DeleteSoftware.as_view(), name='software-delete'),
]
#software instance manager
urlpatterns += [
    path('softwareinstance/create/', views.CreateSoftwareInstance.as_view(), name='softwareinstance-create'),
    path('softwareinstance/<uuid:pk>/update/', views.UpdateSoftwareInstance.as_view(), name='softwareinstance-update'),
    path('softwareinstance/<uuid:pk>/delete/', views.DeleteSoftwareInstance.as_view(), name='softwareinstance-delete'),
]



