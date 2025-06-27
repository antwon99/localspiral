import os
import sys
import json
import pytest

stubs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'stubs'))
sys.path.insert(0, stubs_path)

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from localspiral.utils.characters import load_character


def test_load_character_success(tmp_path):
    src_file = os.path.join(project_root, 'localspiral', 'characters', 'sample_character.json')
    data = load_character(src_file)
    assert data['id'] == 'sample'


def test_load_character_missing_field(tmp_path):
    bad_file = tmp_path / 'bad.json'
    bad_content = {
        "id": "bad"
        # missing other fields
    }
    bad_file.write_text(json.dumps(bad_content))
    with pytest.raises(ValueError):
        load_character(str(bad_file))


def test_load_character_bad_json(tmp_path):
    bad_file = tmp_path / 'corrupt.json'
    bad_file.write_text('{')
    with pytest.raises(ValueError):
        load_character(str(bad_file))
