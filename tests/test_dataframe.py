from pathlib import Path

import pytest

from sbalign.dataframe import read_sbalign_df


def test_dataframe():
    file_name = Path(__file__).parent / "sample.txt"
    df = read_sbalign_df(file_name)
    assert len(df) == 32
    row = df[df.uttid == "LJ002-0243"]
    assert row.error_rate.item() == pytest.approx(53.85)
    assert (
        row.ref.item()
        == "WITH;JURISDICTION;TO;HOLD;PLEAS;IN;ALL;ACTIONS;WITHIN;THE;PRESCRIBED;"
        "LIMITS;THE;COURT;WAS;CHIEFLY;USED;FOR;THE;RECOVERY;OF;SMALL;DEBTS;UNDER;"
        "TEN;POUNDS"
    )
