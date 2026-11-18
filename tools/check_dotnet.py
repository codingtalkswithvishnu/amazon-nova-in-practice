"""Restore locked packages and build each C# project without invoking AWS."""

import argparse
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--dotnet", default="dotnet", help="Path to the .NET SDK executable"
)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
projects = sorted(root.glob("examples/**/Sample.csproj")) + sorted(
    root.glob("dotnet/**/Sample.csproj")
)
for project in projects:
    subprocess.run([args.dotnet, "restore", str(project), "--locked-mode"], check=True)
    subprocess.run(
        [args.dotnet, "build", str(project), "--no-restore", "--nologo"], check=True
    )
print(f"Built {len(projects)} C# projects with locked packages; no AWS calls.")
