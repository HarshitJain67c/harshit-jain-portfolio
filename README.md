# Harshit Jain — Portfolio

A responsive, accessible portfolio for Harshit Jain, Senior Software Engineer at
Veer Textiles. The site presents his experience across mobile applications, web
platforms, analytics, production operations, and DevOps, along with education,
the open-source AnnotraQ benchmark, and the MillPulse operations prototype.

## Live site

[harshitjain67c.github.io/harshit-jain-portfolio](https://harshitjain67c.github.io/harshit-jain-portfolio/)

## Run locally

No build tools or dependencies are required.

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000`.

## Verify

```bash
./verify.sh
```

The check validates the page structure, local assets, accessibility text, links,
and—when Node.js is available—JavaScript syntax.

## GitHub Pages

The repository is a static site and can be published directly from the root of
the `main` branch in **Settings → Pages**.

## Project structure

```text
.
├── index.html
├── styles.css
├── script.js
├── assets/
│   └── engineering-systems.png
└── tests/
    └── validate_site.py
```

The hero artwork is an original generated asset created for this portfolio.
