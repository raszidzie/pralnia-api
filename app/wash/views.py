from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Clothe, Wash
from wash import serializers

class BaseWashAttrViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.CreateModelMixin):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TagViewSet(BaseWashAttrViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

class ClotheViewSet(BaseWashAttrViewSet):
    queryset = Clothe.objects.all()
    serializer_class = serializers.ClotheSerializer

class WashViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WashSerializer
    queryset = Wash.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)