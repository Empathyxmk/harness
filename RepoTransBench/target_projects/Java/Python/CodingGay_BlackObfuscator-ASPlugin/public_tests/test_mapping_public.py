def create_mapping_class():
    class Mapping:
        def __init__(self):
            self.class_map = {}
            self.method_map = {}
            self.field_map = {}

        def put_class_mapping(self, class_name, obf_name):
            self.class_map[class_name] = obf_name

        def get_obfuscated_class_name(self, class_name):
            return self.class_map.get(class_name)

        def put_method_mapping(self, class_name, method_sig, obf_name):
            self.method_map[(class_name, method_sig)] = obf_name

        def get_obfuscated_method_name(self, class_name, method_sig):
            return self.method_map.get((class_name, method_sig))

        def put_field_mapping(self, class_name, field_name, obf_name):
            self.field_map[(class_name, field_name)] = obf_name

        def get_obfuscated_field_name(self, class_name, field_name):
            return self.field_map.get((class_name, field_name))

        def get_class_mapping(self):
            return self.class_map

    return Mapping

def test_put_and_get_different_data():
    Mapping = create_mapping_class()
    mapping = Mapping()
    class_name = "top.example2024.NewClass"
    obf_class_name = "aBcD_PUBLIC"
    mapping.put_class_mapping(class_name, obf_class_name)
    assert mapping.get_obfuscated_class_name(class_name) == obf_class_name

    method_name = "publicMethod2024()V"
    obf_method_name = "m2024"
    mapping.put_method_mapping(class_name, method_name, obf_method_name)
    assert mapping.get_obfuscated_method_name(class_name, method_name) == obf_method_name

    field_name = "publicField2024"
    obf_field_name = "f2024"
    mapping.put_field_mapping(class_name, field_name, obf_field_name)
    assert mapping.get_obfuscated_field_name(class_name, field_name) == obf_field_name

def test_to_map_different_data():
    Mapping = create_mapping_class()
    mapping = Mapping()
    mapping.put_class_mapping("ClassA2024", "XxYyZz")
    class_map = mapping.get_class_mapping()
    assert class_map["ClassA2024"] == "XxYyZz"
    assert "ClassA2024" in class_map