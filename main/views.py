from typing import Any
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView , UpdateView
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.contrib.auth.hashers import make_password



from .models import *
from .forms import *


def CheckImgPath(request,url): 
    current_domain = request.get_host()
    if str(url).startswith("/main"):
        return  "http://" + current_domain + "/" + str(url)
    else:
        return url

class LoginView(LoginView):  # new
    template_name = 'loginView/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    authentication_form = LoginForm
    def get_success_url(self):
        return reverse_lazy('admin')
    
class DashboardView(LoginRequiredMixin, ListView):
    login_url = '/login/'

    model = ModAdmin
    template_name = 'dashboard/index.html'
    context_object_name = 'admin'


    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = ModAdmin.objects.filter(username=user.username)
        else:
            queryset = ModAdmin.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        request = self.request
        context = super().get_context_data(**kwargs)

        if user.is_authenticated:
            context["name"] = user.get_full_name()
            context["avatar"] = CheckImgPath(request, user.image)
        else:
            context["name"] = "Guest"
            context["avatar"] = None

        return context

class ProfileView(LoginRequiredMixin, ListView):
    login_url = '/login/'

    model = ModAdmin
    template_name = 'profile/index.html'
    context_object_name = 'admin'


    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = ModAdmin.objects.filter(username=user.username)
        else:
            queryset = ModAdmin.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        request = self.request
        context = super().get_context_data(**kwargs)

        if user.is_authenticated:
            context["user"] = user
            context["name"] = user.get_full_name()
            context["avatar"] = CheckImgPath(request, user.image)
        else:
            context["name"] = "Guest"
            context["avatar"] = None

        return context


class MemberView(LoginRequiredMixin, ListView):
    login_url = '/login/'

    model = ModAdmin
    template_name = 'member/index.html'
    context_object_name = 'member'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = ModAdmin.objects.filter(username=user.username)
        else:
            queryset = ModAdmin.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        request = self.request
        context = super().get_context_data(**kwargs)

        if user.is_authenticated:
            context["members"] = ModAdmin.objects.exclude(is_superuser=True).all()
            context["name"] = user.get_full_name()
            context["avatar"] = CheckImgPath(request, user.image)
            context["is_superuser"] = user.is_superuser
        else:
            context["members"] = None
        
        return context

class EventView(LoginRequiredMixin, ListView):
    login_url = '/login/'

    model = ModAdmin
    template_name = 'event/index.html'
    context_object_name = 'event'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = ModAdmin.objects.filter(username=user.username)
        else:
            queryset = ModAdmin.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        request = self.request
        context = super().get_context_data(**kwargs)

        if user.is_authenticated:
            context["events"] = Events.objects.all()
            context["name"] = user.get_full_name()
            context["avatar"] = CheckImgPath(request, user.image)
            context["is_superuser"] = user.is_superuser
            context["check_mssv"] = str(user.mssv)
        else:
            context["events"] = None
        
        return context

class PaperView(LoginRequiredMixin, ListView):
    login_url = '/login/'

    model = ModAdmin
    template_name = 'paper/index.html'
    context_object_name = 'paper'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = ModAdmin.objects.filter(username=user.username)
        else:
            queryset = ModAdmin.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        request = self.request
        context = super().get_context_data(**kwargs)

        if user.is_authenticated:
            context["papers"] = Paper.objects.all()
            context["name"] = user.get_full_name()
            context["avatar"] = CheckImgPath(request, user.image)
            context["is_superuser"] = user.is_superuser
            context["check_mssv"] = str(user.mssv)

        else:
            context["papers"] = None
        return context



class AddMemberView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = MemberForm
    model = ModAdmin
    template_name = 'formMember/index.html'
    success_url = reverse_lazy('addMember')

    def get_context_data(self, **kwargs):
        user = self.request.user
        request = self.request
        context = super().get_context_data(**kwargs)

        if user.is_authenticated:
            context["name"] = user.get_full_name()
            context["avatar"] = CheckImgPath(request, user.image)
        else:
            context["name"] = "Guest"
            context["avatar"] = None

        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.user = self.request.user

        instance = self.object
        print("co do day khong")
        instance.password = make_password(instance.password)

        instance.save()
        return super().form_valid(form)

class EditMemberView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = ModAdmin
    form_class = MemberForm
    template_name = 'formMember/index.html'
    success_url = reverse_lazy('member') 

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_superuser :
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse_lazy('member'))

    def get_object(self, queryset=None):
        pk = self.kwargs.get('id')
        return ModAdmin.objects.get(pk=pk)
    def get_context_data(self, **kwargs):
        user = self.request.user
        request = self.request
        context = super().get_context_data(**kwargs)

        if user.is_authenticated:
            context["name"] = user.get_full_name()
            context["avatar"] = CheckImgPath(request, user.image)
        else:
            context["name"] = "Guest"
            context["avatar"] = None

        return context
    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.user = self.request.user

        instance = self.object
        print("co do day khong")
        instance.password = make_password(instance.password)

        instance.save()
        return super().form_valid(form)

class DeleteMemberView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, id):
        if request.user.is_superuser:
            member = ModAdmin.objects.get(id_user=id)
            member.delete()
            return HttpResponseRedirect(reverse_lazy('member'))
        else:
            return HttpResponseRedirect(reverse_lazy('member'))

class SearchMemberView(LoginRequiredMixin, ListView):
    login_url = '/login/'

    model = ModAdmin
    template_name = 'member/index.html'
    context_object_name = 'member'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = ModAdmin.objects.filter(username=user.username)
        else:
            queryset = ModAdmin.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        request = self.request
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search')
        print(search)
        if user.is_authenticated:
            context["members"] = ModAdmin.objects.filter(full_name__icontains=search)
            context["name"] = user.get_full_name()
            context["avatar"] = CheckImgPath(request, user.image)
            context["is_superuser"] = user.is_superuser
        else:
            context["members"] = None
        
        return context

class AddEventView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = EventForm
    model = Events
    template_name = 'formEvent/index.html'
    success_url = reverse_lazy('event')

    def get_context_data(self, **kwargs):
        user = self.request.user
        request = self.request
        context = super().get_context_data(**kwargs)

        if user.is_authenticated:
            context["name"] = user.get_full_name()
            context["avatar"] = CheckImgPath(request, user.image)
        else:
            context["name"] = "Guest"
            context["avatar"] = None

        return context
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class EditEventView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Events
    form_class = EventForm
    template_name = 'formEvent/index.html'
    success_url = reverse_lazy('event') 

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_superuser :
            return super().dispatch(request, *args, **kwargs)
        try :
            event = Events.objects.get(id_event=self.kwargs.get('id'), id_user=user.id_user)
            if event is not None:
                return super().dispatch(request, *args, **kwargs)
        except Events.DoesNotExist:
            return HttpResponseRedirect(reverse_lazy('event'))

    def get_object(self, queryset=None):
        pk = self.kwargs.get('id')
        return Events.objects.get(pk=pk)
    def get_context_data(self, **kwargs):
        user = self.request.user
        request = self.request
        context = super().get_context_data(**kwargs)

        if user.is_authenticated:
            context["name"] = user.get_full_name()
            context["avatar"] = CheckImgPath(request, user.image)
        else:
            context["name"] = "Guest"
            context["avatar"] = None

        return context

class DeleteEventView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, id):
        if request.user.is_superuser:
            event = Events.objects.get(id_event=id)
            event.delete()
            return HttpResponseRedirect(reverse_lazy('event'))
        if request.user.is_authenticated:
            user = request.user
            try :
                event = Events.objects.get(id_event=id, id_user=user.id_user)
            except Events.DoesNotExist:
                return HttpResponseRedirect(reverse_lazy('event'))
            if event is not None: 
                event.delete()
            return HttpResponseRedirect(reverse_lazy('event'))
        else:
            return HttpResponseRedirect(reverse_lazy('event'))

class SearchEventView(LoginRequiredMixin, ListView):
    login_url = '/login/'

    model = ModAdmin
    template_name = 'event/index.html'
    context_object_name = 'event'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = ModAdmin.objects.filter(username=user.username)
        else:
            queryset = ModAdmin.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        request = self.request
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search')
        print(search)
        if user.is_authenticated:
            context["events"] = Events.objects.filter(name_event__icontains=search)
            context["name"] = user.get_full_name()
            context["avatar"] = CheckImgPath(request, user.image)
            context["is_superuser"] = user.is_superuser
        else:
            context["events"] = None
        
        return context

class AddPaperView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = PaperForm
    model = Paper
    template_name = 'formPaper/index.html'
    success_url = reverse_lazy('paper')

    def get_context_data(self, **kwargs):
        user = self.request.user
        request = self.request
        context = super().get_context_data(**kwargs)

        if user.is_authenticated:
            context["name"] = user.get_full_name()
            context["avatar"] = CheckImgPath(request, user.image)
        else:
            context["name"] = "Guest"
            context["avatar"] = None

        return context
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DeletePaperView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, id):
        if request.user.is_superuser:
            paper = Paper.objects.get(id_paper=id)
            paper.delete()
            return HttpResponseRedirect(reverse_lazy('paper'))
        if request.user.is_authenticated:
            user = request.user
            try :
                paper = Paper.objects.get(id_paper=id, id_user=user.id_user)
            except Paper.DoesNotExist:
                return HttpResponseRedirect(reverse_lazy('paper'))
            if paper is not None: 
                paper.delete()
            return HttpResponseRedirect(reverse_lazy('paper'))
        else:
            return HttpResponseRedirect(reverse_lazy('paper'))

class EditPaperView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    model = Paper
    form_class = PaperForm
    template_name = 'formPaper/index.html' 
    success_url = reverse_lazy('paper') 

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_superuser :
            return super().dispatch(request, *args, **kwargs)
        try :
            paper = Paper.objects.get(id_paper=self.kwargs.get('id'), id_user=user.id_user)
            if paper is not None:
                return super().dispatch(request, *args, **kwargs)
        except Paper.DoesNotExist:
            return HttpResponseRedirect(reverse_lazy('paper'))

    def get_object(self, queryset=None):
        pk = self.kwargs.get('id')
        
        return Paper.objects.get(pk=pk)
    def get_context_data(self, **kwargs):
        user = self.request.user
        request = self.request
        context = super().get_context_data(**kwargs)

        if user.is_authenticated:
            context["name"] = user.get_full_name()
            context["avatar"] = CheckImgPath(request, user.image)
        else:
            context["name"] = "Guest"
            context["avatar"] = None

        return context

class SearchPaperView(LoginRequiredMixin, ListView):
    login_url = '/login/'

    model = ModAdmin
    template_name = 'paper/index.html'
    context_object_name = 'paper'

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = ModAdmin.objects.filter(username=user.username)
        else:
            queryset = ModAdmin.objects.none()
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        request = self.request
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('search')
        print(search)
        if user.is_authenticated:
            context["papers"] = Paper.objects.filter(title__icontains=search)
            context["name"] = user.get_full_name()
            context["avatar"] = CheckImgPath(request, user.image)
            context["is_superuser"] = user.is_superuser
        else:
            context["papers"] = None
        
        return context


# API Views

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import JsonResponse
from main.serializers import *

class ModAdminAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        queryset = ModAdmin.objects.exclude(is_superuser=True).all()
        serializer = ModAdminSerializer(queryset, many=True)
        return Response(serializer.data)

class EventsAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        queryset = Events.objects.all()
        serializer = EventsSerializer(queryset, many=True)
        return Response(serializer.data)

class PaperAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        queryset = Paper.objects.all()  # Use .all() to retrieve all objects
        serializer = PaperSerializer(queryset, many=True)
        return Response(serializer.data)

class ModAdminIdAPI(APIView):
    permission_classes = [AllowAny]

    def get_object(self, id):
        try:
            return ModAdmin.objects.get(id_user=id)
        except ModAdmin.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id, format=None):
        queryset = self.get_object(id)
        serializer = ModAdminSerializer(queryset)
        return Response(serializer.data)

    # def put(self, request, id, format=None):
    #     queryset = self.get_object(id)
    #     serializer = ModAdminSerializer(queryset, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors)

    # def delete(self, request,id, format=None):
    #     queryset = self.get_object(id)
    #     queryset.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    
class AddMemberAPI(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request, format=None):
        serializer = ModAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SearchMemberAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, search, format=None):
        queryset = ModAdmin.objects.filter(full_name__icontains=search)
        serializer = ModAdminSerializer(queryset, many=True)
        return Response(serializer.data)

class EventIdAPI(APIView):
    permission_classes = [AllowAny]

    def get_object(self, id):
        try:
            return Events.objects.get(id_event=id)
        except Events.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id, format=None):
        queryset = self.get_object(id)
        serializer = EventsSerializer(queryset)
        return Response(serializer.data)

    # def put(self, request, id, format=None):
    #     queryset = self.get_object(id)
    #     serializer = EventsSerializer(queryset, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors)

    # def delete(self, request,id, format=None):
    #     queryset = self.get_object(id)
    #     queryset.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class AddEventAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = EventsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SearchEventAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, search, format=None):
        queryset = Events.objects.filter(name_event__icontains=search)
        serializer = EventsSerializer(queryset, many=True)
        return Response(serializer.data)

class PaperIdAPI(APIView):
    permission_classes = [AllowAny]

    def get_object(self, id):
        try:
            return Paper.objects.get(id_paper=id)
        except Paper.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id, format=None):
        queryset = self.get_object(id)
        serializer = PaperSerializer(queryset)
        return Response(serializer.data)

    # def put(self, request, id, format=None):
    #     queryset = self.get_object(id)
    #     serializer = PaperSerializer(queryset, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors)

    # def delete(self, request,id, format=None):
    #     queryset = self.get_object(id)
    #     queryset.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    
class AddPaperAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = PaperSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetInterestedPaperAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        queryset = Paper.objects.filter(interest = True)
        serializer = PaperSerializer(queryset, many=True)
        return Response(serializer.data)
    
class GetCountPaperAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        queryset = Paper.objects.all()
        total = queryset.count()
        queryset = Paper.objects.filter(institute__icontains = "YSC")
        YSC = queryset.count()
        queryset = Paper.objects.filter(institute__icontains = "FDSE")
        FDSE = queryset.count()
        queryset = Paper.objects.filter(institute__icontains = "Euréka")
        Euréka = queryset.count()
        
        return Response({"data" : {
            "total" : total,
            "YSC" : YSC,
            "FDSE" : FDSE,
            "Euréka" : Euréka
        }})

class SearchPaperAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, search, format=None):
        queryset = Paper.objects.filter(title__icontains=search)
        serializer = PaperSerializer(queryset, many=True)
        return Response(serializer.data)






