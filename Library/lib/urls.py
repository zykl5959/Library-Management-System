from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('showfine/<int:loan_id>/makepaymentbyloanid/',views.makepaymentbyloanid,name='makepaymentbyloadid'),
    path('showfine/<int:card_id>/makepaymentbycardid/',views.makepaymentbycardid,name='makepaymentbycardid'),
    path('showfine/',views.showfine,name='showfine'),
    path('updatefine/',views.updatefine,name='updatefine'),
    path('createborrower/',views.createborrower,name='createborrower'),
    path('createborrower/newborrower',views.newborrower,name='newborrower'),
    path('checkin/',views.checkin,name='checkin'),
    path('checkin/result/',views.checkinresult,name='checkinresult'),
    path('checkin/result/checkinfinish/',views.checkinfinish,name='checkinfinish'),
    path('search/', views.searchbook, name='searchbook'),
    path('search/result/',views.searchbookresult,name='result'),
    path('search/result/<int:book_id>/checkout/',views.checkout,name='checkout'),
    path('search/result/<int:book_id>/checkoutresult/',views.checkoutresult,name='checkoutresult'),
]