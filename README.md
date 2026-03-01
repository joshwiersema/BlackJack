# BlackJack

I built this browser-based Blackjack game built without frameworks and deployed it using the free tier of Render. I built this for my college friends that have a gambling addiction that are too broke to feed it.
Live at: https://uiblackjack.onrender.com

---

## Tech Stack

**Backend:** Pure Python using the standard library's `http.server` module — no Flask, no Django, no third-party web framework. The server is multithreaded via `ThreadingHTTPServer` and handles all routing, session management, and game logic manually. Sessions are maintained server-side and tracked via an `HttpOnly` cookie.

**Frontend:** Vanilla HTML, CSS, and JavaScript served from a `static/` directory. No frontend frameworks or build tools.

**Deployment:** Render, configured via `render.yaml`.

---

## How to Play

1. Enter your name and a starting balance to begin a session.
2. Place a bet using the quick-select buttons or enter a custom amount, then hit **Deal**.
3. On your turn, choose an action:
   - **Hit** — draw another card
   - **Stand** — end your turn and let the dealer play
   - **Double** — double your bet, draw exactly one more card, and end your turn
4. The dealer draws until reaching a hand total of 17 or higher.
5. Whoever is closer to 21 without going over wins. A natural Blackjack (Ace + 10-value card on the initial deal) pays out at 2.5x your bet.
6. Continue playing hands until you cash out or your balance hits zero.

---

## Run Locally
```bash
git clone https://github.com/joshwiersema/BlackJack.git
cd BlackJack
pip install -r requirements.txt
python server.py
```

Navigate to `http://localhost:8080` in your browser.
