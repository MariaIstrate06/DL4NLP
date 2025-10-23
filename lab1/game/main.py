from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import nltk
from nltk.corpus import words, wordnet
import random, os, json, uuid

# ensure nltk data is downloaded
nltk.download('words', quiet=True)
nltk.download('wordnet', quiet=True)

HTML_FILE = "index.html"
GAMES = dict()


# --- word utils ---
def get_random_words(draws=1):
    """Draws random words that exist in WordNet."""
    drws = []
    for _ in range(draws):
        while True:
            attempt = random.choice(words.words())
            if len(wordnet.synsets(attempt)) == 0:
                continue
            if attempt in [d["word"] for d in drws]:
                continue
            drws.append({"word": attempt, "score": random.random() * 5})
            break
    drws.sort(key=lambda w: w["score"], reverse=True)
    return drws


def generate_game(gameid):
    """Creates a new game object."""
    return {
        "gameid": gameid,
        "state": "ongoing",
        "words": get_random_words(7),
        "cutoff": 3,  # if a word falls below this, it's removed
        "word_ceiling": 13,  # max allowed words before game over
        "turns": 0,
        "score": 0,
    }


# --- semantic similarity logic ---
def expanded_synset_relations(synset):
    """
    Returns a set of related synsets including hypernyms, hyponyms,
    similar_tos, member_holonyms, etc.
    """
    related = set()
    related.update(synset.hypernyms())
    related.update(synset.hyponyms())
    related.update(synset.similar_tos())
    related.update(synset.member_holonyms())
    related.update(synset.part_holonyms())
    related.update(synset.member_meronyms())
    related.update(synset.part_meronyms())
    related.update(synset.attributes())
    related.update(synset.also_sees())
    return related


def get_similarity(word, guess):
    """
    Returns a composite similarity score between two words using:
      - direct Wu-Palmer similarity
      - expanded synset relations overlap
    """
    synsets1 = wordnet.synsets(guess)
    synsets2 = wordnet.synsets(word)

    if not synsets1 or not synsets2:
        return 0.0

    # Base similarity (Wu-Palmer)
    wup_sim = max(
        (s1.wup_similarity(s2) or 0.0)
        for s1 in synsets1
        for s2 in synsets2
    )

    # Expand both sets to include related concepts
    expanded1 = set()
    for s in synsets1:
        expanded1 |= expanded_synset_relations(s)
    expanded2 = set()
    for s in synsets2:
        expanded2 |= expanded_synset_relations(s)

    # Overlap ratio of expanded related synsets
    overlap = len(expanded1 & expanded2)
    denom = max(len(expanded1 | expanded2), 1)
    relation_score = overlap / denom

    # weighted combo (feel free to tweak weights)
    final_score = (wup_sim * 0.7) + (relation_score * 0.3)
    return final_score


# --- game logic ---
def update_game_state(state: dict, update: dict) -> dict:
    guess = update["word"].lower()
    state.pop("altered_words", None)
    state.pop("removed_words", None)
    state.pop("message", None)

    if len(wordnet.synsets(guess)) == 0:
        state["message"] = "Unknown word used. Try another one."
        return state

    match update["action"]:
        case "guess":
            if guess in [w["word"] for w in state["words"]]:
                state["message"] = "Cannot use word already in list."
                return state

            altered_words = []
            for w in state["words"][state["cutoff"]:]:
                similarity = get_similarity(w["word"], guess)
                if similarity > 0.0:
                    altered_words.append(w["word"])
                    w["score"] += similarity

            state["words"].sort(key=lambda w: w["score"], reverse=True)

            removed_words = []
            for w in state["words"][:state["cutoff"]]:
                if w["word"] in altered_words:
                    removed_words.append(w["word"])
                    state["score"] += w["score"]
                    state["words"].remove(w)

            state["altered_words"] = altered_words
            state["removed_words"] = removed_words
            state["turns"] += 1
            state["words"] += get_random_words(1)

        case "requestHint":
            for w in state["words"]:
                if w["word"] == guess:
                    definitions = [s.definition() for s in wordnet.synsets(guess)]
                    w["definition"] = definitions
                    break

    if len(state["words"]) > state["word_ceiling"]:
        state["state"] = "game_over"

    return state


# --- HTTP handler ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        params = parse_qs(parsed_url.query)
        gameid = params.get("gameid", [None])[0]

        if not gameid or gameid not in GAMES:
            new_gameid = str(uuid.uuid4())
            GAMES[new_gameid] = generate_game(new_gameid)
            self.send_response(302)
            self.send_header("Location", f"/?gameid={new_gameid}")
            self.end_headers()
            return

        if parsed_url.path == "/":
            if os.path.exists(HTML_FILE):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open(HTML_FILE, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"HTML file not found.")

        elif parsed_url.path == "/gamestate":
            game = GAMES[gameid]
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(game).encode())

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found.")

    def do_POST(self):
        parsed_url = urlparse(self.path)
        params = parse_qs(parsed_url.query)
        gameid = params.get("gameid", [None])[0]

        if not gameid or gameid not in GAMES:
            new_gameid = str(uuid.uuid4())
            GAMES[new_gameid] = generate_game(new_gameid)
            self.send_response(302)
            self.send_header("Location", f"/?gameid={new_gameid}")
            self.end_headers()
            return

        if parsed_url.path == "/gamestate":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            update = json.loads(post_data)
            GAMES[gameid] = update_game_state(GAMES[gameid], update)
            print("New state:", GAMES[gameid])
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(GAMES[gameid]).encode())


# --- run server ---
def run(server_class=HTTPServer, handler_class=SimpleHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
