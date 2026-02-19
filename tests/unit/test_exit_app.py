"""
Unit tests for Exit App CLI command.
Tests all exit_app() function functionality, confirmation, and cleanup.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.cli.exit_app import exit_app
from src.lib.utils import display_error, display_success, pause, get_confirmation, clear_screen


class TestExitAppCLI:
    """Unit tests for Exit App CLI command"""

    @patch('src.cli.exit_app.get_confirmation')
    @patch('src.cli.exit_app.display_success')
    @patch('src.cli.exit_app.display_error')
    @patch('src.cli.exit_app.pause')
    @patch('src.cli.exit_app.clear_screen')
    def test_exit_app_with_confirm(self, mock_clear, mock_pause, mock_error, mock_success, mock_confirm):
        """Test exiting app with confirmation"""
        # Setup mock inputs and outputs
        mock_confirm.return_value = True

        # Execute the function
        exit_app()

        # Verify interactions
        mock_clear.assert_called_once()
        mock_confirm.assert_called_once()
        mock_success.assert_called_once()
        mock_error.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.exit_app.get_confirmation')
    @patch('src.cli.exit_app.display_success')
    @patch('src.cli.exit_app.display_error')
    @patch('src.cli.exit_app.pause')
    @patch('src.cli.exit_app.clear_screen')
    def test_exit_app_with_cancel(self, mock_clear, mock_pause, mock_error, mock_success, mock_confirm):
        """Test exiting app with cancel"""
        # Setup mock inputs and outputs
        mock_confirm.return_value = False

        # Execute the function
        exit_app()

        # Verify interactions
        mock_clear.assert_called_once()
        mock_confirm.assert_called_once()
        mock_success.assert_not_called()
        mock_error.assert_not_called()
        mock_pause.assert_called_once()

    @patch('src.cli.exit_app.get_confirmation')
    @patch('src.cli.exit_app.display_success')
    @patch('src.cli.exit_app.display_error')
    @patch('src.cli.exit_app.pause')
    @patch('src.cli.exit_app.clear_screen')
    def test_exit_app_with_general_exception(self, mock_clear, mock_pause, mock_error, mock_success, mock_confirm):
        """Test exiting app with general exception"""
        # Setup mock inputs and outputs
        mock_confirm.side_effect = Exception("Unexpected error")

        # Execute the function
        exit_app()

        # Verify interactions
        mock_clear.assert_called_once()
        mock_confirm.assert_called_once()
        mock_success.assert_not_called()
        mock_error.assert_called_once()
        mock_pause.assert_called_once()

    @patch('src.cli.exit_app.get_confirmation')
    @patch('src.cli.exit_app.display_success')
    @patch('src.cli.exit_app.display_error')
    @patch('src.cli.exit_app.pause')
    @patch('src.cli.exit_app.clear_screen')
    def test_exit_app_with_keyboard_interrupt(self, mock_clear, mock_pause, mock_error, mock_success, mock_confirm):
        """Test exiting app with keyboard interrupt"""
        # Setup mock inputs and outputs
        mock_confirm.side_effect = KeyboardInterrupt()

        # Execute the function
        exit_app()

        # Verify interactions
        mock_clear.assert_called_once()
        mock_confirm.assert_called_once()
        mock_success.assert_not_called()
        mock_error.assert_not_called()
        mock_pause.assert_called_once()