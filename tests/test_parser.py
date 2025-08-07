from pathlib import Path

import pytest

from sbalign.parser import parse_alignment_file


def test_parser():
    file_name = Path(__file__).parent / "sample.txt"
    alignment = parse_alignment_file(file_name)
    assert len(alignment.items) == 32
    assert alignment.error_rate == pytest.approx(45.72)
    assert alignment.utt_error_rate == pytest.approx(78.12)
    assert alignment.utt_errors == 25
    assert alignment.utt_total == 32
    item = alignment.items[0]
    assert item.ref == [
        "THE",
        "PAPER",
        "ON",
        "WHICH",
        "THE",
        "PRINTING",
        "IS",
        "TO",
        "BE",
        "DONE",
        "IS",
        "A",
        "NECESSARY",
        "PART",
        "OF",
        "OUR",
        "SUBJECT",
    ]

    assert item.hyp == [
        "THE",
        "PAPER",
        "ON",
        "WHICH",
        "THE",
        "PRINTING",
        "IS",
        "TO",
        "BE",
        "AND",
        "IS",
        "A",
        "NECESSARY",
        "PART",
        "OF",
        "OUR",
        "SUBJECT",
    ]
    assert item.uttid == "LJ001-0156"
    assert item.error_rate == pytest.approx(5.88)
    assert item.errors == 1
    assert item.tokens == 17
    assert item.insertions == 0
    assert item.deletions == 0
    assert item.substitutions == 1
    item = alignment.items[-1]
    assert item.uttid == "LJ003-0232"
    assert item.error_rate == pytest.approx(28.57)
