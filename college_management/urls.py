from django.contrib import admin
from django.urls import path, include, re_path
from custom_admin import views as v1
from faculty import views as v2
from student import views as v3
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', v1.home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', v1.admin_login_page, name='login'),
    path('custom_admin/', include(('custom_admin.urls', 'custom_admin'))),
    path('custom_admin_dashboard/', v1.custom_admin_dashboard, name='custom_admin_dashboard'),

    path('faculty/', include(('faculty.urls', 'faculty'))),
    path('faculty_login/', v2.Faculty_login_page, name='faculty_login'),

    path('student/', include(('student.urls', 'student'))),
    path('student_login', v3.student_login, name='student_login'),
    path('student_logout/', v3.student_logout, name='student_logout'),
]

# ✅ Serve media files in development only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ⛔️ Catch-all must come last
urlpatterns += [
    re_path(r'^(?P<path>.*)$', v1.catch_all, name='catch_all'),
]
