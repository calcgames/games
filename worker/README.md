# Payment Worker (paid games)

One-time setup, run from this `worker/` folder:

1. `npx wrangler login`
2. `npx wrangler r2 bucket create calc-games-private`
3. Upload the paid files (they stay private, they are not in the Pages site):
   `npx wrangler r2 object put calc-games-private/block_blast.py --file=path/to/block_blast.py` (repeat for `.zip`, `candy`, `tetris`)
4. Add your Stripe secret key: `npx wrangler secret put STRIPE_SECRET_KEY`
5. Put your site URL in `src/index.js` (`SITE`) and the Worker URL in `public/pay.js` (`WORKER`).
6. `npx wrangler deploy`

Stripe: the account owner must be 18+, or have a legal guardian as owner (see Stripe's age rules).
Test with Stripe test keys first (`sk_test_...`) and card `4242 4242 4242 4242`.
