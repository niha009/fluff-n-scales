from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pet_list/', views.PetListView.as_view(), name='pet_list'),
    path('pet_detail/<int:pk>', views.PetDetail.as_view(), name='pet_detail'),
    path('pet/create/', views.PetCreate.as_view(), name='pet_create'),
    path('pet/<int:pk>/update/', views.PetUpdate.as_view(), name='pet_update'),
    path('pet/<int:pk>/delete/', views.pet_delete, name='pet_delete'),
    path('pet_images/', views.pet_image_list, name='pet_image_list'),
    path('pet/<int:pk>/like/', views.LikePet.as_view(), name='like_pet'),
    path('pet/<int:pk>/dislike/', views.DislikePet.as_view(), name='dislike_pet'),

]
