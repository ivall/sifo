from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view()),
    path('category/<category_name>', views.HomeView.as_view()),
    path('add_video/', views.AddVideoView.as_view()),
    path('video/<video_id>/', views.VideoView.as_view()),
    path('add_link/', views.AddLinkView.as_view()),
    path('panel/', views.PanelView.as_view()),
    path('video_action/', views.VideoAction.as_view()),
    path('link_action/', views.LinkAction.as_view()),
    path('search/', views.HomeView.as_view()),
    path('actualize_series/', views.ActualizeSeriesDataView.as_view()),
]
