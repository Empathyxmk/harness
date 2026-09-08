import json
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from celery.utils.time import maybe_make_aware

from redbeat import RedBeatSchedulerEntry
from redbeat.decoder import RedBeatJSONDecoder, from_timestamp, to_timestamp
from tests.basecase import RedBeatCase

CELERY_CONFIG_DEFAULT_KWARGS = {}


class PublicTestRedBeatEntry(RedBeatCase):
    def test_basic_save(self):
        e = self.create_entry(name='public_test', task='tasks.public_test')
        e.save()
        expected = {
            'name': 'public_test',
            'task': 'tasks.public_test',
            'schedule': e.schedule,
            'args': None,
            'kwargs': CELERY_CONFIG_DEFAULT_KWARGS,
            'options': {},
            'enabled': True,
        }
        expected_key = self.app.redbeat_conf.key_prefix + 'public_test'

        redis = self.app.redbeat_redis
        value = redis.hget(expected_key, 'definition')
        self.assertEqual(expected, json.loads(value, cls=RedBeatJSONDecoder))
        self.assertEqual(redis.zrank(self.app.redbeat_conf.schedule_key, e.key), 0)
        self.assertEqual(redis.zscore(self.app.redbeat_conf.schedule_key, e.key), e.score)

    def test_from_key_nonexistent_key(self):
        with self.assertRaises(KeyError):
            RedBeatSchedulerEntry.from_key('doesnotexist_public', self.app)

    def test_from_key_missing_meta(self):
        initial = self.create_entry(name='entry_missing_meta').save()
        loaded = RedBeatSchedulerEntry.from_key(initial.key, self.app)
        self.assertEqual(initial.task, loaded.task)
        self.assertIsNotNone(loaded.last_run_at)

    def test_next(self):
        initial = self.create_entry(name='public_next').save()
        now = self.app.now()
        now = maybe_make_aware(now)

        n = initial.next(last_run_at=now)

        self.assertIsNotNone(now.tzinfo)
        self.assertEqual(n.last_run_at, now)
        self.assertEqual(initial.total_run_count + 1, n.total_run_count)

        loaded = RedBeatSchedulerEntry.from_key(initial.key, app=self.app)
        self.assertEqual(loaded.last_run_at, now)
        self.assertEqual(loaded.total_run_count, initial.total_run_count + 1)

        redis = self.app.redbeat_redis
        self.assertEqual(redis.zscore(self.app.redbeat_conf.schedule_key, n.key), n.score)

    def test_next_only_update_last_run_at(self):
        initial = self.create_entry(name='public_next_only_update')

        n = initial.next(only_update_last_run_at=True)
        self.assertGreater(n.last_run_at, initial.last_run_at)
        self.assertEqual(n.total_run_count, initial.total_run_count)

    def test_delete(self):
        initial = self.create_entry(name='public_delete')
        initial.save()

        e = RedBeatSchedulerEntry.from_key(initial.key, app=self.app)
        e.delete()

        exists = self.app.redbeat_redis.exists(initial.key)
        self.assertFalse(exists)

        score = self.app.redbeat_redis.zrank(self.app.redbeat_conf.schedule_key, initial.key)
        self.assertIsNone(score)

    def test_due_at_never_run(self):
        entry = self.create_entry(name='public_never_run', last_run_at=datetime.min)

        before = entry._default_now()
        due_at = entry.due_at
        after = entry._default_now()

        self.assertLess(before, due_at)
        self.assertLess(due_at, after)

    def test_due_at(self):
        entry = self.create_entry(name='due_at_public')

        now = entry._default_now()

        entry.last_run_at = now
        due_at = entry.due_at

        self.assertLess(now, due_at)
        self.assertLess(due_at, now + entry.schedule.run_every)

    def test_due_at_overdue(self):
        last_run_at = self.app.now() - timedelta(hours=8)
        entry = self.create_entry(last_run_at=last_run_at, name='public_due_at_overdue')

        before = entry._default_now()
        due_at = entry.due_at

        self.assertLess(last_run_at, due_at)
        self.assertGreater(due_at, before)

    def test_score(self):
        run_every = 123 * 60
        entry = self.create_entry(run_every=run_every, name='public_score')
        entry = entry._next_instance()

        score = entry.score
        expected = entry.last_run_at + timedelta(seconds=run_every)
        expected = expected.replace(microsecond=0)
        expected = maybe_make_aware(expected)

        self.assertEqual(score, to_timestamp(expected))
        self.assertEqual(expected, from_timestamp(score))

    def test_generate_key(self) -> None:
        entry = self.create_entry(name="public_generate_key")

        key = entry.generate_key(app=self.app, name="another_public_name")

        self.assertEqual(key, "redbeat:another_public_name")

    @patch.object(RedBeatSchedulerEntry, "generate_key")
    def test_key(self, mock_generate_key: MagicMock) -> None:
        entry = self.create_entry(name="public_key")

        key = entry.key

        mock_generate_key.assert_called_once_with(app=self.app, name="public_key")

        self.assertEqual(key, mock_generate_key.return_value)