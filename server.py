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

def game_state_for_client(game, reveal_dealer=False):
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

    return {
        "phase": game["phase"],
        "dealer": dealer_visible,
        "dealer_total": dealer_total if game["phase"] in ("dealer", "done") else None,
        "player": player_hand,
        "player_total": player_total,
        "result": result,
        "can_double": len(player_hand) == 2 and game["phase"] == "player",
    }

def new_game(sessions, session_id):
    deck = make_deck()
    player = deal(deck, 2)
    dealer = deal(deck, 2)
    game = {
        "deck": deck,
        "player": player,
        "dealer": dealer,
        "phase": "player",
    }
    # Instant resolve if player has blackjack
    if is_blackjack(player):
        game["phase"] = "done"
    sessions[session_id] = game
    return game_state_for_client(game)

def hit(sessions, session_id):
    game = sessions.get(session_id)
    if not game or game["phase"] != "player":
        return {"error": "invalid action"}
    game["player"] += deal(game["deck"], 1)
    if hand_total(game["player"]) >= 21:
        # Auto-stand or bust — run dealer
        _run_dealer(game)
    return game_state_for_client(game)

def double_down(sessions, session_id):
    game = sessions.get(session_id)
    if not game or game["phase"] != "player" or len(game["player"]) != 2:
        return {"error": "invalid action"}
    game["player"] += deal(game["deck"], 1)
    _run_dealer(game)
    return game_state_for_client(game)

def stand(sessions, session_id):
    game = sessions.get(session_id)
    if not game or game["phase"] != "player":
        return {"error": "invalid action"}
    _run_dealer(game)
    return game_state_for_client(game)

def _run_dealer(game):
    game["phase"] = "dealer"
    while hand_total(game["dealer"]) < 17:
        game["dealer"] += deal(game["deck"], 1)
    game["phase"] = "done"


# ──────────────────────────────────────────────
# HTTP server
# ──────────────────────────────────────────────

sessions = {}  # session_id -> game state

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

        if path == "/" or path == "/index.html":
            self._send_file(os.path.join(STATIC_DIR, "index.html"), "text/html; charset=utf-8")
        elif path.startswith("/static/"):
            file_path = os.path.join(os.path.dirname(__file__), path.lstrip("/"))
            ext = os.path.splitext(file_path)[1]
            ctype = {"css": "text/css", "js": "application/javascript", "png": "image/png"}.get(ext.lstrip("."), "application/octet-stream")
            self._send_file(file_path, ctype)
        elif path == "/api/new":
            sid = self._session_id()
            new_sid = sid or str(uuid.uuid4())
            state = new_game(sessions, new_sid)
            self._send_json(state, new_session=new_sid if not sid else None)
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
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        self.do_GET()


if __name__ == "__main__":
    port = 8080
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"Blackjack running at http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
