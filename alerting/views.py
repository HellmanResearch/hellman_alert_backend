import logging

from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.response import Response

from . import models as l_models
from . import serializers as l_serializers

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


logger = logging.getLogger(__name__)


class Subscribe(viewsets.ModelViewSet):
    queryset = l_models.Subscribe.objects.all()
    serializer_class = l_serializers.Subscribe


class Alert(viewsets.ReadOnlyModelViewSet):
    queryset = l_models.Alert.objects.all()
    serializer_class = l_serializers.Alert

    # def create(self, request, *args, **kwargs):
    #     logger.info("received a alert: ", request.data)
    #     # serializer = self.get_serializer(data=request.data)
    #     # serializer.is_valid(raise_exception=True)
    #     # self.perform_create(serializer)
    #     # headers = self.get_success_headers(serializer.data)
    #     return Response({}, 200)


