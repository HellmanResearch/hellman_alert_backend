
import logging

from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model


from web3 import Account
from eth_account.messages import encode_defunct


from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import decorators
from rest_framework import exceptions
from rest_framework.decorators import action

from devops_django import decorators as dd_decorators

from . import models as l_models
from . import serializers as l_serializers
from . import objects as l_objects
from .objects import user as l_object_user

User = get_user_model()

logger = logging.getLogger("user")


class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = l_serializers.User
    queryset = l_models.User.objects.all()

    @action(methods=["get"], detail=False, url_path="signature-content")
    @dd_decorators.parameter("public_key", str, False, default=None)
    def get_signature_content(self, request, public_key, *args, **kwargs):
        # public_key = self.request.query_params.get("public_key")
        user, _ = l_object_user.UserObject.get_or_create(public_key)
        data = {
            "signature_content": user.signature_content
        }
        return Response(data)

    @action(methods=["get"], detail=False, url_path="login-signature")
    @dd_decorators.parameter("public_key", str, False, default=None)
    @dd_decorators.parameter("signature", str, False, default=None)
    def login_signature(self, request, public_key, signature, *args, **kwargs):
        user, is_new = l_object_user.UserObject.get_or_create(public_key)
        if is_new is True:
            raise exceptions.ParseError("The user doesn't exist, please get signature content first to create")

        message = encode_defunct(text="ssss")
        recovered_address = Account.recover_message(message, signature=signature)

        if recovered_address.lower() == public_key.lower():
            login(request, user)
            data = {
                "result": "login successful"
            }
            return Response(data)
        else:
            raise exceptions.ParseError("wrong signature")