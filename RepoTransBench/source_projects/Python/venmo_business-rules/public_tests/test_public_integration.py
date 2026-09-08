from business_rules.engine import check_condition
from business_rules import export_rule_data
from business_rules.actions import rule_action, BaseActions
from business_rules.variables import BaseVariables, string_rule_variable, numeric_rule_variable, boolean_rule_variable
from business_rules.fields import FIELD_TEXT, FIELD_NUMERIC, FIELD_SELECT

from unittest import TestCase

class PublicVariables(BaseVariables):

    @string_rule_variable()
    def bar(self):
        return "bar"

    @numeric_rule_variable(label="Vinte")
    def twenty(self):
        return 20

    @boolean_rule_variable()
    def false_bool(self):
        return False

class PublicActions(BaseActions):

    @rule_action(params={"bar": FIELD_NUMERIC})
    def another_action(self, bar): pass

    @rule_action(label="yippee", params={"baz": FIELD_TEXT})
    def different_action(self, baz): pass

    @rule_action(params=[{'fieldType': FIELD_SELECT,
                          'name': 'qux',
                          'label': 'Qux',
                          'options': [
                            {'label': 'Choose Alpha', 'name': 'alpha'},
                            {'label': 'Choose Beta', 'name': 'beta'}
                        ]}])
    def more_select_action(self, qux): pass


class PublicIntegrationTests(TestCase):
    """ Public integration test, using the library as a user would (different data).
    """
    def test_true_boolean_variable_public(self):
        condition = {
            'name': 'false_bool',
            'operator': 'is_false',
            'value': ''
        }
        res = check_condition(condition, PublicVariables())
        self.assertTrue(res)

    def test_false_boolean_variable_public(self):
        condition = {
            'name': 'false_bool',
            'operator': 'is_true',
            'value': ''
        }
        res = check_condition(condition, PublicVariables())
        self.assertFalse(res)

    def test_check_true_condition_happy_path_public(self):
        condition = {'name': 'bar',
                     'operator': 'contains',
                     'value': 'a'}
        self.assertTrue(check_condition(condition, PublicVariables()))

    def test_check_false_condition_happy_path_public(self):
        condition = {'name': 'bar',
                     'operator': 'contains',
                     'value': 'z'}
        self.assertFalse(check_condition(condition, PublicVariables()))

    def test_check_incorrect_method_name_public(self):
        condition = {'name': 'bazzz',
                     'operator': 'equal_to',
                     'value': 'abc'}
        err_string = 'Variable bazzz is not defined in class PublicVariables'
        with self.assertRaisesRegex(AssertionError, err_string):
            check_condition(condition, PublicVariables())

    def test_check_incorrect_operator_name_public(self):
        condition = {'name': 'bar',
                     'operator': 'doesnt_exist',
                     'value': 'bar'}
        with self.assertRaises(AssertionError):
            check_condition(condition, PublicVariables())

    def test_export_rule_data_public(self):
        """ Ensure export_rule_data produces correct action/variable/operator data for new class/data """
        all_data = export_rule_data(PublicVariables(), PublicActions())
        self.assertEqual(all_data.get("actions"),
                [{"name": "another_action",
                  "label": "Another Action",
                  "params": [{'fieldType': 'numeric', 'label': 'Bar', 'name': 'bar'}]},
                 {"name": "different_action",
                  "label": "yippee",
                  "params": [{'fieldType': 'text', 'label': 'Baz', 'name': 'baz'}]},
                 {"name": "more_select_action",
                  "label": "More Select Action",
                  "params":[{'fieldType': FIELD_SELECT,
                             'name': 'qux',
                             'label': 'Qux',
                             'options': [
                                {'label': 'Choose Alpha', 'name': 'alpha'},
                                {'label': 'Choose Beta', 'name': 'beta'}
                            ]}]
                  }
                 ])

        self.assertEqual(all_data.get("variables"),
                         [{"name": "bar",
                           "label": "Bar",
                           "field_type": "string",
                           "options": []},
                          {"name": "twenty",
                           "label": "Vinte",
                           "field_type": "numeric",
                           "options": []},
                          {'name': 'false_bool',
                           'label': 'False Bool',
                           'field_type': 'boolean',
                           'options': []}])

        self.assertEqual(all_data.get("variable_type_operators"),
                         {'boolean': [{'input_type': 'none',
                             'label': 'Is False',
                             'name': 'is_false'},
                            {'input_type': 'none',
                             'label': 'Is True',
                             'name': 'is_true'}],
                           'numeric': [{'input_type': 'numeric',
                             'label': 'Equal To',
                             'name': 'equal_to'},
                            {'input_type': 'numeric', 'label': 'Greater Than', 'name': 'greater_than'},
                            {'input_type': 'numeric',
                             'label': 'Greater Than Or Equal To',
                             'name': 'greater_than_or_equal_to'},
                            {'input_type': 'numeric', 'label': 'Less Than', 'name': 'less_than'},
                            {'input_type': 'numeric',
                             'label': 'Less Than Or Equal To',
                             'name': 'less_than_or_equal_to'}],
                           'select': [{'input_type': 'select', 'label': 'Contains', 'name': 'contains'},
                            {'input_type': 'select',
                             'label': 'Does Not Contain',
                             'name': 'does_not_contain'}],
                           'select_multiple': [{'input_type': 'select_multiple',
                             'label': 'Contains All',
                             'name': 'contains_all'},
                            {'input_type': 'select_multiple',
                             'label': 'Is Contained By',
                             'name': 'is_contained_by'},
                            {'input_type': 'select_multiple',
                             'label': 'Shares At Least One Element With',
                             'name': 'shares_at_least_one_element_with'},
                            {'input_type': 'select_multiple',
                             'label': 'Shares Exactly One Element With',
                             'name': 'shares_exactly_one_element_with'},
                            {'input_type': 'select_multiple',
                             'label': 'Shares No Elements With',
                             'name': 'shares_no_elements_with'}],
                           'string': [{'input_type': 'text', 'label': 'Contains', 'name': 'contains'},
                            {'input_type': 'text', 'label': 'Ends With', 'name': 'ends_with'},
                            {'input_type': 'text', 'label': 'Equal To', 'name': 'equal_to'},
                            {'input_type': 'text',
                             'label': 'Equal To (case insensitive)',
                             'name': 'equal_to_case_insensitive'},
                            {'input_type': 'text', 'label': 'Matches Regex', 'name': 'matches_regex'},
                            {'input_type': 'none', 'label': 'Non Empty', 'name': 'non_empty'},
                            {'input_type': 'text', 'label': 'Starts With', 'name': 'starts_with'}]})