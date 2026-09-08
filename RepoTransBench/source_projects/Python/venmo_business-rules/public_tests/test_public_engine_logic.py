from business_rules import engine
from business_rules.variables import BaseVariables
from business_rules.operators import StringType
from business_rules.actions import BaseActions

from mock import patch, MagicMock
from unittest import TestCase


class PublicEngineTests(TestCase):

    ###
    ### Run
    ###

    @patch.object(engine, 'run')
    def test_run_all_some_rule_triggered_public(self, *args):
        ruleA = {'conditions': 'condA', 'actions': 'actionX'}
        ruleB = {'conditions': 'condB', 'actions': 'actionY'}
        variables = BaseVariables()
        actions = BaseActions()

        def return_actionA(rule, *args, **kwargs):
            return rule['actions'] == 'actionX'
        engine.run.side_effect = return_actionA

        result = engine.run_all([ruleA, ruleB], variables, actions)
        self.assertTrue(result)
        self.assertEqual(engine.run.call_count, 2)

        engine.run.reset_mock()
        result = engine.run_all([ruleB, ruleA], variables, actions)
        self.assertTrue(result)
        self.assertEqual(engine.run.call_count, 2)

    @patch.object(engine, 'run', return_value=True)
    def test_run_all_stop_on_first_public(self, *args):
        ruleX = {'conditions': 'condX', 'actions': 'actionP'}
        ruleY = {'conditions': 'condY', 'actions': 'actionQ'}
        variables = BaseVariables()
        actions = BaseActions()

        result = engine.run_all([ruleX, ruleY], variables, actions, stop_on_first_trigger=True)
        self.assertEqual(result, True)
        self.assertEqual(engine.run.call_count, 1)
        engine.run.assert_called_once_with(ruleX, variables, actions)

    @patch.object(engine, 'check_conditions_recursively', return_value=True)
    @patch.object(engine, 'do_actions')
    def test_run_that_triggers_rule_public(self, *args):
        rule = {'conditions': 'abc', 'actions': 'xyz'}
        variables = BaseVariables()
        actions = BaseActions()

        result = engine.run(rule, variables, actions)
        self.assertEqual(result, True)
        engine.check_conditions_recursively.assert_called_once_with(rule['conditions'], variables)
        engine.do_actions.assert_called_once_with(rule['actions'], actions)

    @patch.object(engine, 'check_conditions_recursively', return_value=False)
    @patch.object(engine, 'do_actions')
    def test_run_that_doesnt_trigger_rule_public(self, *args):
        rule = {'conditions': 'abc', 'actions': 'xyz'}
        variables = BaseVariables()
        actions = BaseActions()

        result = engine.run(rule, variables, actions)
        self.assertEqual(result, False)
        engine.check_conditions_recursively.assert_called_once_with(rule['conditions'], variables)
        self.assertEqual(engine.do_actions.call_count, 0)

    @patch.object(engine, 'check_condition', return_value=True)
    def test_check_all_conditions_with_all_true_public(self, *args):
        conditions = {'all': [{'x1': ''}, {'x2': ''}]}
        variables = BaseVariables()

        result = engine.check_conditions_recursively(conditions, variables)
        self.assertEqual(result, True)
        self.assertEqual(engine.check_condition.call_count, 2)
        engine.check_condition.assert_called_with({'x2': ''}, variables)

    @patch.object(engine, 'check_condition', return_value=False)
    def test_check_all_conditions_with_all_false_public(self, *args):
        conditions = {'all': [{'y1': ''}, {'y2': ''}]}
        variables = BaseVariables()

        result = engine.check_conditions_recursively(conditions, variables)
        self.assertEqual(result, False)
        engine.check_condition.assert_called_once_with({'y1': ''}, variables)

    def test_check_all_condition_with_no_items_fails_public(self):
        with self.assertRaises(AssertionError):
            engine.check_conditions_recursively({'all': []}, BaseVariables())

    @patch.object(engine, 'check_condition', return_value=True)
    def test_check_any_conditions_with_all_true_public(self, *args):
        conditions = {'any': [{'z1': ''}, {'z2': ''}]}
        variables = BaseVariables()

        result = engine.check_conditions_recursively(conditions, variables)
        self.assertEqual(result, True)
        engine.check_condition.assert_called_once_with({'z1': ''}, variables)

    @patch.object(engine, 'check_condition', return_value=False)
    def test_check_any_conditions_with_all_false_public(self, *args):
        conditions = {'any': [{'q1': ''}, {'q2': ''}]}
        variables = BaseVariables()

        result = engine.check_conditions_recursively(conditions, variables)
        self.assertEqual(result, False)
        self.assertEqual(engine.check_condition.call_count, 2)
        engine.check_condition.assert_called_with({'q2': ''}, variables)

    def test_check_any_condition_with_no_items_fails_public(self):
        with self.assertRaises(AssertionError):
            engine.check_conditions_recursively({'any': []}, BaseVariables())

    def test_check_all_and_any_together_public(self):
        conditions = {'any': [], 'all': []}
        variables = BaseVariables()
        with self.assertRaises(AssertionError):
            engine.check_conditions_recursively(conditions, variables)

    @patch.object(engine, 'check_condition')
    def test_nested_all_and_any_public(self, *args):
        conditions = {'all': [
            {'any': [{'name': 101}, {'name': 202}]},
            {'name': 303}]}
        bv = BaseVariables()

        def side_effect(condition, _):
            return condition['name'] in [202, 303]
        engine.check_condition.side_effect = side_effect

        engine.check_conditions_recursively(conditions, bv)
        self.assertEqual(engine.check_condition.call_count, 3)
        engine.check_condition.assert_any_call({'name': 101}, bv)
        engine.check_condition.assert_any_call({'name': 202}, bv)
        engine.check_condition.assert_any_call({'name': 303}, bv)

    def test_check_operator_comparison_public(self):
        string_type = StringType('public string')
        with patch.object(string_type, 'starts_with', return_value=True):
            result = engine._do_operator_comparison(
                    string_type, 'starts_with', 'pub')
            self.assertTrue(result)
            string_type.starts_with.assert_called_once_with('pub')

    def test_do_actions_public(self):
        actions = [
            {'name': 'my_action1'},
            {'name': 'my_action2', 'params': {'paramX': 'bar', 'paramY': 25}}
        ]
        defined_actions = BaseActions()
        defined_actions.my_action1 = MagicMock()
        defined_actions.my_action2 = MagicMock()

        engine.do_actions(actions, defined_actions)
        defined_actions.my_action1.assert_called_once_with()
        defined_actions.my_action2.assert_called_once_with(paramX='bar', paramY=25)