from rest_framework import routers
from rest_framework import serializers

from icekit.api.base_views import ModelViewSet

from ...api_serializers import Creator
from .models import OrganizationCreator as OrganizationCreatorModel


VIEWNAME = 'api:organization-api'


class Organization(Creator):
    type = serializers.SerializerMethodField()
    type_plural = serializers.SerializerMethodField()

    class Meta:
        model = OrganizationCreatorModel
        fields = Creator.Meta.fields + (
            'type',
            'type_plural',
        )
        extra_kwargs = dict(Creator.Meta.extra_kwargs, **{
            'url': {
                'lookup_field': 'pk',
                'view_name': '%s-detail' % VIEWNAME,
            }
        })
        writable_related_fields = Creator.Meta.writable_related_fields

    def get_type(self, obj):
        return obj.get_type()

    def get_type_plural(self, obj):
        return obj.get_type_plural()


class APIViewSet(ModelViewSet):
    """
    Organization resource.
    """
    queryset = OrganizationCreatorModel.objects.all()
    serializer_class = Organization


router = routers.DefaultRouter()
router.register('organization', APIViewSet, VIEWNAME)
