from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('generate', views.generate, name="generate"),
    path('analyse', views.analyse, name="analyse"),
    path('comments', views.comments, name="comments"),
    path('positive-comments/<int:data_id>/', views.Positivecomments, name="positive-comments"),
    path('negative-comments/<int:data_id>/', views.Negativecomments, name="negative-comments"),
    path('all-comments/<int:data_id>/', views.Allcomments,name="all-comments"),
    path('success/<int:data_id>/', views.success, name="success"),
]

