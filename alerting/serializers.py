
from rest_framework import serializers

from . import models as l_models
from prom import models as prom_models

from django.db import models
from django.contrib.auth import get_user_model

from prom.metrics_rules.field import NameFiledMap

from rest_framework import exceptions

User = get_user_model()


class Subscribe(serializers.ModelSerializer):

    @staticmethod
    def c_get_conditions_serializer_cls(fields_attr):
        field_dict = {}
        for key, filed_attr in fields_attr.items():
            field_cls = NameFiledMap.get(filed_attr["type"])
            if field_cls is None:
                raise Exception('filed_attr["type"] not support')
            filed_attr.pop("type")
            field = field_cls(**filed_attr)
            field_dict[filed_attr["key"]] = field.generate_serializer_field()
        serializer_cls = type("DynamicSerializer", (serializers.Serializer,), field_dict)
        return serializer_cls

    def validate_conditions(self, value):
        metric_id = self.initial_data.get("metric")
        # fields_attr = metric.fields_attr

        if metric_id is None:
            raise exceptions.ValidationError("metric is required")
        try:
            metric = prom_models.Metric.objects.get(id=int(metric_id))
        except Exception as exc:
            raise exceptions.ValidationError(f"get metric from db error: {exc}")
        fields_attr = metric.fields_attr
        # fields_attr = self.validated_data["metric"].fields_attr
        serializer_cls = self.c_get_conditions_serializer_cls(fields_attr)
        serializer = serializer_cls(data=value)
        serializer.is_valid(raise_exception=True)
        return value

    # def validate(self, attrs):
    #     metric = attrs.get("metric")
    #     # fields_attr = metric.fields_attr
    #
    #     if metric is None:
    #         raise exceptions.ValidationError("metric is required")
    #     # try:
    #     #     metric = prom_models.Metric.objects.get(id=int(metric_id))
    #     # except Exception as exc:
    #     #     raise exceptions.ValidationError(f"get metric from db error: {exc}")
    #     fields_attr = metric.fields_attr
    #     # fields_attr = self.validated_data["metric"].fields_attr
    #     serializer_cls = self.c_get_conditions_serializer_cls(fields_attr)
    #     serializer = serializer_cls(data=attrs["conditions"])
    #     serializer.is_valid(raise_exception=True)

    # def validate_conditions(self, value):
    #     fields_attr = self.validated_data["metric"].fields_attr
    #     serializer_cls = self.c_get_conditions_serializer_cls(fields_attr)
    #     serializer = serializer_cls(data=value)
    #     serializer.is_valid(raise_exception=True)

    class Meta:
        model = l_models.Subscribe
        fields = "__all__"


class Alert(serializers.ModelSerializer):
    class Meta:
        model = l_models.Alert
        fields = "__all__"



