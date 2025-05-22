from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'ads', views.AdViewSet)

urlpatterns = [
    path('', views.AdListView.as_view(), name='ad_list'),
    path('ad/<int:pk>/', views.AdDetailView.as_view(), name='ad_detail'),
    path('ad/new/', views.AdCreateView.as_view(), name='ad_create'),
    path('ad/<int:pk>/edit/', views.AdUpdateView.as_view(), name='ad_update'),
    path('ad/<int:pk>/delete/', views.AdDeleteView.as_view(), name='ad_delete'),
    path('ad/<int:ad_id>/propose/', views.create_exchange_proposal, name='create_exchange_proposal'),
    path('api/', include(router.urls)),
] 