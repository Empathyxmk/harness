from business_rules.variables import BaseVariables, rule_variable, boolean_rule_variable, numeric_rule_variable, string_rule_variable
from unittest import TestCase

class PublicBoolVars(BaseVariables):

    @boolean_rule_variable(label="Allowed")
    def allowed(self):
        return False

class PublicNumVars(BaseVariables):

    @numeric_rule_variable(label="Best Number")
    def best(self):
        return 42

class PublicStringVars(BaseVariables):

    @string_rule_variable(label="Artist Name")
    def artist(self):
        return "Mozart"

class PublicVariablesTest(TestCase):

    def test_get_all_boolean_variables_public(self):
        vars = PublicBoolVars.get_all_variables()
        self.assertEqual(len(vars), 1)
        self.assertEqual(vars[0]["name"], "allowed")
        self.assertEqual(vars[0]["label"], "Allowed")
        self.assertEqual(vars[0]["field_type"], "boolean")

    def test_get_all_numeric_variables_public(self):
        vars = PublicNumVars.get_all_variables()
        self.assertEqual(vars[0]["name"], "best")
        self.assertEqual(vars[0]["label"], "Best Number")
        self.assertEqual(vars[0]["field_type"], "numeric")

    def test_get_all_string_variables_public(self):
        vars = PublicStringVars.get_all_variables()
        self.assertEqual(vars[0]["name"], "artist")
        self.assertEqual(vars[0]["label"], "Artist Name")
        self.assertEqual(vars[0]["field_type"], "string")