# Releasing

**TL;DR.** A pushed, annotated tag that is `headset.json`'s calendar version (`2026.12.0`, a beta `2026.12.0b0`)
makes the release overpressure downloads (`python -m overpressure headset add myheadset`, the window's
*Download*): the source zip and its SHA-256, nothing uploaded by hand. Only the headset's team creates its tags
([GOVERNANCE.md](https://github.com/overpressure/.github/blob/main/GOVERNANCE.md)).

## Versions

Calendar versions, as overpressure's
([versions across the project](https://github.com/overpressure/overpressure/blob/main/docs/releasing.md#versions-across-the-project)):
a release is `YYYY.M.PATCH` (the month without a leading zero, that month's releases counted from 0), a beta the
coming release with `bN` from `b0`, and `main` between releases the next one as a development version
(`2026.12.0.dev0`); a download of `main` is shown with its commit's time. The tag is the version itself, the same as
`version` in [headset.json](../headset.json). A beta is a pre-release: `headset add myheadset` takes it while there is
no stable release. `api` in `headset.json` names the overpressure headset interface the release needs: every
overpressure that runs it installs the release, also later ones, and the release's notes name the oldest one.

## A release

1. **Ready.** Everything is on `main`, CI is green, and no issue the release depends on is open. An overpressure
   release runs this headset's `api` already (the notes need one).
2. **The version.** With overpressure checked out beside this repository as `.overpressure`:
   `python .overpressure/scripts/release.py bump beta --version-file headset.json` (or `stable`) writes the
   release's version and prints it. That change goes to `main` by pull request.
3. **The tag.** An annotated tag on that commit of `main`, named exactly as the version: its first line the
   release's title, the rest the release's own words, what was checked on the headset and what is known not to
   work. Then push it.

   ```sh
   git tag -a 2026.12.0b0 -F tag-message.md
   git push origin 2026.12.0b0
   ```

4. **CI** ([release.yml](../.github/workflows/release.yml)) runs every check of CI on the tagged commit, refuses
   a tag that is not annotated, not on `main`, not a calendar release or another version than `headset.json`'s,
   writes the notes and `CHANGELOG.md` with overpressure's `scripts/release.py notes` (git-cliff,
   [cliff.toml](../cliff.toml)), naming the oldest overpressure release that runs `api`, makes the source zip with
   `git archive` and creates the GitHub release, a pre-release for a beta.
5. **The next version.** `python .overpressure/scripts/release.py bump next --version-file headset.json` writes
   the next development version, by pull request.
6. **The catalogue.** For its first release, the headset gets its entry in overpressure's
   `overpressure/catalogue.py`, by pull request there: then the window offers it.

A failed check stops the release before anything is published. Fix it on `main`, delete the tag (`git push
origin :refs/tags/2026.12.0b0`) and tag the fixed commit. A published version never moves.
