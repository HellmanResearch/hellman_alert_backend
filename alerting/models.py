
from django.db import models
from django.contrib.auth import get_user_model

from prom import models as prom_models

User = get_user_model()


# class Rule(models.Model):
#     metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
#     display = models.CharField(max_length=20)
#
#     create_time = models.DateTimeField(auto_now_add=True)
#     update_time = models.DateTimeField(auto_now=True)


class Subscribe(models.Model):

    NOTIFICATION_TYPE = [
        ("email", "email"),
        ("discord", "discord"),
        ("webhook", "webhook"),
    ]
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, models.CASCADE, related_name="subscribe_set")
    metric = models.ForeignKey(prom_models.Metric, models.PROTECT)
    # rules = models.ManyToManyField(Rule)
    conditions = models.JSONField()

    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPE)
    notification_address = models.TextField()

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("name", "user"), )


class Alert(models.Model):
    subscribe = models.ForeignKey(Subscribe, models.PROTECT)
    user = models.ForeignKey(User, models.CASCADE, related_name="alert_set")
    metric = models.ForeignKey(prom_models.Metric, models.PROTECT)

    confirmed = models.BooleanField(default=False)
    confirm_time = models.DateTimeField(null=True, blank=True)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)