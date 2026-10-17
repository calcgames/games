// Calc Games payment Worker.
// Routes:
//   POST /checkout              { game } -> { url }  (Stripe Checkout, GBP)
//   GET  /download/<game>.<ext>?session=cs_...      (serves the file only if Stripe says it was paid)
// Secret: STRIPE_SECRET_KEY (set with `wrangler secret put STRIPE_SECRET_KEY`).

const SITE = "https://YOUR-SITE-URL/"; // e.g. https://calcgames.github.io/games/ (must end with /)

// Prices in pence. Keep in sync with the labels in pay.js / index.html.
const PRICES = {
  block_puzzle: { amount: 200, name: "Block Puzzle" },
  sweet_match: { amount: 150, name: "Sweet Match" },
  falling_blocks: { amount: 100, name: "Falling Blocks" },
};

const ORIGIN = SITE.replace(/\/$/, "");

function cors() {
  return {
    "access-control-allow-origin": ORIGIN,
    "access-control-allow-methods": "GET, POST, OPTIONS",
    "access-control-allow-headers": "content-type",
  };
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "content-type": "application/json", ...cors() },
  });
}

async function createCheckout(game, env) {
  const p = PRICES[game];
  const params = new URLSearchParams({
    mode: "payment",
    "line_items[0][quantity]": "1",
    "line_items[0][price_data][currency]": "gbp",
    "line_items[0][price_data][unit_amount]": String(p.amount),
    "line_items[0][price_data][product_data][name]": `${p.name} for Casio fx-CG100`,
    success_url: `${SITE}${game}.html?paid=1&session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${SITE}${game}.html`,
    "metadata[game]": game,
    "payment_intent_data[metadata][game]": game,
  });
  // Stripe needs the {CHECKOUT_SESSION_ID} placeholder unescaped.
  const body = params.toString().replace("%7BCHECKOUT_SESSION_ID%7D", "{CHECKOUT_SESSION_ID}");
  const r = await fetch("https://api.stripe.com/v1/checkout/sessions", {
    method: "POST",
    headers: {
      authorization: `Bearer ${env.STRIPE_SECRET_KEY}`,
      "content-type": "application/x-www-form-urlencoded",
    },
    body,
  });
  if (!r.ok) return json({ error: "Could not start checkout" }, 502);
  const s = await r.json();
  return json({ url: s.url });
}

async function serveDownload(game, ext, sessionId, env) {
  if (!PRICES[game] || !/^cs_[A-Za-z0-9_]+$/.test(sessionId || "")) {
    return new Response("Not found", { status: 404 });
  }
  const r = await fetch(`https://api.stripe.com/v1/checkout/sessions/${sessionId}`, {
    headers: { authorization: `Bearer ${env.STRIPE_SECRET_KEY}` },
  });
  if (!r.ok) return new Response("Not found", { status: 404 });
  const s = await r.json();
  if (s.payment_status !== "paid" || s.metadata?.game !== game) {
    return new Response("Payment not found for this game", { status: 403 });
  }
  const obj = await env.GAMES.get(`${game}.${ext}`);
  if (!obj) return new Response("File missing", { status: 404 });
  return new Response(obj.body, {
    headers: {
      "content-type": ext === "py" ? "text/x-python; charset=utf-8" : "application/zip",
      "content-disposition": `attachment; filename="${game}.${ext}"`,
      "cache-control": "private, no-store",
    },
  });
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    if (req.method === "OPTIONS") return new Response(null, { headers: cors() });

    if (url.pathname === "/checkout" && req.method === "POST") {
      const { game } = await req.json().catch(() => ({}));
      if (!PRICES[game]) return json({ error: "Unknown game" }, 400);
      return createCheckout(game, env);
    }

    const m = url.pathname.match(/^\/download\/([a-z_]+)\.(py|zip)$/);
    if (m && req.method === "GET") {
      return serveDownload(m[1], m[2], url.searchParams.get("session"), env);
    }

    return new Response("Not found", { status: 404 });
  },
};
