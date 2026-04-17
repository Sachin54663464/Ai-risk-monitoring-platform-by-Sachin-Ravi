from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    PostViewSet,
    VoteViewSet,
    dashboard_view,
    investigations_view,
    mark_reviewed,
    toggle_suspicious,
    user_risk_trend,
    logs_view,
    analytics_view,
    settings_view,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'votes', VoteViewSet)

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('investigations/', investigations_view, name='investigations'),
    path('review/<int:user_id>/', mark_reviewed, name='mark_reviewed'),
    path('toggle/<int:user_id>/', toggle_suspicious, name='toggle_suspicious'),
    path('risk/<int:user_id>/', user_risk_trend, name='risk_trend'),
    path('logs/', logs_view, name='logs'),
    path('analytics/', analytics_view, name='analytics'),
    path('settings/', settings_view, name='settings'),
]

urlpatterns += router.urls