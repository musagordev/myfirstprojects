from django.urls import path, reverse_lazy
from . import views

app_name='pics'
urlpatterns = [
    path('', views.PicListView.as_view(), name='all'),
    path('pics/<int:pk>', views.PicDetailView.as_view(), name='pic_detail'),
    path('pics/create', views.PicCreateView.as_view(success_url=reverse_lazy('pics:all')), name='pic_create'),
    path('pics/<int:pk>/update', views.PicUpdateView.as_view(success_url=reverse_lazy('pics:all')), name='pic_update'),
    path('pics/<int:pk>/delete', views.PicDeleteView.as_view(success_url=reverse_lazy('pics:all')), name='pic_delete'),
    path('pics_picture/<int:pk>', views.stream_file, name='pic_picture'),
]

# We use reverse_lazy in urls.py to delay looking up the view until all the paths are defined
