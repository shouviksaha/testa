from django.conf.urls import patterns, include, url
from reg.views import index,checklogin,student_reg,client_reg,activate_user,forgot_password,forgot_password_email,forgot_password_handler,new_password,change_password,change_password_handler,log_out
from quiz.views import test_sync,upload,take_test,test_apply,evaluate_test
from users.views import client_dashboard_student,student_bio,client_bio,student_test_landing,test_analysis,student_dashboard_ongoingtests,client_dashboard,client_dashboard_tests,student_dashboard_takentests,student_dashboard_appliedtests,student_dashboard_personal,student_dashboard_approvedtests,student_dashboard,student_applytest,student_dashboard_closedtests,student_dashboard_tests,student_test,student_dashboard_opentests,approve_test,jqgrid_handler,jqgrid_handler2
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testa.views.home', name='home'),
    # url(r'^testa/', include('testa.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
   url(r'^admin/', include(admin.site.urls)),	
   url(r'^$',index),
	url(r'^logout/$',log_out),
	url(r'^checklogin/$',checklogin),
	url(r'^client-dashboard/$',client_dashboard),
	url(r'^client-dashboard/client-tests/$',client_dashboard_tests),
	url(r'^client-dashboard/bio/$',client_bio),
	url(r'^client-dashboard/student/(?P<student_id>\d+)$',client_dashboard_student),
	url(r'^student-dashboard/bio/$',student_bio),
	url(r'^student-dashboard/personal/$',student_dashboard_personal),
	url(r'^student-dashboard/personal/applied/$',student_dashboard_appliedtests),
	url(r'^student-dashboard/tests/ongoing/$',student_dashboard_ongoingtests),
	url(r'^student-dashboard/tests/approved/$',student_dashboard_approvedtests),
	url(r'^student-dashboard/tests/taken/$',student_dashboard_takentests),
	url(r'^landing/(\w+)/(?P<test_key>[\w,-]+)$',student_test_landing),
	url(r'^student-dashboard/tests/analysis/(?P<test_id>\d+)$',test_analysis),
	url(r'^student-dashboard/$',student_dashboard),
	url(r'^student-dashboard/tests/$',student_dashboard_tests),
	url(r'^student-dashboard/tests/open-tests/$',student_dashboard_opentests),
	url(r'^student-dashboard/tests/closed-tests/$',student_dashboard_closedtests),
	url(r'^student-dashboard/tests/apply/(?P<test_id>\d+)/$',student_applytest),
	url(r'^student-reg/$',student_reg),
	url(r'^test-sync/$',test_sync),
	url(r'^apply/(?P<test_id>\d+)$',test_apply),
	url(r'^approve/$',approve_test),
	url(r'^start/(\w+)/(?P<test_key>[\w,-]+)/$',take_test),
	url(r'^start/(\w+)/(?P<test_key>[\w,-]+)/evaluate/$',evaluate_test),
	url(r'^client-reg/$',client_reg),
	url(r'^activate/(?P<a_string>\w{30})/$',activate_user),
	url(r'^forgot-password/$',forgot_password),
	url(r'^fp-email/$',forgot_password_email),
	url(r'^fp-string/(?P<fp_string>\w{30})/$',forgot_password_handler),
	url(r'^new-password/$',new_password),
	url(r'^change-password/$',change_password),
	url(r'^cp-handler/$',change_password_handler),
	url(r'^client-dashboard/upload-test/$',upload),
	url(r'^jqgrid-handler/$',jqgrid_handler),
	url(r'^jqgrid-handler2/$',jqgrid_handler2),
	url(r'^test/(\w+)/(?P<test_key>[\w,-]+)$',student_test),
	
)

urlpatterns += staticfiles_urlpatterns()