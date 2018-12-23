from django.conf.urls import url
from . import user_views, college_views

urlpatterns = [
    url(r'^register/',user_views.RegisterView),
    url(r'^login/',user_views.LoginView),
#    url(r'^user/',),
    url(r'^college/model/',college_views.CollegeView),
#    url(r'^team/model/',),
#    url(r'^event/model/',),
#    url(r'^event/rel_team/',),
#    url(r'^team/rel_player/',),
]