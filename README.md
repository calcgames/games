# Calc Games

A static website. No build step. Every link is relative, so it works at
`https://<you>.github.io/<repo>/` without changes.

## Publish on GitHub Pages (private repo, public site)

1. Create a **private** repository and upload everything in this folder,
   including the hidden `.github` folder and `.nojekyll`. Easiest is git:
   `git init -b main && git add -A && git commit -m "site" && git remote add origin <url> && git push -u origin main`
2. Repo **Settings > Pages > Build and deployment > Source: GitHub Actions**.
3. Go to the **Actions** tab. "Deploy site to GitHub Pages" runs on every push to `main`
   (or press "Run workflow"). When it is green, the site is at
   `https://<you>.github.io/<repo>/`.

The site and everything in `files/` (the `.py` and `.zip` downloads) are public.
The repository itself, and any file you do not put in this folder, stay private.
Only put things in this folder that you want public, because the whole folder is published.

**Plan requirement:** GitHub Pages from a *private* repo needs GitHub Pro, Team or Enterprise Cloud.
On the free plan, Pages only works from public repos. If you are on Free, keep your private repo
for your own source and make a second **public** repo containing just this folder.

## Edit it

- Games live in `files/` (the `.py` and a `.zip` of each). Replace both together.
- Screenshots are in `img/`.
- Each game has its own page (`flappy.html`, ...). The home page is `index.html`.
- Colours and layout are in `style.css`.

## Other hosts

Netlify (drag the folder onto app.netlify.com/drop), Cloudflare Pages and Vercel also work: no build command, output directory `.`.
