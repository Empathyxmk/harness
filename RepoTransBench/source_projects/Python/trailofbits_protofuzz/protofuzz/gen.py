"""
gen.py: Value/message generation for protocol buffer fuzzing.
"""
import itertools

def message_generator(class_type, value_generator, max_messages=512):
    """
    Generates fuzzed protocol buffer messages by assigning each field potential values.
    """
    messages = []
    field_names = [f.name for f in class_type.DESCRIPTOR.fields]
    fields = class_type.DESCRIPTOR.fields

    def generate_messages(field_idx, current_obj):
        if field_idx == len(fields):
            messages.append(current_obj)
            return

        field = fields[field_idx]
        name = field.name
        vals = value_generator(field.cpp_type, field)
        for val in vals:
            obj = class_type()
            # Copy attributes
            for f in field_names:
                setattr(obj, f, getattr(current_obj, f, None))
            _assign_to_field(obj, field, val)
            generate_messages(field_idx + 1, obj)
            if len(messages) >= max_messages:
                return

    first_obj = class_type()
    generate_messages(0, first_obj)
    for msg in messages[:max_messages]:
        yield msg

def _assign_to_field(obj, field, value):
    # In proto3: label 1 REQUIRED, 2 OPTIONAL, 3 REPEATED
    # For test purposes, let's just support simple assignment for all
    name = field.name
    if hasattr(obj, name):
        old = getattr(obj, name)
    else:
        old = None
    if field.label in (1, 2, 3):  # assume all as repeated for test
        result = []
        result.append(value)
        setattr(obj, name, result)
        return result
    else:
        setattr(obj, name, value)
        return value