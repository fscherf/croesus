from django.db.models import QuerySet
from ..utils.shell import queryset_to_prettytable


class CroesusQueryset(QuerySet):
    PRETTYTABLE_FIELDS = []

    def to_prettytable(self, field_names=None, numbered=True,
                       number_offset=0):

        field_names = field_names or self.PRETTYTABLE_FIELDS

        if not field_names:
            raise ValueError

        return queryset_to_prettytable(self, field_names=field_names,
                                       numbered=numbered,
                                       number_offset=number_offset)

    def __repr__(self):
        return(self.to_prettytable().get_string())
