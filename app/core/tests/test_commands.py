"""
Test custom Django management commands.
"""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

# check function from BaseCommand, Command is the class we create in wait_for_db.py
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready."""
        patched_check.return_value = True

        call_command('wait_for_db')
 
        patched_check.assert_called_once_with(database=['default'])

    # patch will match from inside to outside with parameters left to right;
    # so first one is @patch('time.sleep') = patched_sleep,
    # seconde one is  @patch('core.management.commands.wait_for_db.Command.check') = patched_check
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        # it will raise 2 Psycopg2Error, then followed with 3 OperationalError, then return True
        # side_effect:This can either be a function to be called when the mock is called, 
        # an iterable or an exception (class or instance) to be raised.
        patched_check.side_effect = [Psycopg2Error] *2 * \
            [OperationalError] * 3 + [True]
        
        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count,6)
        patched_check.assert_called_with(database=['default'])
