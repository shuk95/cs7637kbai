import re
import numpy as np

class SentenceReadingAgent:
    def __init__(self):
        self.names = {"Serena", "Andrew", "Bobbie", "Cason", "David", "Farzana", "Frank", "Hannah", "Ida", "Irene", "Jim", "Jose", "Keith", "Laura", "Lucy", "Meredith", "Nick", "Ada", "Yeeling", "Yan"}

        self.common_words = {"the", "of", "to", "and", "a", "in", "is", "it", "you", "that", "he", "was", "for", "on", "are", "with", "as", "I", "his", "they", "be", "at", "one", "have", "this", "from", "or", "had", "by", "hot", "but", "some", "what", "there", "we", "can", "out", "other", "were", "all", "your", "when", "up", "use", "word", "how", "said", "an", "each", "she", "which", "do", "their", "time", "if", "will", "way", "about", "many", "then", "them", "would", "write", "wrote", "like", "so", "these", "her", "long", "make", "thing", "see", "him", "two", "has", "look", "more", "day", "could", "go", "come", "did", "my", "sound", "no", "most", "number", "who", "over", "know", "water", "than", "call", "first", "people", "may", "down", "side", "been", "now", "find", "any", "new", "work", "part", "take", "get", "place", "made", "live", "where", "after", "back", "little", "only", "round", "man", "year", "came", "show", "every", "good", "me", "give", "our", "under", "name", "very", "through", "just", "form", "much", "great", "think", "say", "help", "low", "line", "before", "turn", "cause", "same", "mean", "differ", "move", "right", "boy", "old", "too", "does", "tell", "sentence", "set", "three", "want", "air", "well", "also", "play", "small", "end", "put", "home", "read", "hand", "port", "large", "spell", "add", "even", "land", "here", "must", "big", "high", "such", "follow", "act", "why", "ask", "men", "change", "went", "light", "kind", "off", "need", "house", "picture", "try", "us", "again", "animal", "point", "mother", "world", "near", "build", "self", "earth", "father", "head", "stand", "own", "page", "should", "country", "found", "answer", "school", "grow", "study", "still", "learn", "plant", "cover", "food", "sun", "four", "thought", "let", "keep", "eye", "never", "last", "door", "between", "city", "tree", "cross", "since", "hard", "start", "might", "story", "saw", "far", "sea", "draw", "left", "late", "run", "don't", "while", "press", "close", "night", "real", "life", "few", "stop", "open", "seem", "together", "next", "white", "children", "begin", "got", "walk", "example", "ease", "paper", "often", "always", "music", "those", "both", "mark", "book", "letter", "until", "mile", "river", "car", "feet", "care", "second", "group", "carry", "took", "rain", "eat", "room", "friend", "began", "idea", "fish", "mountain", "north", "once", "base", "hear", "horse", "cut", "sure", "watch", "color", "face", "wood", "main", "enough", "plain", "girl", "usual", "young", "ready", "above", "ever", "red", "Red", "list"}

    def solve(self, sentence, question):
        words = np.array(re.findall(r'\w+:\w+|\w+', sentence))
        question_lower = question.lower()

        if "who brought" in question_lower:
            return words[np.where(words == "brought")[0][0] - 1]

        if "what did" in question_lower:
            idx_start, idx_end = np.where(words == "brought")[0][0] + 1, np.where(words == "to")[0][0]
            return " ".join(words[idx_start:idx_end])

        if "who did" in question_lower:
            return words[np.where(words == "to")[0][0] + 1]

        if "how long" in question_lower:
            return next((word for word in words if word in ["short", "long"]), "")

        if "who does" in question_lower and "with" in question_lower:
            subject = re.findall(r'who does (\w+)', question_lower)[0].capitalize()
            return next((word for word in words if word in self.names and word != subject), "")

        if "where" in question_lower:
            return words[np.where(words == "to")[0][-1] + 1]

        if "how far" in question_lower:
            idx = np.where(words == "mile")[0][0]
            return f"{words[idx - 1]} mile"

        if "how do" in question_lower:
            return next((word for word in words if word in ["walk", "run", "drive", "fly"]), "")

        if "at what time" in question_lower:
            return next((word for word in words if re.match(r'\d+:\d+(AM|PM)?', word)), "")

        return ""
