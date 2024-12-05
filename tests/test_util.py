import logging
from unittest.mock import patch

import pytest

from dupehunter.utils import configure_logging


@pytest.mark.parametrize(
    "log_level",
    [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL],
)
@patch("dupehunter.utils.logging.basicConfig")
def test_configure_logging(mock_basic_config, log_level):
    """
    Test that configure_logging correctly sets up logging with the given level.
    """
    configure_logging(level=log_level)
    mock_basic_config.assert_called_once_with(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
