from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('groups', views.groupView, name='groupView'),
    path('groups/group-new', views.addGroup, name = 'group-new'),
    path('group/<int:group_id>/transactions', views.transactionView, name='transaction-view'),
    path('group/<int:group_id>', views.recieptList, name='reciept-list'),
    path('reciept/<int:group_id>/<int:reciept_id>', views.recieptView, name='reciept-view'),
    path('reciept/<int:group_id>/<int:reciept_id>/manage', views.recieptManage, name='reciept-manage'),
    path('reciept/<int:group_id>/<int:reciept_id>/edit', views.recieptEdit, name='reciept-edit'),
    path('reciept/<int:group_id>/<int:reciept_id>/rm',views.removeRecieptConfirmation, name='reciept-remove'),
    path('reciept/<int:group_id>/<int:reciept_id>/rm/confirmation', views.removeReciept, name='reciept-remove-confirmed'),
    path('reciept/<int:group_id>/new', views.addReciept, name='reciept-add'),
    path('accounts/login/', views.loginView, name='login'),
    path('accounts/logout', views.logoutMethod, name='logout'),
    path('accounts/signup', views.signupView, name='signup'),
]