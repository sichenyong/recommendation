from django.urls import path
from adminapp import views

urlpatterns = [
    path('',views.loginPage, name="adminLoginpage"),
    path('login',views.login,name="adminLogin"),
    #用户
    path('dashboard', views.dashboard, name="adminDashboard"),
    path('sysuser0',views.getSysUser0, name="getsysuser0"),
    path('sysdashboard',views.sys1user, name="sys1user"),
    path('sysuser1',views.getSysUser1, name="getsysuser1"),
    path('usereditPage/<int:user_id>',views.usereditPage, name="usereditPage"),
    path('doeditUser',views.doeditUser,name="doeditUser"),
    path('userdel/<int:user_id>',views.userdel, name="userdel"),
    path('usersearch',views.usersearch,name="usersearch"),
    path('adduserPage',views.adduserPage,name="adduserPage"),
    path('doadduser',views.doadduser,name="doadduser"),
    path('findexist',views.userisexist,name="userisexist"),
    path('logout',views.logout,name="adminlogout"),
    path('adminPage',views.adminPage,name="adminPage"),

    #分页浏览地点信息
    path('venuedashboard/<int:pIndex>', views.venueDashboard, name="venueDashboard"),
    path('venueedit/<int:venue_id>',views.editvenue,name="editvenue"),
    path('dovenueedit',views.doeditvenue,name="doeditvenue"),
    path("delvenue/<int:venue_id>",views.delvenue, name="delvenue"),
    path("venuesearch",views.venuesearch, name="venuesearch"),
    path("venuedashboard/addvenue",views.addvenue,name="addvenue"),
    path("venuedashboard/doaddvenue",views.doaddvenue,name="doaddvenue"),
]