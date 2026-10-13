# OMA website

Source of <https://microbiome.github.io>, the landing page for
**Orchestrating Microbiome Analysis with Bioconductor (OMA)**.

The site is built with [Quarto](https://quarto.org). GitHub Actions renders it
on every push to `master` and deploys it to GitHub Pages. Pull requests are
rendered as a check but not deployed.

## Common edits

| To change… | Edit |
|---|---|
| Consortium members | `data/contributors.csv` (`name`, `affiliation`, `orcid`, `github`; only `name` is required) |
| Workshops (globe and list) | `data/events.csv` (date can be `2024`, `2024-09` or `2024-09-18`; leave `lat`/`lon` empty for online workshops; optional `registration` URL marks an upcoming workshop as "Registration open" (brown) with a Register link; optional `registration_deadline` (`YYYY-MM-DD`) closes it automatically. Upcoming/past and open/closed are worked out in the visitor's browser from today's date, so no rebuild is needed when a date passes) |
| Book, packages, material, workshops, publications, contributors | `index.qmd` (one section each) |
| Globe (3D map of events) | `scripts/globe.html`; country shapes in `data/countries.geojson` |
| In-page contents bar | the `<nav class="section-nav">` block in `index.qmd` |
| Navigation and footer | `_quarto.yml` |
| Colours and fonts (taken from bioconductor.org) | `styles/theme.scss` |
| Header background (mia logo characters) | run `python3 scripts/make-hero-background.py`; characters in `images/characters/` |

## Preview locally

```sh
quarto preview
```

You need R with `rmarkdown`, `knitr` and `jsonlite`.

## Contributing

1. Fork the repository and create a branch.
2. Make your change and check it with `quarto preview`.
3. Open a pull request. The GitHub Action checks that the site renders.

## First-time setup

In the repository settings, go to **Pages** and set **Source** to
**GitHub Actions**.
