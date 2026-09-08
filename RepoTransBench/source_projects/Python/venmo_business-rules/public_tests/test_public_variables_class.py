from business_rules.variables import BaseVariables, rule_variable
from business_rules.operators import StringType
from unittest import TestCase

class PublicVariablesClassTests(TestCase):
    """ Public test methods on classes that inherit from BaseVariables, using different test data """

    def test_base_has_no_variables_public(self):
        self.assertEqual(len(BaseVariables.get_all_variables()), 0)

    def test_get_all_variables_public(self):
        """ Returns a dictionary listing all the functions on the class that
        have been decorated as variables, with some of the data about them.
        """
        class PublicSomeVariables(BaseVariables):

            @rule_variable(StringType, label="Public Rule Label")
            def another_rule(self):
                return "different"

            def non_rule_func(self):
                return "should not be a variable"

        vars = PublicSomeVariables.get_all_variables()
        self.assertEqual(len(vars), 1)
        self.assertEqual(vars[0]['name'], 'another_rule')
        self.assertEqual(vars[0]['label'], 'Public Rule Label')
        self.assertEqual(vars[0]['field_type'], 'string')
        self.assertEqual(vars[0]['options'], [])

        # should work on an instance of the class too
        self.assertEqual(len(PublicSomeVariables().get_all_variables()), 1)