import os
from unittest.mock import AsyncMock, MagicMock

import pytest

from pytest import Config

from settings.db import IS_NOSQL, IS_RELATIONAL_DB, initialize_db


def pytest_configure(config: Config):
    echo = print  # ignore: remove-print-statements
    echo(__file__)
    echo(f'DATABASE_URI={os.environ["DATABASE_URI"]}')


@pytest.fixture(scope='session')
def anyio_backend():
    yield 'asyncio'


@pytest.fixture(scope='session')
async def mock_async_unit_of_work():
    auow = MagicMock()
    auow.__aenter__.return_value = auow
    auow.pce_repo = AsyncMock()

    yield auow


if IS_NOSQL:

    @pytest.fixture(scope='function', autouse=True)
    async def engine():
        await initialize_db()
