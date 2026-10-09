from pathlib import Path
import shutil
import pytest
from syntaxlab.config import Config
from syntaxlab.courses import Catalog
from syntaxlab.service import Lab

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def catalog():
    return Catalog(ROOT)


@pytest.fixture
def lab(tmp_path):
    shutil.copytree(ROOT / "content", tmp_path / "content")
    return Lab(Config(tmp_path))
