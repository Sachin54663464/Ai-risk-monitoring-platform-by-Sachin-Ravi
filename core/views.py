from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Post, Vote, AnomalyLog
from .serializers import UserSerializer, PostSerializer, VoteSerializer


# =========================
# DRF API VIEWSETS
# =========================

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


# =========================
# DASHBOARD VIEWS (HTML)
# =========================

@login_required
def dashboard_view(request):
    context = {
        "user_count": User.objects.count(),
        "request_count": Vote.objects.count(),
        "anomaly_count": AnomalyLog.objects.count(),
        "suspicious_count": User.objects.filter(trust_score__lt=50).count()
    }
    return render(request, "dashboard.html", context)


@login_required
def investigations_view(request):
    suspicious_users = User.objects.filter(trust_score__lt=50).order_by("trust_score")
    return render(request, "investigations.html", {
        "suspicious_users": suspicious_users
    })


@login_required
def mark_reviewed(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_reviewed = True
    user.save()
    return redirect("investigations")


@login_required
def toggle_suspicious(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_suspicious = not user.is_suspicious
    user.save()
    return redirect("investigations")


@login_required
def logs_view(request):
    logs = AnomalyLog.objects.all().order_by("-created_at")
    return render(request, "logs.html", {"logs": logs})


@login_required
def analytics_view(request):
    return render(request, "analytics.html")


@login_required
def settings_view(request):
    return render(request, "settings.html")


# =========================
# API ENDPOINTS (JSON ONLY)
# =========================

@api_view(['GET'])
def user_risk_trend(request, user_id):
    user = get_object_or_404(User, id=user_id)
    anomalies = AnomalyLog.objects.filter(user=user).order_by("created_at")

    data = [a.severity for a in anomalies]

    return Response({
        "username": user.username,
        "risk_history": data
    })