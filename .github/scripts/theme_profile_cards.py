from pathlib import Path
import re

ROOT = Path("profile-summary-card-output")

THEMES = {
    "github_dark": {
        "output": "custom_dark",
        "background": "#0D1117",
        "text": "#C9D1D9",
        "muted": "#8B949E",
        "accent": "#88ABA3",
    },
    "github": {
        "output": "custom_light",
        "background": "#FFFFFF",
        "text": "#24292F",
        "muted": "#57606A",
        "accent": "#527C73",
    },
}

# Standard theme colors to replace.
# Additional colors can be added after inspecting generated SVGs.
REPLACEMENTS = {
    "github_dark": {
        "#0d1117": "background",
        "#c9d1d9": "text",
        "#8b949e": "muted",
        "#58a6ff": "accent",
        "#39d353": "accent",
        "#2ea043": "accent",
        "#3fb950": "accent",
        "#26a641": "accent",
        "#00ff00": "accent",
    },
    "github": {
        "#ffffff": "background",
        "#24292f": "text",
        "#57606a": "muted",
        "#0969da": "accent",
        "#1f883d": "accent",
        "#2da44e": "accent",
        "#40c463": "accent",
    },
}


def transform(source: Path, destination: Path, theme: str):
    content = source.read_text(encoding="utf-8")

    settings = THEMES[theme]
    replacements = REPLACEMENTS[theme]

    def replace_color(match):
        original = match.group(0)
        key = original.lower()

        if key not in replacements:
            return original

        target = replacements[key]
        return settings[target]

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

        transform(source, destination, theme)


if __name__ == "__main__":
    main()
