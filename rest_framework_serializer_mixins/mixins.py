class DynamicFieldsMixin(object):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        read_only_fields = kwargs.pop('read_only_fields', None)

        super(DynamicFieldsMixin, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if read_only_fields is not None:
            for field_name in read_only_fields:
                field = self.fields.get(field_name, None)
                if field is not None:
                    field.read_only = True
