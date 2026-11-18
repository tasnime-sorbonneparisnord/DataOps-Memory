"""Textes de l'interface en français et en anglais (une clé = un texte dans chaque langue)."""

TEXTS = {
    "fr": {
        "common.back": "Retour",
        "common.player": "Joueur",
        "level.easy": "Facile",
        "level.medium": "Moyen",
        "level.hard": "Difficile",
        "level.title": "Niveau {name}",

        "splash.welcome": "Bienvenue dans DataOps Memory !",
        "splash.slogan": "Trouve la paire, répare le serveur !",
        "splash.continue": "Clique pour continuer",

        "pseudo.title": "Ton pseudo",
        "pseudo.question": "Comment t'appelles-tu, data engineer ?",
        "pseudo.hint": "{max} caractères maximum · Entrée pour valider",
        "pseudo.validate": "Valider",
        "pseudo.error.empty": "Le pseudo ne peut pas être vide.",
        "pseudo.error.too_long": "{max} caractères maximum.",
        "pseudo.error.characters": "Lettres, chiffres, espaces, - et _ seulement.",

        "menu.hello": "Salut, {pseudo} !",
        "menu.play": "Jouer",
        "menu.play.sub": "Choisis ton niveau et sauve la prod",
        "menu.rules": "Comment jouer",
        "menu.rules.sub": "Les règles en une minute",
        "menu.scores": "Meilleurs scores",
        "menu.scores.sub": "Tes records pour chaque niveau",
        "menu.settings": "Paramètres",
        "menu.settings.sub": "Volume, luminosité et langue",
        "menu.credits": "Crédits",
        "menu.credits.sub": "L'équipe et le cadre du projet",
        "menu.quit": "Quitter",
        "menu.quit.sub": "À bientôt, d'astreinte !",

        "levels.title": "Choisis ton niveau",
        "intro.start": "C'est parti !",
        "intro.incidents": "{count} incidents à réparer",
        "intro.cards": "{cards} cartes · {seconds} secondes",
        "intro.no_special": "Aucune carte spéciale",
        "intro.coffee": "{count} carte{s} Café : +{seconds} s",
        "intro.critical": "{count} carte{s} Critique : -{seconds} s",
        "intro.tagline.easy": "Parfait pour t'échauffer avant la vraie panne !",
        "intro.tagline.medium": "La prod commence à chauffer : reste concentré !",
        "intro.tagline.hard": "Panne générale à 3 h du matin : garde ton sang-froid !",

        "cinematic.calm": "3 h 06 du matin... tout est calme.",
        "cinematic.alert": "ALERTE : la prod est en panne !",
        "cinematic.go": "À toi de jouer : répare les incidents !",

        "rules.title": "Comment jouer",
        "rules.lines": [
            "Il est 3 h du matin : la prod est en panne et tu es d'astreinte.",
            "Retourne deux cartes à la fois en cliquant dessus.",
            "Si c'est un incident et sa solution, l'incident est réparé !",
            "Sinon, les cartes se recachent : retiens bien leur place.",
            "Carte Café : +10 secondes.   Carte Critique : −10 secondes.",
            "Répare tous les incidents avant la fin du chrono pour gagner.",
            "Record : le plus de temps restant, puis le moins de tentatives.",
        ],

        "scores.title": "Meilleurs scores",
        "scores.level": "Niveau",
        "scores.time_left": "Temps restant",
        "scores.attempts": "Essais",
        "scores.none": "Pas encore de record",

        "settings.title": "Paramètres",
        "settings.music": "Musique",
        "settings.effects": "Effets sonores",
        "settings.brightness": "Luminosité",
        "settings.language": "Langue",

        "credits.title": "Crédits",
        "credits.heading": "Développement du projet — DataOps Memory",
        "credits.team": "Membres de l'équipe",
        "credits.frame": "Cadre du projet",
        "credits.master": "Master 2 BIDABI",
        "credits.course": "Module : Programmation épurée (Clean Code)",

        "game.time": "Temps",
        "game.attempts": "Essais",
        "game.record": "Record",
        "game.record_detail": "{count} essais",
        "game.to_beat": "à battre !",
        "game.mission": "Mission",
        "game.fixed_count": "incidents réparés",
        "game.fixed": "Incident réparé !",
        "game.coffee": "Pause café ! +{seconds} s",
        "game.critical": "Incident critique ! −{seconds} s",

        "end.win": "{pseudo} sauve la prod !",
        "end.lose": "La prod est toujours en panne...",
        "end.default_player": "Le joueur",
        "end.victory": "Victoire",
        "end.defeat": "Défaite",
        "end.replay": "Rejouer",
        "end.levels": "Niveaux",
        "end.home": "Accueil",
        "end.new_record": "Nouveau record !",
        "end.time_left": "Temps restant",
        "end.attempts": "Essais",
        "end.fixed": "Incidents réparés",
        "end.record": "Record",
        "end.record_with": "Record ({count} essais)",
    },
    "en": {
        "common.back": "Back",
        "common.player": "Player",
        "level.easy": "Easy",
        "level.medium": "Medium",
        "level.hard": "Hard",
        "level.title": "{name} level",

        "splash.welcome": "Welcome to DataOps Memory!",
        "splash.slogan": "Find the pair, fix the server!",
        "splash.continue": "Click to continue",

        "pseudo.title": "Your name",
        "pseudo.question": "What's your name, data engineer?",
        "pseudo.hint": "{max} characters max · Press Enter to confirm",
        "pseudo.validate": "Confirm",
        "pseudo.error.empty": "Your name can't be empty.",
        "pseudo.error.too_long": "{max} characters max.",
        "pseudo.error.characters": "Letters, digits, spaces, - and _ only.",

        "menu.hello": "Hi, {pseudo}!",
        "menu.play": "Play",
        "menu.play.sub": "Pick a level and save production",
        "menu.rules": "How to play",
        "menu.rules.sub": "The rules in one minute",
        "menu.scores": "Best scores",
        "menu.scores.sub": "Your records for each level",
        "menu.settings": "Settings",
        "menu.settings.sub": "Volume, brightness and language",
        "menu.credits": "Credits",
        "menu.credits.sub": "The team and the project",
        "menu.quit": "Quit",
        "menu.quit.sub": "See you on call!",

        "levels.title": "Choose your level",
        "intro.start": "Let's go!",
        "intro.incidents": "{count} incidents to fix",
        "intro.cards": "{cards} cards · {seconds} seconds",
        "intro.no_special": "No special card",
        "intro.coffee": "{count} Coffee card{s}: +{seconds} s",
        "intro.critical": "{count} Critical card{s}: -{seconds} s",
        "intro.tagline.easy": "Perfect to warm up before the real outage!",
        "intro.tagline.medium": "Production is heating up: stay focused!",
        "intro.tagline.hard": "Total outage at 3 a.m.: keep your cool!",

        "cinematic.calm": "3:06 a.m.... everything is quiet.",
        "cinematic.alert": "ALERT: production is down!",
        "cinematic.go": "Your turn: fix the incidents!",

        "rules.title": "How to play",
        "rules.lines": [
            "It's 3 a.m.: production is down and you are on call.",
            "Flip two cards at a time by clicking on them.",
            "If they are an incident and its solution, the incident is fixed!",
            "Otherwise, the cards flip back: remember where they are.",
            "Coffee card: +10 seconds.   Critical card: −10 seconds.",
            "Fix every incident before the timer runs out to win.",
            "Record: most time left first, then fewest attempts.",
        ],

        "scores.title": "Best scores",
        "scores.level": "Level",
        "scores.time_left": "Time left",
        "scores.attempts": "Attempts",
        "scores.none": "No record yet",

        "settings.title": "Settings",
        "settings.music": "Music",
        "settings.effects": "Sound effects",
        "settings.brightness": "Brightness",
        "settings.language": "Language",

        "credits.title": "Credits",
        "credits.heading": "Project development — DataOps Memory",
        "credits.team": "Team members",
        "credits.frame": "Project context",
        "credits.master": "Master's degree (M2) BIDABI",
        "credits.course": "Course: Clean Code programming",

        "game.time": "Time",
        "game.attempts": "Attempts",
        "game.record": "Record",
        "game.record_detail": "{count} attempts",
        "game.to_beat": "to beat!",
        "game.mission": "Mission",
        "game.fixed_count": "incidents fixed",
        "game.fixed": "Incident fixed!",
        "game.coffee": "Coffee break! +{seconds} s",
        "game.critical": "Critical incident! −{seconds} s",

        "end.win": "{pseudo} saves production!",
        "end.lose": "Production is still down...",
        "end.default_player": "The player",
        "end.victory": "Victory",
        "end.defeat": "Defeat",
        "end.replay": "Play again",
        "end.levels": "Levels",
        "end.home": "Home",
        "end.new_record": "New record!",
        "end.time_left": "Time left",
        "end.attempts": "Attempts",
        "end.fixed": "Incidents fixed",
        "end.record": "Record",
        "end.record_with": "Record ({count} attempts)",
    },
}
DEFAULT_LANGUAGE = "fr"


class Translator:
    """Donne le texte d'une clé dans la langue choisie dans les paramètres.

    La langue est relue à chaque appel : changer de langue s'applique tout de suite.
    Une clé absente en anglais retombe sur le français, pour ne jamais planter.
    """

    def __init__(self, settings):
        self._settings = settings

    def __call__(self, key: str, **values) -> str:
        text = self.raw(key)
        return text.format(**values) if values else text

    def raw(self, key: str):
        """Le texte (ou la liste de textes) sans remplacer les {valeurs}."""
        language = TEXTS.get(self._settings.language, TEXTS[DEFAULT_LANGUAGE])
        return language.get(key, TEXTS[DEFAULT_LANGUAGE][key])

    def level_name(self, difficulty) -> str:
        return self(f"level.{difficulty.value}")
