from pathlib import Path
import re

ROOT = Path("profile-summary-card-output")

THEMES = {
    "github_dark": {
        "output": "custom_dark",
        "colors": {
            "#0d1117": "#0d1117",  # Background
            "#2e343b": "#30363d",  # Border
            "#0366d6": "#88aba3",  # Username
            "#40c463": "#88aba3",  # Graph
            "#77909c": "#c9d1d9",  # Text
            "#8b949e": "#8b949e",  # Icons
        },
    },
    "github": {
        "output": "custom_light",
        "colors": {
            "#ffffff": "#ffffff",  # Background
            "#0366d6": "#527c73",  # Username
            "#40c463": "#527c73",  # Graph
            "#24292f": "#24292f",  # Text
            "#57606a": "#57606a",  # Secondary text
        },
    },
}


def transform(source: Path, destination: Path, replacements: dict):
    content = source.read_text(encoding="utf-8")

    def replace_color(match):
        original = match.group(0)
        return replacements.get(original.lower(), original)

    content = re.sub(
        r"#[0-9a-fA-F]{6}\b",
        replace_color,
        content,
    )

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")

    print(f"Generated: {destination}")


def main():
    for theme, settings in THEMES.items():
        source = ROOT / theme / "0-profile-details.svg"

        if not source.exists():
            raise FileNotFoundError(
                f"Required SVG not found: {source}"
            )

        destination = (
            ROOT
            / settings["output"]
            / "0-profile-details.svg"
        )

        transform(
            source,
            destination,
            settings["colors"],
        )


if __name__ == "__main__":
    main()
