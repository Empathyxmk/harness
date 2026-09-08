from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_TEXT
from unittest import TestCase

class PublicActionsClass(BaseActions):

    @rule_action(label="Omega", params={"bar_foo": FIELD_TEXT})
    def bye_public(self, bar_foo):
        return f"bye {bar_foo}"

    def still_not_an_action_public(self):
        pass

class PublicActionsClassTestCase(TestCase):
    def test_get_all_actions_public(self):
        actions = PublicActionsClass.get_all_actions()
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]['name'], 'bye_public')
        self.assertEqual(actions[0]['label'], 'Omega')
        self.assertEqual(actions[0]['params'],
                         [{'fieldType': 'text', 'label': 'Bar Foo', 'name': 'bar_foo'}])

        # should work on an instance
        self.assertEqual(len(PublicActionsClass().get_all_actions()), 1)