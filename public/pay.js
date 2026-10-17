// Paid games: shows a Buy button, then the download links once Stripe confirms payment.
(function () {
  var WORKER = "https://calc-games-pay.YOUR-SUBDOMAIN.workers.dev"; // set after `wrangler deploy`
  var box = document.querySelector("[data-paid]");
  if (!box) return;
  var game = box.getAttribute("data-paid");
  var price = box.getAttribute("data-price");
  var params = new URLSearchParams(location.search);
  var sid = params.get("session_id");

  function link(href, text, cls) {
    var a = document.createElement("a");
    a.className = cls;
    a.href = href;
    a.textContent = text;
    return a;
  }

  function note(text) {
    var p = document.createElement("p");
    p.className = "muted";
    p.textContent = text;
    return p;
  }

  box.textContent = "";
  if (params.get("paid") === "1" && sid) {
    box.appendChild(link(WORKER + "/download/" + game + ".py?session=" + encodeURIComponent(sid), "Download " + game + ".py", "btn dl"));
    box.appendChild(link(WORKER + "/download/" + game + ".zip?session=" + encodeURIComponent(sid), "Download " + game + ".zip", "btn dl"));
    box.parentNode.insertBefore(note("Thanks for buying! If a download fails, reload this page with the same address."), box.nextSibling);
    return;
  }

  var buy = document.createElement("button");
  buy.className = "btn dl";
  buy.type = "button";
  buy.textContent = "Buy " + game.replace(/_/g, " ") + " for " + price;
  var err = note("");
  err.style.display = "none";
  buy.addEventListener("click", function () {
    buy.disabled = true;
    fetch(WORKER + "/checkout", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ game: game }),
    })
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (!d.url) throw new Error(d.error || "No checkout link");
        location.href = d.url;
      })
      .catch(function () {
        buy.disabled = false;
        err.textContent = "Could not start payment. Please try again.";
        err.style.display = "";
      });
  });
  box.appendChild(buy);
  box.parentNode.insertBefore(err, box.nextSibling);
})();
