# encoding: utf-8
import json
import logging
import os

# Gère le fichier des high-scores
HIGHSCORE_FILE = "scores.json"
HIGHSCORE_COUNT = 10    # conserve uniquement les 10 meilleurs

# Le tableau des scores ressemble à ceci
# {
#   "scores" : [
#       { "nom": "bob", "score": 1000 },
#       { "nom": "alice", "score": 950 }
#   ]
# }
scores = { "scores": [{'nom': '---', 'score': 0}] * 10 }


def load_high_score():
    global scores
    
    if not os.path.exists(HIGHSCORE_FILE):
        return scores
    
    try:
        with open(HIGHSCORE_FILE) as json_file:
            scores = json.load(json_file)
            
        # Test de cohérence:
        if 'scores' not in scores:
            logging.error("Le fichier des highscores semble corrompu")
            scores["scores"] = [{'nom': '---', 'score': 0}] * 10
    except Exception as e:
        logging.error(e)
        logging.error("Impossible de trouver le fichier des high-scores")
        
    return scores


# Détermine si le score fait partie du "top-ten" (HIGHSCORE_COUNT)
def is_highscore(score):
    scs = scores["scores"]
    sorted_scs = sorted(scs, key=lambda d: d['score'], reverse=True)
    sorted_scs = sorted_scs[:HIGHSCORE_COUNT]
    return not len(scs) or sorted_scs[-1]['score'] < score

    
# Met à jour les scores
def update(name, score):
    global scores
    
    scores['scores'].append({ 'nom': name, 'score': score})
    scs = scores["scores"]
    sorted_scs = sorted(scs, key=lambda d: d['score'], reverse=True)
    scores = { "scores": list(sorted_scs[:HIGHSCORE_COUNT])}
    
    try:
        with open(HIGHSCORE_FILE, 'w') as outfile:
            json.dump(scores, outfile)
    except Exception as e:
        logging.error(e)
        logging.error("Impossible de sauver le fichier des high-scores")
