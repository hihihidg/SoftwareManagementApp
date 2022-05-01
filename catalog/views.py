from urllib import request
from django.shortcuts import render
from .models import RequestingSoftware, Software, SoftwareType, SoftwareInstance
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Software
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse

import requests
import datetime
from catalog.forms import ApplyLicenseKeyForm
from django.views.generic.edit import FormView

def get_referer(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return None
    return referer

class MySoftwareByUser(LoginRequiredMixin, generic.ListView, PermissionRequiredMixin):
    permission_required = 'catalog.canmake'
    model = SoftwareInstance
    template_name='catalog/mysoftware.html'
    paginate_by = 10
    def get_queryset(self):
        return SoftwareInstance.objects.order_by('software').order_by('renewal_date')
        
class AvailableSoftwareByUser(LoginRequiredMixin, generic.ListView):
    model = Software
    template_name='catalog/availablesoftware.html'
    paginate_by = 10
    def get_queryset(self):
        return Software.objects.order_by('title')

class SoftwareRequestsManager(LoginRequiredMixin, generic.ListView, PermissionRequiredMixin):
    permission_required = 'catalog.canmake'
    model = RequestingSoftware
    template_name='catalog/requstsoftwaremanager.html'
    paginate_by = 10
    def get_queryset(self):
        return RequestingSoftware.objects.order_by('send_date')

#manage software
class SoftwareManager(LoginRequiredMixin, generic.ListView, PermissionRequiredMixin):
    permission_required = 'catalog.canmake'
    model = Software
    template_name='catalog/softwaremanager.html'
    paginate_by = 10
    def get_queryset(self):
        return Software.objects.order_by('title')
        
class CreateSoftware(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
    permission_required = 'catalog.canmake'
    model = Software
    fields = ['title', 'description']
    success_url = reverse_lazy('software-manager')

class UpdateSoftware(LoginRequiredMixin,UpdateView, PermissionRequiredMixin):
    permission_required = 'catalog.canmake'
    model = Software
    success_url = reverse_lazy('software-manager')
    fields = ['title', 'description']

class DeleteSoftware(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    permission_required = 'catalog.canmake'
    model = Software
    success_url = reverse_lazy('software-manager')


#manage software instance
class CreateSoftwareInstance(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
    permission_required = 'catalog.canmake'
    model = SoftwareInstance
    fields = ['license_key', 'renewal_date', 'renewal_cost']
    success_url = reverse_lazy('mysoftware')

    def form_valid(self, form):
        return super(CreateSoftwareInstance, self).form_valid(form)

class UpdateSoftwareInstance(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    permission_required = 'catalog.canmake'
    model = SoftwareInstance
    fields = ['license_key', 'renewal_date', 'renewal_cost', 'status', 'user']
    success_url = reverse_lazy('mysoftware')

class DeleteSoftwareInstance(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    permission_required = 'catalog.canmake'
    model = SoftwareInstance
    success_url = reverse_lazy('mysoftware')

    




class SoftwareDetailView(LoginRequiredMixin, generic.DetailView):
    model = Software

class SoftwareRequestsDetailView(LoginRequiredMixin, generic.DetailView):
    model = RequestingSoftware

class CreateSoftwareRequest (LoginRequiredMixin, CreateView, PermissionRequiredMixin):
    template_name='catalog/requestingsoftware_form.html'
    permission_required = 'catalog.canmake'
    model = RequestingSoftware
    fields = ['name', 'email', 'department', 'software', 'reason']    
    success_url = reverse_lazy('softwarerequest-create')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateSoftwareRequest, self).form_valid(form)

class DeleteRequestingSoftware(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    permission_required = 'catalog.canmake'
    model = RequestingSoftware
    success_url = reverse_lazy('softwarerequests-manager')

@login_required
@permission_required('catalog.canmake', raise_exception=True)
def accept_button(request, pk):
    requestingsoftware_instance = get_object_or_404(RequestingSoftware, pk=pk)
    context = {
        'requestingsoftware_instance': requestingsoftware_instance,
    }
    
    request.session['RequestingSoftware'] = str(requestingsoftware_instance.id)

    return render(request, 'catalog/requestingsoftware_confirm_accept.html',context)
    
@login_required
@permission_required('catalog.canmake', raise_exception=True)
def process(request, pk):
    if not get_referer(request):
        return HttpResponse('<h1>Page not found</h1>')
    Softwarerequest = RequestingSoftware.objects.get(id=request.session['RequestingSoftware'])
    del request.session['RequestingSoftware']
    softwareinstance = get_object_or_404(SoftwareInstance, pk=pk)
    softwareinstance.user = Softwarerequest.user
    softwareinstance.status = 'u'
    softwareinstance.save()
    Softwarerequest.delete()
    return redirect('softwarerequests-manager')

@login_required
@permission_required('catalog.canmake', raise_exception=True)
def softwarelicensekeys(request, pk):
    software = get_object_or_404(Software, pk=pk)

    context = {
        'software' : software,
        'softwareinstance_list': software.softwareinstance_set.all,
    }
    return render(request, 'catalog/mysoftware.html',context)

"""
def accept_button(request, pk):
    requestingsoftware_instance = get_object_or_404(RequestingSoftware, pk=pk)

    if request.method == 'POST':
        form = ApplyLicenseKeyForm(request.POST)
        if form.is_valid():
            requestingsoftware_instance = get_object_or_404(RequestingSoftware, pk=pk)
            requestingsoftware_instance.save()
            requestingsoftware_instance.delete()
            return redirect('softwarerequests-manager')
    else:
        form = ApplyLicenseKeyForm(requestingsoftware_instance.software)

    context = {
        'form': form,
        'requestingsoftware_instance': requestingsoftware_instance,
    }

    return render(request, 'catalog/requestingsoftware_confirm_accept.html',context)

"""