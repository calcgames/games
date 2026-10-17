# Calc Games

A static website of games for the Casio fx-CG100. No build step.

- `public/` is the whole site. The workflow publishes only this folder to GitHub Pages, so nothing outside it is ever served.
- `public/files/` holds the free games (`.py` and `.zip` of each).
- Falling Blocks, Block Puzzle and Sweet Match are sold on Payhip. Their game pages link to the Payhip product pages.

## Rules

- Never commit the paid game files. Keep them on your computer and upload them to Payhip.
- Everything inside `public/` is public.

## Edit it

- Each game has a page in `public/` (`flappy.html`, ...). The home page is `public/index.html`.
- Screenshots are in `public/img/`. Colours and layout are in `public/style.css`.
- Push to `main` and the site redeploys.
