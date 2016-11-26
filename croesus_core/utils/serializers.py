from django.core.serializers.pyyaml import Serializer
from collections import OrderedDict
from decimal import Decimal
import yaml

try:
    from yaml import CSafeDumper as SafeDumper

except ImportError:
    from yaml import SafeDumper


class SafeDumper(SafeDumper):
    def represent_decimal(self, data):
        return self.represent_scalar('tag:yaml.org,2002:str', str(data))

    def represent_ordered_dict(self, data):
        return self.represent_mapping('tag:yaml.org,2002:map', data.items())


SafeDumper.add_representer(Decimal, SafeDumper.represent_decimal)
SafeDumper.add_representer(OrderedDict, SafeDumper.represent_ordered_dict)


class PrettyYamlSerializer(Serializer):
    def end_serialization(self):
        objects = [
            OrderedDict([
                ('model', i['model'],),
                ('pk', i['pk'],),
                ('fields', i['fields'],),
            ]) for i in self.objects]

        for index, obj in enumerate(objects):
            if index > 0:
                self.stream.write('\n')

            yaml.dump([obj], self.stream, Dumper=SafeDumper,
                      default_flow_style=False)
