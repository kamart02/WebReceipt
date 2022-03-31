from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('groups', views.groupView, name='groupView'),
    path('groups/group-new', views.addGroup, name = 'group-new'),
    path('group/<int:group_id>/transactions', views.transactionView, name='transaction-view'),
    path('group/<int:group_id>', views.receiptList, name='receipt-list'),
    path('receipt/<int:group_id>/<int:receipt_id>', views.receiptView, name='receipt-view'),
    path('receipt/<int:group_id>/<int:receipt_id>/manage', views.receiptManage, name='receipt-manage'),
    path('receipt/<int:group_id>/<int:receipt_id>/edit', views.receiptEdit, name='receipt-edit'),
    path('receipt/<int:group_id>/<int:receipt_id>/rm',views.removereceiptConfirmation, name='receipt-remove'),
    path('receipt/<int:group_id>/<int:receipt_id>/rm/confirmation', views.removereceipt, name='receipt-remove-confirmed'),
    path('receipt/<int:group_id>/new', views.addreceipt, name='receipt-add'),
    path('accounts/login/', views.loginView, name='login'),
    path('accounts/logout', views.logoutMethod, name='logout'),
    path('accounts/signup', views.signupView, name='signup'),
]