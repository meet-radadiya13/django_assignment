from django.core.serializers.json import DjangoJSONEncoder

from authentication.models import User


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        print("defaulting to")
        if isinstance(obj, User):
            print("if condi")
            return str(obj)
        return super().default(obj)
