import json
import logging

from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from . import models as l_models
from . import serializers as l_serializers
from rest_framework import viewsets

logger = logging.getLogger(__name__)


class MetricGroup(viewsets.ReadOnlyModelViewSet):
    queryset = l_models.MetricGroup.objects.all()
    serializer_class = l_serializers.MetricGroup


class Metric(viewsets.ModelViewSet):
    queryset = l_models.Metric.objects.all()
    serializer_class = l_serializers.Metric


# class Rule(viewsets.GenericViewSet):
#     pass


class Alert(viewsets.GenericViewSet):
    queryset = l_models.Alert.objects.all()
    serializer_class = l_serializers.PromAlert

    def create(self, request, *args, **kwargs):
        body_content = json.dumps(request.data)
        logger.info("received a alert body_content: ", body_content)
        return Response({}, 200)
