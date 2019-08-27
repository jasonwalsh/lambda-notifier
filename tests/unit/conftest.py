import os
import pytest

from json import load
from unittest.mock import create_autospec

from github3.github import GitHub

from . import BASE_DIR


@pytest.fixture
def event():
    """Represents an Amazon API Gateway event"""
    with open(os.path.join(BASE_DIR, '..', 'event.json')) as f:
        return load(f)


@pytest.fixture
def context():
    return None


@pytest.fixture
def session():
    Session = create_autospec(GitHub, spec_set=True)
    return Session(token='4494bc85')
