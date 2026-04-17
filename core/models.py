from django.db import models
from django.utils import timezone
from datetime import timedelta


# =====================================
# USER MODEL
# =====================================

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    trust_score = models.FloatField(default=100.0)

    # Auto-detected flag
    is_suspicious = models.BooleanField(default=False)

    # Manual analyst review flag
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# =====================================
# POST MODEL
# =====================================

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    risk_score = models.FloatField(default=0.0)

    def __str__(self):
        return self.title


# =====================================
# VOTE MODEL (AI DETECTION ENGINE)
# =====================================

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_upvote = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        is_duplicate = Vote.objects.filter(
            user=self.user,
            post=self.post
        ).exists()

        super().save(*args, **kwargs)

        anomaly_triggered = False

        # -------------------------------
        # 1️⃣ Duplicate Vote Detection
        # -------------------------------
        if is_duplicate:
            self.user.trust_score = max(0, self.user.trust_score - 10)
            self.post.risk_score = min(100, self.post.risk_score + 5)

            AnomalyLog.objects.create(
                user=self.user,
                post=self.post,
                anomaly_type="DUPLICATE",
                severity=2
            )

            anomaly_triggered = True

        # -------------------------------
        # 2️⃣ Burst Voting Detection
        # -------------------------------
        one_minute_ago = timezone.now() - timedelta(minutes=1)

        recent_votes = Vote.objects.filter(
            user=self.user,
            created_at__gte=one_minute_ago
        ).count()

        if recent_votes >= 5:
            self.user.trust_score = max(0, self.user.trust_score - 20)
            self.post.risk_score = min(100, self.post.risk_score + 10)

            AnomalyLog.objects.create(
                user=self.user,
                post=self.post,
                anomaly_type="BURST",
                severity=3
            )

            anomaly_triggered = True

        # -------------------------------
        # 3️⃣ Auto Suspicious Flag
        # -------------------------------
        if self.user.trust_score < 50:
            self.user.is_suspicious = True

        # Save updated values
        if anomaly_triggered:
            self.user.save()
            self.post.save()

    def __str__(self):
        return f"{self.user.username} -> {self.post.title}"


# =====================================
# ANOMALY LOG MODEL
# =====================================

class AnomalyLog(models.Model):

    ANOMALY_TYPES = (
        ("DUPLICATE", "Duplicate Vote"),
        ("BURST", "Burst Voting"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    anomaly_type = models.CharField(max_length=20, choices=ANOMALY_TYPES)
    severity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.anomaly_type}"