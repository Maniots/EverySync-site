# EverySync website

Static homepage and privacy policy for [EverySync](https://github.com/Maniots/OneDriveSync).
This repository is maintained separately and linked from the application repository
as the `website` Git submodule.

- Homepage: https://maniots.github.io/EverySync-site/
- Privacy: https://maniots.github.io/EverySync-site/privacy.html

## Edit and preview

Edit `public/index.html`, `public/privacy.html` and `public/styles.css`.
The logo is copied from the application's existing `ui/resources/app.svg`.
No JavaScript, package manager, external fonts, analytics or build step is used.

```sh
python scripts/check_site.py
python -m http.server 8000 --directory public
```

Open http://localhost:8000. Check both pages at desktop and mobile widths.
When changing data handling, verify the privacy text against the application code
and update its effective date. Never commit OAuth metadata, user tokens,
application configuration, logs or user files to this public repository.

## Deployment

GitHub Pages must be configured to use **GitHub Actions**. A push to `main`
affecting the public files or deployment checks validates and publishes only
`public/`. The `Publish EverySync website` workflow can also be started manually.
The site deploys independently of the Windows installer and its regressions.

After a website commit, update the submodule pointer in the application repository
so that its checkout records the published website revision.

## Google OAuth

Use the public homepage and privacy URLs above in Google Auth Platform Branding.
These pages do not configure OAuth, change publishing status, verify domain
ownership or indicate Google approval. Verify ownership through Google Search
Console separately if Google requests it. Keep the same privacy URL linked from
the homepage and the consent screen.
