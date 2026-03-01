"""
Blackjack web server — pure Python stdlib, no dependencies.
Run: python3 server.py
Then open: http://localhost:8080
"""

import json
import random
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import os

# ──────────────────────────────────────────────
# Game logic
# ──────────────────────────────────────────────

SUITS = ["S", "H", "D", "C"]
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

def card_value(rank):
    if rank in ("J", "Q", "K"):
        return 10
    if rank == "A":
        return 11  # treated as 11; hand logic reduces as needed
    return int(rank)

def hand_total(hand):
    total = 0
    aces = 0
    for card in hand:
        v = card_value(card["rank"])
        if card["rank"] == "A":
            aces += 1
        total += v
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def is_blackjack(hand):
    return len(hand) == 2 and hand_total(hand) == 21

def make_deck():
    deck = [{"rank": r, "suit": s} for s in SUITS for r in RANKS]
    random.shuffle(deck)
    return deck

def deal(deck, n=1):
    cards = []
    for _ in range(n):
        if not deck:
            deck.extend(make_deck())
        cards.append(deck.pop())
    return cards

def compute_payout(result, bet):
    """Return (payout_amount, net) based on result and bet."""
    if result == "blackjack":
        payout = int(bet * 2.5)
        net = payout - bet
    elif result in ("win", "dealer_bust"):
        payout = bet * 2
        net = bet
    elif result == "push":
        payout = bet
        net = 0
    else:  # lose, bust, dealer_blackjack
        payout = 0
        net = -bet
    return payout, net

def game_state_for_client(game, session=None, reveal_dealer=False):
    dealer_hand = game["dealer"]
    player_hand = game["player"]

    if reveal_dealer or game["phase"] in ("dealer", "done"):
        dealer_visible = dealer_hand
        dealer_total = hand_total(dealer_hand)
    else:
        dealer_visible = [{"rank": "?", "suit": "?"}, dealer_hand[1]] if len(dealer_hand) >= 2 else dealer_hand
        dealer_total = card_value(dealer_hand[1]["rank"]) if len(dealer_hand) >= 2 else 0

    player_total = hand_total(player_hand)
    player_bj = is_blackjack(player_hand)
    dealer_bj = is_blackjack(dealer_hand)

    result = None
    if game["phase"] == "done":
        pt = hand_total(player_hand)
        dt = hand_total(dealer_hand)
        if player_bj and not dealer_bj:
            result = "blackjack"
        elif dealer_bj and not player_bj:
            result = "dealer_blackjack"
        elif pt > 21:
            result = "bust"
        elif dt > 21:
            result = "dealer_bust"
        elif pt > dt:
            result = "win"
        elif dt > pt:
            result = "lose"
        else:
            result = "push"

    state = {
        "phase": game["phase"],
        "dealer": dealer_visible,
        "dealer_total": dealer_total if game["phase"] in ("dealer", "done") else None,
        "player": player_hand,
        "player_total": player_total,
        "result": result,
        "can_double": len(player_hand) == 2 and game["phase"] == "player",
    }

    if session is not None:
        bet = session.get("bet", 0)
        balance = session.get("balance", 0)
        payout = None
        net = None
        if result is not None:
            payout, net = compute_payout(result, bet)
        state["balance"] = balance
        state["bet"] = bet
        state["payout"] = payout
        state["net"] = net
        state["name"] = session.get("name", "")
        state["broke"] = balance == 0 and game["phase"] == "done" and result not in ("win", "blackjack", "dealer_bust", "push")

    return state

def new_game(sessions, session_id, bet):
    session = sessions.get(session_id, {})
    deck = make_deck()
    player = deal(deck, 2)
    dealer = deal(deck, 2)
    game = {
        "deck": deck,
        "player": player,
        "dealer": dealer,
        "phase": "player",
    }
    # Deduct bet from balance
    session["balance"] = session.get("balance", 0) - bet
    session["bet"] = bet
    session["game"] = game

    # Instant resolve if player has blackjack
    if is_blackjack(player):
        game["phase"] = "done"
        _apply_payout(game, session)

    sessions[session_id] = session
    return game_state_for_client(game, session)

def hit(sessions, session_id):
    session = sessions.get(session_id)
    if not session:
        return {"error": "no session"}
    game = session.get("game")
    if not game or game["phase"] != "player":
        return {"error": "invalid action"}
    game["player"] += deal(game["deck"], 1)
    if hand_total(game["player"]) >= 21:
        _run_dealer(game, session)
    return game_state_for_client(game, session)

def double_down(sessions, session_id):
    session = sessions.get(session_id)
    if not session:
        return {"error": "no session"}
    game = session.get("game")
    if not game or game["phase"] != "player" or len(game["player"]) != 2:
        return {"error": "invalid action"}
    # Double the bet — deduct additional bet from balance
    extra = session["bet"]
    if extra > session["balance"]:
        extra = session["balance"]  # can't bet more than you have
    session["balance"] -= extra
    session["bet"] += extra
    game["player"] += deal(game["deck"], 1)
    _run_dealer(game, session)
    return game_state_for_client(game, session)

def stand(sessions, session_id):
    session = sessions.get(session_id)
    if not session:
        return {"error": "no session"}
    game = session.get("game")
    if not game or game["phase"] != "player":
        return {"error": "invalid action"}
    _run_dealer(game, session)
    return game_state_for_client(game, session)

def _run_dealer(game, session=None):
    game["phase"] = "dealer"
    while hand_total(game["dealer"]) < 17:
        game["dealer"] += deal(game["deck"], 1)
    game["phase"] = "done"
    if session is not None:
        _apply_payout(game, session)

def _apply_payout(game, session):
    """Calculate result and add payout back to balance."""
    player_hand = game["player"]
    dealer_hand = game["dealer"]
    player_bj = is_blackjack(player_hand)
    dealer_bj = is_blackjack(dealer_hand)
    pt = hand_total(player_hand)
    dt = hand_total(dealer_hand)

    if player_bj and not dealer_bj:
        result = "blackjack"
    elif dealer_bj and not player_bj:
        result = "dealer_blackjack"
    elif pt > 21:
        result = "bust"
    elif dt > 21:
        result = "dealer_bust"
    elif pt > dt:
        result = "win"
    elif dt > pt:
        result = "lose"
    else:
        result = "push"

    bet = session.get("bet", 0)
    payout, _ = compute_payout(result, bet)
    session["balance"] = session.get("balance", 0) + payout


# ──────────────────────────────────────────────
# HTTP server
# ──────────────────────────────────────────────

sessions = {}  # session_id -> session dict (includes "game" key)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # silence default access log spam

    def _session_id(self):
        cookie = self.headers.get("Cookie", "")
        for part in cookie.split(";"):
            part = part.strip()
            if part.startswith("bj_session="):
                return part[len("bj_session="):]
        return None

    def _send_json(self, data, status=200, new_session=None):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        if new_session:
            self.send_header("Set-Cookie", f"bj_session={new_session}; Path=/; HttpOnly")
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path, content_type):
        try:
            with open(path, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", len(data))
            self.end_headers()
            self.wfile.write(data)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == "/" or path == "/index.html":
            self._send_file(os.path.join(STATIC_DIR, "index.html"), "text/html; charset=utf-8")
        elif path.startswith("/static/"):
            file_path = os.path.join(os.path.dirname(__file__), path.lstrip("/"))
            ext = os.path.splitext(file_path)[1]
            ctype = {"css": "text/css", "js": "application/javascript", "png": "image/png"}.get(ext.lstrip("."), "application/octet-stream")
            self._send_file(file_path, ctype)

        elif path == "/api/setup":
            name = params.get("name", [""])[0].strip() or "Player"
            try:
                balance = int(params.get("balance", ["0"])[0])
            except ValueError:
                self._send_json({"error": "invalid balance"}, 400)
                return
            if not (1 <= balance <= 1_000_000):
                self._send_json({"error": "balance must be between 1 and 1,000,000"}, 400)
                return
            sid = self._session_id()
            new_sid = sid or str(uuid.uuid4())
            sessions[new_sid] = {
                "name": name,
                "balance": balance,
                "starting_balance": balance,
                "bet": 0,
                "game": None,
            }
            self._send_json(
                {"name": name, "balance": balance, "phase": "betting"},
                new_session=new_sid if not sid else None
            )

        elif path == "/api/new":
            sid = self._session_id()
            if not sid or sid not in sessions:
                self._send_json({"error": "no session — call /api/setup first"}, 400)
                return
            session = sessions[sid]
            try:
                bet = int(params.get("bet", ["0"])[0])
            except ValueError:
                self._send_json({"error": "invalid bet"}, 400)
                return
            if not (1 <= bet <= session["balance"]):
                self._send_json({"error": f"bet must be between 1 and {session['balance']}"}, 400)
                return
            state = new_game(sessions, sid, bet)
            self._send_json(state)

        elif path == "/api/hit":
            sid = self._session_id()
            if not sid:
                self._send_json({"error": "no session"}, 400)
                return
            self._send_json(hit(sessions, sid))

        elif path == "/api/stand":
            sid = self._session_id()
            if not sid:
                self._send_json({"error": "no session"}, 400)
                return
            self._send_json(stand(sessions, sid))

        elif path == "/api/double":
            sid = self._session_id()
            if not sid:
                self._send_json({"error": "no session"}, 400)
                return
            self._send_json(double_down(sessions, sid))

        elif path == "/api/cashout":
            sid = self._session_id()
            if not sid or sid not in sessions:
                self._send_json({"error": "no session"}, 400)
                return
            session = sessions[sid]
            name = session.get("name", "Player")
            starting = session.get("starting_balance", 0)
            final = session.get("balance", 0)
            net = final - starting
            if net > 0:
                message = f"You walked away ${net} ahead!"
            elif net < 0:
                message = f"You're down ${abs(net)} — better luck next time."
            else:
                message = "You broke even — not bad!"
            del sessions[sid]
            self._send_json({
                "name": name,
                "starting_balance": starting,
                "final_balance": final,
                "net": net,
                "message": message,
            })

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        self.do_GET()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"Blackjack running at http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
