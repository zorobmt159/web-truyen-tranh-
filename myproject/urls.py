from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from users.views import (
    home, register, user_login, user_logout, comic_detail,
    search_results, search_suggestions, profile, pricing,
    checkout, confirm_payment, hot_comics, ranking,
    toggle_follow, followed_comics, genre_list,
    cancel_subscription, dismiss_coupon,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('comic/<int:pk>/', comic_detail, name='comic_detail'),
    path('search/', search_results, name='search_results'),
    path('search-suggestions/', search_suggestions, name='search_suggestions'),
    path('profile/', profile, name='profile'),
    path('pricing/', pricing, name='pricing'),
    path('checkout/<str:plan>/', checkout, name='checkout'),
    path('confirm-payment/', confirm_payment, name='confirm_payment'),
    path('cancel-subscription/', cancel_subscription, name='cancel_subscription'),
    path('dismiss-coupon/', dismiss_coupon, name='dismiss_coupon'),
    path('hot/', hot_comics, name='hot_comics'),
    path('ranking/', ranking, name='ranking'),
    path('comic/<int:pk>/follow/', toggle_follow, name='toggle_follow'),
    path('theo-doi/', followed_comics, name='followed_comics'),
    path('the-loai/', genre_list, name='the_loai'),
    path('the-loai/<str:tag_name>/', genre_list, name='genre_filter'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
