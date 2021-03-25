from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index, name='home page'),
    path('delete_items/<int:pk>/', views.delete_items, name='delete_items'),
    path('user/', views.register,name='register-view'),
    path('login/', auth_views.LoginView.as_view(template_name='task/login.html') ,name='login'),
    path('logout/', views.logout, name='logout'),  
    path('customer/<customer_id>', views.customer_view, name="customer"),
    path('task/',views.task, name='task'),
    path('edit/<int:id>/',views.update,name="edit"),
    path('delete/<int:pk>/',views.delete,name='delete'),
    path('note/',views.note,name='note'),
    path('note_edit/<int:id>/',views.update_note,name="editnote"),
    path('note_delete/<int:id>/',views.delete_note,name='deletenote'),
    path('operation', views.operation, name="operation"),
    path('operation-note', views.operation_note, name="operation-note"),
    path('editText', views.editText, name="editText")

]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
