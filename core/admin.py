from django.contrib import admin
from .models import User, Post, Vote, AnomalyLog


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "trust_score", "is_suspicious", "created_at")
    list_filter = ("is_suspicious",)
    search_fields = ("username",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "risk_score", "created_at")
    search_fields = ("title",)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "is_upvote", "created_at")


@admin.register(AnomalyLog)
class AnomalyLogAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "anomaly_type", "severity", "created_at")
    list_filter = ("anomaly_type",)
