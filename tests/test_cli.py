import subprocess
import sys

from sbalign import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "sbalign", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__
