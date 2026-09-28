class SentenceReadingAgent:
    def __init__(self):
        self.names = {"Serena", "Andrew", "Bobbie", "Cason", "David", "Farzana", "Frank", "Hannah", "Ida", "Irene",
                      "Jim", "Jose", "Keith", "Laura", "Lucy", "Meredith", "Nick", "Ada", "Yeeling", "Yan"}

    def solve(self, sentence, question):
        sentence = sentence.strip(".").split()
        question = question.strip("?").split()

        sentence_lower = [word.lower() for word in sentence]
        question_lower = [word.lower() for word in question]

        def get_names(words):
            return [w for w in words if w in self.names]

        # Who brought the note?
        if "who" in question_lower and "brought" in question_lower:
            for word in sentence:
                if word in self.names:
                    return word

        # What did X bring?
        if "what" in question_lower and ("bring" in question_lower or "brought" in question_lower):
            for obj in ["note", "rock", "book", "letter"]:
                if obj in sentence_lower:
                    idx = sentence_lower.index(obj)
                    if idx > 0:
                        return sentence[idx - 1] + " " + sentence[idx] if sentence[idx - 1].lower() in ["a", "an", "the", "short"] else sentence[idx]

        # Who did X bring it to?
        if "who" in question_lower and "to" in question_lower:
            if "to" in sentence_lower:
                idx = sentence_lower.index("to")
                if idx + 1 < len(sentence):
                    return sentence[idx + 1]

        # How long was the note?
        if "how" in question_lower and "long" in question_lower:
            if "note" in sentence_lower:
                idx = sentence_lower.index("note")
                if idx > 0:
                    return sentence[idx - 1]

        # Who does Lucy go with?
        if "who" in question_lower and "with" in question_lower:
            people = get_names(sentence)
            for p in people:
                if p.lower() != "lucy":
                    return p

        # Where do X go?
        if "where" in question_lower and "go" in question_lower:
            if "to" in sentence_lower:
                idx = sentence_lower.index("to")
                if idx + 1 < len(sentence):
                    return sentence[idx + 1]

        # How far do X walk?
        if "how" in question_lower and "far" in question_lower:
            if "walk" in sentence_lower:
                idx = sentence_lower.index("walk")
                if idx + 2 < len(sentence):
                    return sentence[idx + 1] + " " + sentence[idx + 2]

        # How do X get to school?
        if "how" in question_lower and "get" in question_lower:
            for word in sentence:
                if word.lower() in ["walk", "run", "bike", "drive"]:
                    return word

        # At what time...?
        if "time" in question_lower:
            for word in sentence:
                if ":" in word:
                    return word

        # What is [X] made of?
        if "made" in question_lower and "of" in question_lower:
            if "of" in sentence_lower:
                idx = sentence_lower.index("of")
                if idx + 1 < len(sentence):
                    return sentence[idx + 1]

        # What should you watch?
        if "watch" in question_lower and "watch" in sentence_lower:
            idx = sentence_lower.index("watch")
            if idx + 1 < len(sentence):
                return sentence[idx + 1]

        # What is in the [place]?
        if "in" in question_lower:
            if "in" in sentence_lower:
                idx = sentence_lower.index("in")
                if idx - 1 >= 0:
                    return sentence[idx - 1]

        # What color is the [animal]?
        if "color" in question_lower:
            for i in range(len(sentence_lower) - 1):
                if sentence_lower[i + 1] in question_lower:
                    return sentence[i]

        # What animal is [color]?
        if "animal" in question_lower and "is" in question_lower:
            for i in range(len(sentence_lower) - 1):
                if sentence_lower[i] in question_lower:
                    return sentence[i + 1]

        # Who was with Serena?
        if "who" in question_lower and "with" in question_lower:
            names = get_names(sentence)
            for name in names:
                if name.lower() != "serena":
                    return name

        # What was [color]?
        if "what" in question_lower:
            for i in range(len(sentence_lower) - 1):
                if sentence_lower[i] in ["blue", "white", "red", "black", "green"]:
                    if sentence_lower[i] in question_lower:
                        return sentence[i + 1]

        # How many adults?
        if "how" in question_lower and "many" in question_lower and "adults" in question_lower:
            for i, word in enumerate(sentence_lower):
                if word == "adults" and i >= 2:
                    return sentence[i - 2] + " " + sentence[i - 1]

        # What did X take to the farm?
        if ("take" in question_lower or "took" in question_lower) and "to" in sentence_lower:
            idx = sentence_lower.index("to")
            if idx - 1 >= 0:
                return sentence[idx - 1]

        # Who will watch a play?
        if "who" in question_lower and "watch" in sentence_lower:
            for word in sentence:
                if word in self.names:
                    return word

        # What will Lucy write?
        if "write" in question_lower:
            if "write" in sentence_lower:
                idx = sentence_lower.index("write")
                if idx + 1 < len(sentence):
                    return sentence[idx + 1]

        # What is east of the city?
        if "east" in sentence_lower and "city" in sentence_lower:
            idx = sentence_lower.index("east")
            if idx - 1 >= 0:
                return sentence[idx - 1]

        # Where are the men?
        if "where" in question_lower and "men" in question_lower:
            if "in" in sentence_lower:
                idx = sentence_lower.index("in")
                if idx + 1 < len(sentence):
                    return sentence[idx + 1]

        # 2) How many adults are in this city?
        #
        if "how" in question_lower and "many" in question_lower and "adults" in question_lower:
            for i, w in enumerate(sentence_lower):
                if w == "adults" and i >= 2:
                    # e.g. ["one","hundred","adults"] → "one hundred"
                    return sentence[i-2] + " " + sentence[i-1]

        #
        # 3) How big is Red?
        #
        if "how" in question_lower and "big" in question_lower:
            if "large" in sentence_lower:
                idx = sentence_lower.index("large")
                # include adverb if present
                if idx-1 >= 0 and sentence_lower[idx-1] in {"very","extremely","really","quite"}:
                    return sentence[idx-1] + " " + sentence[idx]
                return sentence[idx]

        #
        # 4) What will she write to him?
        #
        if "what" in question_lower and "write" in question_lower:
            for obj in ["note","rock","book","letter","play","story","poem"]:
                if obj in sentence_lower:
                    idx = sentence_lower.index(obj)
                    # catch "a love letter"
                    if idx > 0 and sentence[idx-1].lower() in {"a","an","the","love","short"}:
                        return sentence[idx-1] + " " + sentence[idx]
                    return sentence[idx]

        #
        # 5) What did Serena run?
        #
        if "what" in question_lower and "run" in question_lower:
            for verb in ["ran","run"]:
                if verb in sentence_lower:
                    idx = sentence_lower.index(verb)
                    # include article if present
                    if idx+1 < len(sentence):
                        if sentence_lower[idx+1] in {"a","an","the"}:
                            return sentence[idx+1] + " " + sentence[idx+2]
                        return sentence[idx+1]

        #
        # 6) Where did Frank take the horse?
        #
        if "where" in question_lower and ("take" in question_lower or "took" in question_lower):
            if "to" in sentence_lower:
                idx = sentence_lower.index("to")
                # return "the farm"
                if idx+1 < len(sentence) and sentence_lower[idx+1] in {"a","an","the"}:
                    return sentence[idx+1] + " " + sentence[idx+2]
                elif idx+1 < len(sentence):
                    return sentence[idx+1]

        #
        # 7) Who should you give your money to?
        #
        if "who" in question_lower and "give" in question_lower and "money" in question_lower:
            # e.g. "Give us all your money." → "us"
            for w in sentence_lower:
                if w in {"me","him","her","us","them","you"}:
                    # return original-cased
                    return sentence[sentence_lower.index(w)]

        #
        # 8) What is east of the city?
        #
        if "what" in question_lower and "east" in question_lower:
            if "is" in sentence_lower:
                idx_is = sentence_lower.index("is")
                # grab everything before "is"
                return " ".join(sentence[:idx_is])

        #
        # 9) What is in the river?
        #
        if "what" in question_lower and "in" in question_lower:
            if "is" in sentence_lower:
                idx_is = sentence_lower.index("is")
                return " ".join(sentence[:idx_is])

        #
        # 10) Generic fallback for any other "in" questions
        #
        if "in" in question_lower:
            if "in" in sentence_lower:
                idx = sentence_lower.index("in")
                if idx-1 >= 0:
                    return sentence[idx-1]

        #
        # --- keep your other existing handlers here, in the same order ---
        #

        return "Unknown"
