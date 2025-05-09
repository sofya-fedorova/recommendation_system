from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('button_click', views.button_click_view, name='button_click'),
    path('pageTest', views.pageTest, name='pageTest'),
    path('button_click_2', views.button_click_view_2, name='button_click_2'),
    path('resultPage', views.resultPage, name='resultPage'),
    path('button_click_3', views.button_click_view_3, name='button_click_3'),
    path('pageEnter', views.pageEnter, name='pageEnter'),
    path('button_enter_click', views.button_enter_click, name='button_enter_click'),
    path('addProgram', views.addProgram, name='addProgram'),
    path('upload_file', views.upload_file, name='upload_file'),
    path('pageResultReport', views.pageResultReport, name='pageResultReport'),
    path('download_results', views.download_results, name='download_results'),
]