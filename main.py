#importer la librairie flask
from flask import Flask, render_template, session, redirect
import os
from questions import questions

#création de l'application
app = Flask(__name__)
app.secret_key = os.urandom(24)


#Route de la page d'accueil
@app.route('/')
def index():
    session["numero_question"] = 0
    session["score"] = {"Builder" :0, "Redstonneur" :0, "Mineur" :0, "Joueur PvP" :0}
    return render_template("index.html")

@app.route('/questions')
def question():
    global questions
    
    #On récupère le cookie question qui nous permet de savoir à quelle question on est
    numero = session["numero_question"]
    #On vérifie si il reste des question (numero nous indique à quelle question on est)
    if numero < len(questions):
        #On récupère l'énoncé de la question
        enonce_question = questions[numero]["enonce"] #Ici on [numero] nous dit où aller et [enonce] dit qu'on récupère ce dernier
        #On crée une copie de notre dictionnaire contenant la question et les réponses
        question_copy = questions[numero].copy()
        #On supprime l'énoncé de la question
        question_copy.pop("enonce")
        #On récupère les réponses sous forme de liste
        reponses = list(question_copy.values())
        #On récupère également les clefs pour les scores
        clefs = list(question_copy.keys())
        #On stocke l'ordre des clefs dans un cookie pour le comptage des scores
        session["clefs"] = clefs
        
        #On affiche notre page question html
        return render_template("questions.html", questions = enonce_question, reponses = reponses)
    else:
        #On trie le score de manière décroissante
        score_trie = sorted(session["score"], key = session["score"].get, reverse = True)
        #On récupère le vainqueur
        vainqueur = score_trie[0]
        return render_template("resultat.html", vainqueur = vainqueur)
    

@app.route('/reponse/<numero>')
def reponse(numero):
    #On incrémente numéro question pour passer à la question suivante
    session["numero_question"] += 1
    #On selectionne le personnage dont la réponse a été selectionnée avec le dico des clefs
    personnage = session["clefs"][int(numero)]
    #On incrémente les scores selon le personnage
    session["score"][personnage] += 1
    return redirect("/questions")

#Execution de l'application
#host="0.0.0.0" => le serv flask s'éxécute sur cette adresse IP
#port = 81 => quelle type de lien informatique est-ce ?
app.run(host="0.0.0.0", port=81)