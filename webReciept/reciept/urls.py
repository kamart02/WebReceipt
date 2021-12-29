from django.urls import path
from . import views

urlpatterns = [
    path('', views.groupView, name='index'),
    path('group-new', views.addGroup, name = 'group-new'),
    path('profile/<int:group_id>', views.profile, name='profile'),
    path('profile/<int:group_id>/newTransaction', views.newTransaction, name='transaction-new'),
    path('group/<int:group_id>', views.recieptList, name='reciept-list'),
    path('reciept/<int:group_id>/<int:id>', views.recieptView, name='reciept-view'),
    path('reciept/<int:group_id>/<int:id>/manage', views.recieptManage, name='reciept-manage'),
    path('reciept/<int:group_id>/<int:id>/edit', views.recieptEdit, name='reciept-edit'),
    path('reciept/<int:group_id>/<int:id>/rm',views.removeRecieptConfirmation, name='reciept-remove'),
    path('reciept/<int:group_id>/<int:id>/rm/confirmation', views.removeReciept, name='reciept-remove-confirmed'),
    path('reciept/<int:group_id>/new', views.addReciept, name='reciept-add')
]