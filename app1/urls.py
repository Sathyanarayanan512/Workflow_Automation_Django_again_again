from django.urls import path
from . import views

urlpatterns=[
    # path('',views.loadregister,name='loadregister'),
    path('',views.home,name='home'),
    path('loadregister/',views.loadregister,name='loadregister'),
    path('userregister/',views.userregister,name='userregister'),
    path('userlogin/',views.userlogin,name='userlogin'),
    path('logout/',views.logout,name='logout'),
    path('loaddashboard/',views.loaddashboard,name='loaddashboard'),
    path('allemployees/',views.allemployees,name='allemployees'),
    path('addemployee/',views.addemployee,name='addemployee'),
    path('loadeditform/<int:user_id>/',views.loadeditform, name='loadeditform'),
    path('editemployee',views.editemployee,name='editemployee'),
    path('deleteemployee/<int:user_id>/',views.deleteemployee,name='deleteemployee'),
    path('createdrequests/<int:uid>/',views.createdrequests,name='createdrequests'),
    path('createrequestform/<int:uid>/',views.createrequestform,name='createrequestform'),
    path('createrequest/',views.createrequest,name='createrequest'),
    path('loadgenerateworkflow/<int:cr_id>/',views.loadgenerateworkflow,name='loadgenerateworkflow'),
    path('generateworkflowstep/<int:uid>/<int:cr_id>/',views.generateworkflowstep,name='generateworkflowstep'),
    path('removefromworkflow/<int:tw_id>/<int:cr_id>/',views.removefromworkflow,name='removefromworkflow'),
    path('finishmakingflow/<int:cr_id>/',views.finishmakingflow,name='finishmakingflow'),
    path('viewworkflow/<int:cr_id>/',views.viewworkflow,name='viewworkflow'),
    path('workrequestsforemployee/<int:uid>/',views.workrequestsforemployee,name='workrequestsforemployee'),
    path('approve/<int:uid>/<int:cr_id>/',views.approve,name='approve'),
]