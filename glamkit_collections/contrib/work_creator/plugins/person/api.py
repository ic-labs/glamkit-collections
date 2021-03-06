from rest_framework import routers

from icekit.api.base_serializers import ModelSubSerializer
from icekit.api.base_views import ModelViewSet

from ...api_serializers import Creator
from .models import PersonCreator as PersonCreatorModel


VIEWNAME = 'api:person-api'


class PersonName(ModelSubSerializer):
    class Meta:
        model = PersonCreatorModel
        source_prefix = 'name_'
        fields = (
            'name_full',
            'name_display',
            'name_sort',
            'name_given',
            'name_family',
        )
        extra_kwargs = {
            # Name fields derived from `name_full` are not required
            'name_display': {
                'required': False,
            },
            'name_sort': {
                'required': False,
            },
        }


class LifeInfo(ModelSubSerializer):
    class Meta:
        model = PersonCreatorModel
        source_prefix = 'life_info_'
        fields = (
            'life_info_birth_date_display',
            'life_info_birth_date_edtf',
            'life_info_birth_place',
            'life_info_birth_place_historic',
            'life_info_death_date_display',
            'life_info_death_date_edtf',
            'life_info_death_place',
        )


class Background(ModelSubSerializer):
    class Meta:
        model = PersonCreatorModel
        source_prefix = 'background_'
        fields = (
            'background_ethnicity',
            'background_nationality',
            'background_neighborhood',
            'background_city',
            'background_state_province',
            'background_country',
            'background_continent',
        )


class Person(Creator):
    name = PersonName(
        help_text="Parts and forms of the Artist's name",
    )
    life_info = LifeInfo(
        required=False,
        help_text="Birth and death dates and places",
    )
    background = Background(
        required=False,
        help_text="Ethnicity, nationality and culture",
    )

    class Meta:
        model = PersonCreatorModel
        fields = tuple(
            # Use Creator field names except for those grouped under PersonName
            f for f in Creator.Meta.fields
            if f not in PersonName.Meta.fields
        ) + (
            'name',
            'life_info',
            'background',
        )
        extra_kwargs = {
            'url': {
                'lookup_field': 'pk',
                'view_name': '%s-detail' % VIEWNAME,
            },
            # Slug field derived from `name_full` is not required
            'slug': {
                'required': False,
            },
        }
        writable_related_fields = Creator.Meta.writable_related_fields


class APIViewSet(ModelViewSet):
    """
    Artist resource.
    """
    queryset = PersonCreatorModel.objects.all()
    serializer_class = Person
    ordering_fields = (
            'name_display',
            'name_sort',
            'name_given',
            'name_family',
            'background_country',
            'background_continent',
    )


router = routers.DefaultRouter()
router.register('person', APIViewSet, VIEWNAME)
