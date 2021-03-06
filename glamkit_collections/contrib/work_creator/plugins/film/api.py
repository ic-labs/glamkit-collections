from rest_framework import serializers
from rest_framework import routers

from icekit.api.base_views import ModelViewSet

from ...api_serializers import MovingImageWork
from .models import Film as FilmModel, Format as FormatModel


VIEWNAME = 'api:film-api'


class Format(serializers.ModelSerializer):
    class Meta:
        model = FormatModel
        fields = (
            'title',
            'slug',
        )


class Film(MovingImageWork):
    formats = Format(
        many=True,
        read_only=True,
    )

    class Meta:
        model = FilmModel
        fields = MovingImageWork.Meta.fields + (
            # Relationships
            'formats',
        )
        extra_kwargs = dict(MovingImageWork.Meta.extra_kwargs, **{
            'url': {
                'lookup_field': 'pk',
                'view_name': '%s-detail' % VIEWNAME,
            },
        })
        writable_related_fields = MovingImageWork.Meta.writable_related_fields


class APIViewSet(ModelViewSet):
    """
    Film resource
    """
    queryset = FilmModel.objects.all() \
        .prefetch_related('creators', 'images')

    serializer_class = Film


router = routers.DefaultRouter()
router.register('film', APIViewSet, VIEWNAME)
