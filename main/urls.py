from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView
from rest_framework_swagger.views import get_swagger_view
from rest_framework.schemas import get_schema_view
from . import views

from .views import *

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("login/", LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page='login'), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="admin"),
    path("profile/", ProfileView.as_view(), name="profile"),

    path("members/", MemberView.as_view(), name="member"),
    path('addMember/', AddMemberView.as_view(), name="addMember"),
    path('editMember/<int:id>', EditMemberView.as_view(), name="editMember"),
    path('deleteMember/<int:id>', DeleteMemberView.as_view(), name="deleteMember"),
    path('searchMember/', SearchMemberView.as_view(), name="searchMember"),

    path('events/', EventView.as_view(), name="event"),
    path('addEvent/', AddEventView.as_view(), name="addEvent"),
    path('deleteEvent/<int:id>', DeleteEventView.as_view(), name="deleteEvent"),
    path('editEvent/<int:id>', EditEventView.as_view(), name="editEvent"),
    path('searchEvent/', SearchEventView.as_view(), name="searchEvent"),

    path('papers/', PaperView.as_view(), name="paper"),
    path('addPaper/', AddPaperView.as_view(), name="addPaper"),
    path('editPaper/<int:id>', EditPaperView.as_view(), name="editPaper"),
    path('deletePaper/<int:id>', DeletePaperView.as_view(), name="deletePaper"),
    path('searchPaper/', SearchPaperView.as_view(), name="searchPaper"),


    # API URL
    path("api_schema/", get_schema_view(title='API Docs'), name="api_schema"),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger/swagger-ui.html',
        extra_context={'schema_url':'api_schema'}
    ), name='swagger-ui'),
    path('redoc/', TemplateView.as_view(
        template_name='swagger/redoc.html',
        extra_context={'schema_url':'api_schema'}
    ), name='redoc'),
    
    path('api/members/', ModAdminAPI.as_view(), name="api_member"),
    path('api/member/<int:id>', ModAdminIdAPI.as_view(), name="api_member"),
    path('api/addMember/', AddMemberAPI.as_view(), name="api_member"),
    path('api/search-member/<str:search>/', SearchMemberAPI.as_view(), name="api_member"),

    path('api/events/', EventsAPI.as_view(), name="api_event"),
    path('api/event/<int:id>', EventIdAPI.as_view(), name="api_event"),
    path('api/addEvent/', AddEventAPI.as_view(), name="api_event"),
    path('api/search-event/<str:search>/', SearchEventAPI.as_view(), name="api_event"),

    path('api/papers/', PaperAPI.as_view(), name="api_paper"),
    path('api/paper/<int:id>', PaperIdAPI.as_view(), name="api_paper"),
    path('api/addPaper/', AddPaperAPI.as_view(), name="api_paper"),
    path('api/get-interested-paper/', GetInterestedPaperAPI.as_view(), name="api_paper"),
    path('api/get-count-paper/', GetCountPaperAPI.as_view(), name="api_paper"),
    path('api/search-paper/<str:search>/', SearchPaperAPI.as_view(), name="api_paper"),
]
