import re
from pathlib import Path
from unittest.mock import patch

from screeninfo import Monitor

README_PATH = Path(__file__).parent.parent / "README.md"


def test_documentation_exists() -> None:
    """Test that the documentation path is valid."""
    assert README_PATH.exists()


def test_documentation(capsys) -> None:
    """Test that the output documented in README is consistent with the actual
    output of the library.
    """
    readme_content = README_PATH.read_text()

    input_match = re.search(
        "```python([^`]*)```", readme_content, flags=re.DOTALL
    )
    output_match = re.search(
        "```python console([^`]*)```", readme_content, flags=re.DOTALL
    )

    assert input_match
    assert output_match

    code = input_match.group(1).strip()
    expected_result = output_match.group(1).strip()
    with patch(
        "screeninfo.get_monitors",
        return_value=[
            Monitor(
                x=3840,
                y=0,
                width=3840,
                height=2160,
                width_mm=1420,
                height_mm=800,
                name="HDMI-0",
                is_primary=False,
            ),
            Monitor(
                x=0,
                y=0,
                width=3840,
                height=2160,
                width_mm=708,
                height_mm=399,
                name="DP-0",
                is_primary=True,
            ),
        ],
    ):
        exec(code)
    actual_result = capsys.readouterr().out.strip()

    assert actual_result == expected_result
