# A new headset from this template

**TL;DR.** An owner creates `overpressure/<codename>` from this template; its team runs
`python scripts/new-headset.py <codename> "<Name>" "<SoC>"` once, commits, and has a headset that loads in
overpressure, passes its CI and offers one step. Everything after that is the headset's own work. This file and
the script go with the first commit.

## What it holds

| File | What it is |
| --- | --- |
| `headset.json` | codename, name, version (`2026.11.0.dev0`, a calendar version: [docs/releasing.md](docs/releasing.md)), the headset interface it is made for (`1.5`) |
| `tooling/__init__.py` | `HEADSET`: one command (`dev status`) and two window steps (the host tools, *Status*) |
| `tooling/localconfig.py`, `env.example` | its `.env` settings: overpressure's `DeviceSettings` with its own key prefix |
| `tooling/doctor.py` | its checks for `python -m overpressure doctor`, from the shared ones |
| `tests/` | host tests of the above |
| `README.md` | the owners' page, in the [headset README template](https://github.com/overpressure/overpressure/blob/main/docs/headset-readme-template.md)'s form, every row ❔ |
| `CLAUDE.md`, `docs/` | the developers' guidance and documents, releasing included |
| `.github/` | CI against overpressure's `main` (tests on Windows, Linux and macOS, ruff, ty, the docs and README check, the private-data scan, shellcheck, actionlint), the release on a tag, issue forms, the pull request template, CODEOWNERS |
| `.gitattributes`, `.editorconfig`, `.gitignore`, `cliff.toml`, `LICENSE` | line endings and `headset.json`'s `export-subst`, the changelog's setup, the Unlicense |

## Steps

1. **An owner** creates `overpressure/<codename>` from this template (*Use this template*), the team
   `<codename>` with *maintain* on it, and its rulesets
   ([GOVERNANCE.md](https://github.com/overpressure/.github/blob/main/GOVERNANCE.md)).
2. **The team**, in an overpressure checkout:

   ```sh
   git clone https://github.com/overpressure/<codename> devices/<codename>
   python devices/<codename>/scripts/new-headset.py <codename> "<Name>" "<SoC>"
   python -m overpressure devices
   python -m unittest discover -t . -s devices/<codename>/tests
   ```

   `<codename>` is the vendor's internal name for the headset, lowercase, a Python identifier. Then commit on a
   branch and open the first pull request: CI runs.
3. **From there** the headset follows
   [docs/adding-a-headset.md](https://github.com/overpressure/overpressure/blob/main/docs/adding-a-headset.md):
   its own commands and steps, the installer, the backup, its kernel layer in overpressure/linux and its packages
   in overpressure/packages (each by pull request there), its README rows as results come in, and its first beta.
