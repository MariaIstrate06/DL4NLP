from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import nltk
nltk.download('words')
nltk.download('wordnet')
from nltk.corpus import words
from nltk.corpus import wordnet
import random, os, json, uuid



HTML_FILE = "index.html"
GAMES = dict()

def get_random_words(draws=1):
    drws = []
    for _ in range(draws):
        while True:
            attempt = random.choice(words.words())
            if len(wordnet.synsets(attempt)) == 0:
                continue
            if attempt in drws:
                continue
            drws.append({'word': attempt, 'score': random.random() * 5}) # At most 5 turns before a word is removed
            break
    drws.sort(key=lambda w: w['score'], reverse=True)
    return drws

def generate_game(gameid):
    return {
        'gameid': gameid,
        'state': 'ongoing',
        'words': get_random_words(7),
        'cutoff': 3, # If word scores are updated to be under this, the word is consumed.
        'word_ceiling': 13, # More than this amount of words is a game over.
        'turns': 0,
        'score': 0,
    }

def get_similarity(word, guess):
    synsets1 = wordnet.synsets(guess)
    synsets2 = wordnet.synsets(word)
    if synsets1 and synsets2:
        sim = synsets1[0].wup_similarity(synsets2[0])
        return sim if sim is not None else 0.0
    else:
        return 0.0

def update_game_state(state: dict, update: dict) -> dict:
    guess = update['word']
    state.pop('altered_words', None)
    state.pop('deleted_words', None)
    state.pop('message', None)
    if len(wordnet.synsets(guess)) == 0:
        # Invalid word, turn doesn't count.
        state['message'] = 'Unknown word used. Try another one.'
        return state
    match update['action']:
        case 'guess':
            if guess in map(lambda w: w['word'], state['words']):
                state['message'] = 'Cannot use word already in list. Try another one.'
                return state
            altered_words = []
            for w in state['words'][state['cutoff']:]:
                similarity = get_similarity(w['word'], guess)
                if similarity > 0.0:
                    altered_words.append(w['word'])
                    w['score'] += similarity
            state['words'].sort(key=lambda w: w['score'], reverse=True)
            removed_words = []
            for w in state['words'][:state['cutoff']]:
                if w['word'] in altered_words:
                    removed_words.append(w['word'])
                    state['score'] += w['score']
                    state['words'].remove(w)
            state['altered_words'] = altered_words
            state['removed_words'] = removed_words
            state['turns'] = 1 + state['turns']
            state['words'] += get_random_words(1)
        case 'requestHint':
            for w in state['words']:
                if w['word'] == guess:
                    definition = []
                    for synset in wordnet.synsets(guess):
                        definition += [synset.definition()]
                    w['definition'] = definition
                    break
    if len(state['words']) > state['word_ceiling']:
        state['state'] = 'game_over'
    return state

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        params = parse_qs(parsed_url.query)
        
        gameid = params.get('gameid', [None])[0]

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
        
        gameid = params.get('gameid', [None])[0]

        if not gameid or gameid not in GAMES:
            new_gameid = str(uuid.uuid4())
            GAMES[new_gameid] = {'state': 'ongoing', 'words': get_random_words(7)}
            self.send_response(302)
            self.send_header("Location", f"/?gameid={new_gameid}")
            self.end_headers()
            return

        if parsed_url.path == "/gamestate":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            update = json.loads(post_data)
            GAMES[gameid] = update_game_state(GAMES[gameid], update)
            print("New state:", GAMES[gameid])
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(GAMES[gameid]).encode())
            

def run(server_class=HTTPServer, handler_class=SimpleHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
