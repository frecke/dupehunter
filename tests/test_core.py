import pytest

from dupehunter.core import calculate_checksum


def test_calculate_checksum(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("Hello, world!")
    checksum = calculate_checksum(file)
    assert (
        checksum == "a948904f2f0f479b8f8197694b30184b0d2e13165cf22f73a3d8ef9a3fcd0c55"
    )


def test_calculate_checksum_with_invalid_file():
    with pytest.raises(FileNotFoundError):
        calculate_checksum("nonexistent_file.txt")
