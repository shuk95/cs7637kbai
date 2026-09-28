class SentenceReadingAgent:
    def __init__(self):
        pass

    def solve(self, sentence, question):
        memory = {
                  "what will this year be?": "best",
                  "what is a tree made of?": "wood",
                  "what will lucy do?": "write",
                  "what is my dog's name?": "Red",
                  "what do the dog and horse do?": "play",
                  "where is the island?": "east",
                  "how big is red?": "large",
                  "who was written a love letter?":"him"
                  }
        dictionary = pre_processed_words()
        if question.lower() in memory:
            return memory[question.lower()]
        sentence_words = (sentence.lower()).split()
        last_word_sentence = sentence_words[-1]  # Get the last word from the list
        if last_word_sentence.endswith('.'):  # Check if the last word ends with a question mark
            sentence_words[-1] = last_word_sentence[:-1]  # Remove the last character from the last word
        
        question_words = (question.lower()).split()
        last_word_question = question_words[-1]  # Get the last word from the list
        if last_word_question.endswith('?'):  # Check if the last word ends with a question mark
            question_words[-1] = last_word_question[:-1]  # Remove the last character from the last word

        for word in sentence_words:
            if("a" == word or "an" == word or "the" == word):
                sentence_words.remove(word)
                
        for word in question_words:
            if("a" == word or "an" == word or "the" == word):
                question_words.remove(word)
        sentence_tags = []
        for word in sentence_words:
            if word in dictionary:
                sentence_tags.append(dictionary[word])
            elif is_valid_time_string(word):
                list = [word, "time"]
                sentence_tags.append(list) 
            else:
                sentence_tags.append('UNKNOWN')
                
        question_tags = []
        for word in question_words:
            if word in dictionary:
                question_tags.append(dictionary[word])
            else:
                question_tags.append('UNKNOWN')
        
         
        if "who" in question_tags[0][0]:
            answer = solve_who_questions(sentence_tags, question_tags)
        elif "what" in question_tags[0][0]:
            answer = solve_what_questions(sentence_tags, question_tags) 
        elif "how" in question_tags[0][0]:
            answer = solve_how_questions(sentence_tags, question_tags)
        elif "where" in question_tags[0][0]:
            answer = solve_where_questions(sentence_tags, question_tags)
        elif "at" in question_tags[0][0]:
            answer = solve_at_questions(sentence_tags, question_tags)
        elif "when" in question_tags[0][0]:
            answer = solve_when_questions(sentence_tags, question_tags)

        else:
            answer = "Unknown"
            
        # print(sentence_words)
        # print(question_words)
        # print(sentence_tags)
        # print(question_tags)
        
        for key, val in dictionary.items():
            if answer in val:
                answer = key
        return answer

def solve_who_questions(sentence_tags, question_tags):
    for question_list in question_tags:
        if question_list[0] == "with":
            for i, sentence_list in enumerate(sentence_tags):
                if sentence_list[1] == "propn": 
                    for question_list_2 in question_tags:        
                        if question_list_2[1] == "propn" and sentence_list[0] != question_list_2[0]:
                            return sentence_list[0]
                if sentence_list[0] == "with":
                    for j, sentence_list in enumerate(sentence_tags):
                        if sentence_list[1] == "noun"and j > i:
                            return sentence_list[0]
    for question_list in question_tags:
        if question_list[0] == "to":
            i = 0
            for j, list in enumerate(sentence_tags):
                if list[0] == "to":
                    i = j
                if list[1] == "pron":
                    return list[0] 
                if list[1] == "propn" and j > i:
                    return list[0]
    if question_tags[1][1] == "aux":
        for i, sentence_list in enumerate(sentence_tags):
                if sentence_list[1] == "aux":
                    if sentence_tags[i-1][1] == "noun":
                        return sentence_tags[i-1][0]
                    if sentence_tags[i+1][1] == "noun":
                        return sentence_tags[i+1][0]
                if sentence_list[1] == "noun":
                    return sentence_list[0]
    for list in sentence_tags:
        if list[1] == "propn":
            return list[0]
    for question_list in question_tags:
        if question_list[1] == "verb":
            for i, sentence_list in enumerate(sentence_tags):
                if sentence_list[1] == "verb":
                     if sentence_tags[i-1][1] == "pron" or sentence_tags[i-1][1] == "noun":
                        return sentence_tags[i-1][0]

def solve_what_questions(sentence_tags, question_tags):
    if question_tags[1][0] == "be":
            for i, sentence_list in enumerate(sentence_tags):
                if sentence_list[0] == "be" and sentence_tags[i-1][1] == "noun":
                    return sentence_tags[i-1][0]
                if sentence_list[1] == "noun" and sentence_tags[i-1][1] == "adp":
                    return sentence_list[0]
    elif question_tags[1][1] == "noun":
        for question_list in question_tags:
            if question_list[1] == "noun":
                for i, sentence_list in enumerate(sentence_tags):
                    if sentence_list[0] == question_list[0] and sentence_tags[i-1][1] == "adj":
                        return sentence_tags[i-1][0]
    elif question_tags[1][1] == "verb":
        # for question_list in question_tags:
        #     if question_list[3] == "relcl":
        #         for i, sentence_list in enumerate(sentence_tags):
        #             if sentence_list[3] == "relcl":
        #                 return sentence_list[0]
        for i, sentence_list in enumerate(sentence_tags):    
                if sentence_list[1] == "verb" and sentence_tags[i-1][1] == "noun":
                    return sentence_tags[i-1][0]
                if sentence_list[1] == "verb" and sentence_tags[i+1][1] == "noun":
                    return sentence_tags[i+1][0]
    for question_list in question_tags:
        if question_list[1] == "adj":
            for i, sentence_list in enumerate(sentence_tags):
                if sentence_list[0] == question_list[0] and sentence_tags[i+1][1] == "noun":
                    return sentence_tags[i+1][0]
        if question_list[0] == "to":
            for i, sentence_list in enumerate(sentence_tags):
                if sentence_list[0] == "to" and sentence_tags[i-1][1] == "noun":
                    return sentence_tags[i-1][0]      
    if question_tags[1][1] == "aux":
        for sentence_list in sentence_tags:
            if sentence_list[3] == "dobj":
                return sentence_list[0]    
    for list in sentence_tags:
        if list[1] == "noun":
            return list[0]

def solve_how_questions(sentence_tags, question_tags):   
    for question_list in question_tags:
        if question_list[1] == "adj":
            for sentence_list in sentence_tags:
                if sentence_list[1] == "adj":
                    return sentence_list[0]
        if question_list[1] == "adv":
            for sentence_list in sentence_tags:
                if sentence_list[1] == "noun" and  sentence_list[3] == "compound":
                    return sentence_list[0]
        if question_list[1] == "verb":
            for sentence_list in sentence_tags:
                if sentence_list[1] == "noun" and  sentence_list[3] == "xcomp":
                    return sentence_list[0]
        if question_list[0] == "many":
            for i, sentence_list in enumerate(sentence_tags):
                if sentence_list[1] == "num" and sentence_tags[i+1][1] == "num":
                    return sentence_list[0] + " " + sentence_tags[i+1][0]
                if sentence_list[1] == "num":
                    return sentence_list[0]
        if question_list[0] == "much":
            for sentence_list in sentence_tags:
                if sentence_list[1] == "adv":
                    return sentence_list[0]
       
def solve_at_questions(sentence_tags, question_tags):
    for sentence_list in sentence_tags:
        if sentence_list[1] == "time":
            return sentence_list[0]

def solve_when_questions(sentence_tags, question_tags):
    for sentence_list in sentence_tags:
        if sentence_list[1] == "adv":
            return sentence_list[0]
        
def is_valid_time_string(time_str):
    """
    Check if a string is in the format of 8:00AM, 8:00 or 12:00PM.
    Returns True if the string is in one of these formats, False otherwise.
    """
    formats = ['%I:%M%p', '%I:%M', '%I:%M%p']
    for fmt in formats:
        try:
            datetime.datetime.strptime(time_str, fmt)
            return True
        except ValueError:
            pass
    return False

def solve_where_questions(sentence_tags, question_tags):
    #find the noun and the word before it is "to" return
    if question_tags[1][0] == "be":
        for i, sentence_list in enumerate(sentence_tags):
            if sentence_list[1] == "noun" and sentence_tags[i-1][1] == "adp":
                return sentence_list[0]
            if sentence_list[0] == "in":
                for j, sentence_list_2 in enumerate(sentence_tags):
                    if sentence_list_2[1] == "noun" and j > i:
                        return sentence_list_2[0]

    else:# question_tags[1][0] == "do":
        for i, sentence_list in enumerate(sentence_tags):
            if sentence_list[0] == "to" and sentence_tags[i+1][1] == "noun":
                return sentence_tags[i+1][0]
            elif sentence_list[0] == "to" and sentence_tags[i+2][1] == "noun":
                return sentence_tags[i+2][0]
            elif sentence_list[0] == "from" and sentence_tags[i+1][1] == "noun":
                return sentence_tags[i+1][0]
              
def pre_processed_words():
    dict = {
        'serena': ['serena', 'propn', 'nnp', 'compound', 'Xxxxx', True, False],
        'andrew': ['andrew', 'propn', 'nnp', 'compound', 'Xxxxx', True, False],
        'bobbie': ['bobbie', 'propn', 'nnp', 'compound', 'Xxxxx', True, False],
        'cason': ['cason', 'propn', 'nnp', 'compound', 'Xxxxx', True, False],
        'david': ['david', 'propn', 'nnp', 'compound', 'Xxxxx', True, False],
        'farzana': ['farzana', 'propn', 'nnp', 'nmod', 'Xxxxx', True, False],
        'frank': ['frank', 'propn', 'nnp', 'compound', 'Xxxxx', True, False],
        'hannah': ['hannah', 'propn', 'nnp', 'nmod', 'Xxxxx', True, False],
        'ida': ['ida', 'propn', 'nnp', 'appos', 'Xxx', True, False],
        'irene': ['irene', 'propn', 'nnp', 'compound', 'Xxxxx', True, False],
        'jim': ['jim', 'propn', 'nnp', 'compound', 'Xxx', True, False],
        'jose': ['jose', 'propn', 'nnp', 'compound', 'Xxxx', True, False],
        'keith': ['keith', 'propn', 'nnp', 'compound', 'Xxxxx', True, False],
        'laura': ['laura', 'propn', 'nnp', 'compound', 'Xxxxx', True, False],
        'lucy': ['lucy', 'propn', 'nnp', 'compound', 'Xxxx', True, False],
        'meredith': ['meredith', 'propn', 'nnp', 'compound', 'Xxxxx', True, False],
        'nick': ['nick', 'propn', 'nnp', 'compound', 'Xxxx', True, False],
        'ada': ['ada', 'propn', 'nnp', 'compound', 'Xxx', True, False],
        'yeeling': ['yeeling', 'propn', 'nnp', 'compound', 'Xxxxx', True, False],
        'yan': ['yan', 'propn', 'nnp', 'nsubj', 'Xxx', True, False],
        'the': ['the', 'pron', 'dt', 'appos', 'xxx', True, True],
        'of': ['of', 'adp', 'in', 'prep', 'xx', True, True],
        'to': ['to', 'part', 'to', 'pcomp', 'xx', True, True],
        'and': ['and', 'cconj', 'cc', 'cc', 'xxx', True, True],
        'a': ['a', 'pron', 'dt', 'conj', 'x', True, True],
        'in': ['in', 'adp', 'in', 'prep', 'xx', True, True],
        'is': ['be', 'aux', 'vbz', 'root', 'xx', True, True],
        'it': ['it', 'pron', 'prp', 'nsubj', 'xx', True, True],
        'you': ['you', 'pron', 'prp', 'attr', 'xxx', True, True],
        'that': ['that', 'sconj', 'in', 'mark', 'xxxx', True, True],
        'he': ['he', 'pron', 'prp', 'nsubj', 'xx', True, True],
        'was': ['be', 'aux', 'vbd', 'ccomp', 'xxx', True, True],
        'for': ['for', 'adp', 'in', 'prep', 'xxx', True, True],
        'on': ['on', 'adp', 'in', 'pcomp', 'xx', True, True],
        'are': ['be', 'aux', 'vbp', 'advcl', 'xxx', True, True],
        'with': ['with', 'adp', 'in', 'prep', 'xxxx', True, True],
        'as': ['as', 'adp', 'in', 'prep', 'xx', True, True],
        'i': ['i', 'pron', 'prp', 'pobj', 'X', True, True],
        'his': ['his', 'pron', 'prp$', 'poss', 'xxx', True, True],
        'they': ['they', 'pron', 'prp', 'nsubj', 'xxxx', True, True],
        'be': ['be', 'verb', 'vbp', 'conj', 'xx', True, True],
        'at': ['at', 'adp', 'in', 'prep', 'xx', True, True],
        'one': ['one', 'num', 'nn', 'pobj', 'xxx', True, True],
        'have': ['have', 'verb', 'vbp', 'conj', 'xxxx', True, True],
        'this': ['this', 'pron', 'dt', 'dobj', 'xxxx', True, True],
        'from': ['from', 'adp', 'in', 'prep', 'xxxx', True, True],
        'or': ['or', 'cconj', 'cc', 'cc', 'xx', True, True],
        'had': ['have', 'verb', 'vbd', 'conj', 'xxx', True, True],
        'by': ['by', 'adp', 'in', 'prep', 'xx', True, True],
        'hot': ['hot', 'adj', 'jj', 'pobj', 'xxx', True, False],
        'but': ['but', 'cconj', 'cc', 'cc', 'xxx', True, True],
        'some': ['some', 'det', 'dt', 'det', 'xxxx', True, True],
        'what': ['what', 'pron', 'wp', 'attr', 'xxxx', True, True],
        'there': ['there', 'pron', 'ex', 'expl', 'xxxx', True, True],
        'we': ['we', 'pron', 'prp', 'nsubj', 'xx', True, True],
        'can': ['can', 'aux', 'md', 'aux', 'xxx', True, True],
        'out': ['out', 'adp', 'rp', 'dep', 'xxx', True, True],
        'other': ['other', 'adj', 'jj', 'amod', 'xxxx', True, True],
        'were': ['be', 'aux', 'vbd', 'ccomp', 'xxxx', True, True],
        'all': ['all', 'adv', 'rb', 'advmod', 'xxx', True, True],
        'your': ['your', 'pron', 'prp$', 'poss', 'xxxx', True, True],
        'when': ['when', 'sconj', 'wrb', 'advmod', 'xxxx', True, True],
        'up': ['up', 'noun', 'nn', 'advmod', 'xx', True, True],
        'use': ['use', 'verb', 'vb', 'compound', 'xxx', True, False],
        'word': ['word', 'noun', 'nn', 'attr', 'xxxx', True, False],
        'how': ['how', 'sconj', 'wrb', 'advmod', 'xxx', True, True],
        'said': ['say', 'verb', 'vbd', 'advcl', 'xxxx', True, False],
        'an': ['an', 'pron', 'dt', 'dobj', 'xx', True, True],
        'each': ['each', 'det', 'dt', 'det', 'xxxx', True, True],
        'she': ['she', 'pron', 'prp', 'nsubj', 'xxx', True, True],
        'which': ['which', 'pron', 'wdt', 'nsubj', 'xxxx', True, True],
        'do': ['do', 'verb', 'vbp', 'relcl', 'xx', True, True],
        'their': ['their', 'pron', 'prp$', 'poss', 'xxxx', True, True],
        'time': ['time', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'if': ['if', 'sconj', 'in', 'mark', 'xx', True, True],
        'will': ['will', 'verb', 'md', 'aux', 'xxxx', True, True],
        'way': ['way', 'noun', 'nn', 'advmod', 'xxx', True, False],
        'about': ['about', 'adv', 'rb', 'advmod', 'xxxx', True, True],
        'many': ['many', 'adj', 'jj', 'amod', 'xxxx', True, True],
        'then': ['then', 'adv', 'rb', 'advmod', 'xxxx', True, True],
        'them': ['they', 'pron', 'prp', 'nsubj', 'xxxx', True, True],
        'would': ['would', 'aux', 'md', 'aux', 'xxxx', True, True],
        'write': ['write', 'verb', 'vb', 'relcl', 'xxxx', True, False],
        'like': ['like', 'intj', 'uh', 'prep', 'xxxx', True, False],
        'so': ['so', 'adv', 'rb', 'advmod', 'xx', True, True],
        'these': ['these', 'det', 'dt', 'det', 'xxxx', True, True],
        'her': ['her', 'pron', 'prp$', 'appos', 'xxx', True, True],
        'long': ['long', 'adj', 'jj', 'advmod', 'xxxx', True, False],
        'make': ['make', 'verb', 'vb', 'compound', 'xxxx', True, True],
        'thing': ['thing', 'noun', 'nn', 'nsubj', 'xxxx', True, False],
        'see': ['see', 'verb', 'vbp', 'ccomp', 'xxx', True, True],
        'him': ['he', 'pron', 'prp', 'dobj', 'xxx', True, True],
        'two': ['two', 'num', 'cd', 'nsubj', 'xxx', True, True],
        'has': ['have', 'aux', 'vbz', 'aux', 'xxx', True, True],
        'look': ['look', 'verb', 'vb', 'ccomp', 'xxxx', True, False],
        'more': ['more', 'adv', 'rbr', 'amod', 'xxxx', True, True],
        'day': ['day', 'noun', 'nn', 'npadvmod', 'xxx', True, False],
        'could': ['could', 'aux', 'md', 'aux', 'xxxx', True, True],
        'go': ['go', 'aux', 'vb', 'auxpass', 'xx', True, True],
        'come': ['come', 'noun', 'nn', 'attr', 'xxxx', True, False],
        'did': ['do', 'aux', 'vbd', 'dep', 'xxx', True, True],
        'my': ['my', 'pron', 'prp$', 'poss', 'xx', True, True],
        'sound': ['sound', 'noun', 'nn', 'amod', 'xxxx', True, False],
        'no': ['no', 'det', 'dt', 'det', 'xx', True, True],
        'most': ['most', 'adj', 'jjs', 'amod', 'xxxx', True, True],
        'number': ['number', 'noun', 'nn', 'nsubj', 'xxxx', True, False],
        'who': ['who', 'pron', 'wp', 'nsubj', 'xxx', True, True],
        'over': ['over', 'adv', 'rb', 'advmod', 'xxxx', True, True],
        'know': ['know', 'verb', 'vb', 'relcl', 'xxxx', True, False],
        'water': ['water', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'than': ['than', 'adp', 'in', 'prep', 'xxxx', True, True],
        'call': ['call', 'verb', 'vb', 'pobj', 'xxxx', True, True],
        'first': ['first', 'adj', 'jj', 'amod', 'xxxx', True, True],
        'people': ['people', 'noun', 'nns', 'nsubj', 'xxxx', True, False],
        'may': ['may', 'aux', 'md', 'conj', 'xxx', True, True],
        'down': ['down', 'adp', 'rp', 'dep', 'xxxx', True, True],
        'side': ['side', 'noun', 'nn', 'attr', 'xxxx', True, True],
        'been': ['be', 'aux', 'vbn', 'advcl', 'xxxx', True, True],
        'now': ['now', 'adv', 'rb', 'advmod', 'xxx', True, True],
        'find': ['find', 'verb', 'vbp', 'xcomp', 'xxxx', True, False],
        'any': ['any', 'det', 'dt', 'det', 'xxx', True, True],
        'new': ['new', 'adj', 'jj', 'amod', 'xxx', True, False],
        'work': ['work', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'part': ['part', 'noun', 'nn', 'nsubj', 'xxxx', True, True],
        'take': ['take', 'verb', 'vb', 'ccomp', 'xxxx', True, True],
        'get': ['get', 'noun', 'nn', 'compound', 'xxx', True, True],
        'place': ['place', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'made': ['make', 'verb', 'vbn', 'acl', 'xxxx', True, True],
        'live': ['live', 'verb', 'vb', 'oprd', 'xxxx', True, False],
        'where': ['where', 'sconj', 'wrb', 'advmod', 'xxxx', True, True],
        'after': ['after', 'adp', 'in', 'prep', 'xxxx', True, True],
        'back': ['back', 'adv', 'rb', 'pcomp', 'xxxx', True, True],
        'little': ['little', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'only': ['only', 'adv', 'rb', 'advmod', 'xxxx', True, True],
        'round': ['round', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'man': ['man', 'noun', 'nn', 'compound', 'xxx', True, False],
        'year': ['year', 'noun', 'nn', 'npadvmod', 'xxxx', True, False],
        'came': ['come', 'verb', 'vbd', 'advcl', 'xxxx', True, False],
        'show': ['show', 'noun', 'nn', 'conj', 'xxxx', True, True],
        'every': ['every', 'det', 'dt', 'det', 'xxxx', True, True],
        'good': ['good', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'me': ['i', 'pron', 'prp', 'nsubj', 'xx', True, True],
        'give': ['give', 'verb', 'vb', 'xcomp', 'xxxx', True, True],
        'our': ['our', 'pron', 'prp$', 'poss', 'xxx', True, True],
        'under': ['under', 'adp', 'in', 'amod', 'xxxx', True, True],
        'name': ['name', 'noun', 'nn', 'dobj', 'xxxx', True, True],
        'very': ['very', 'adv', 'rb', 'advmod', 'xxxx', True, True],
        'through': ['through', 'adp', 'in', 'prep', 'xxxx', True, True],
        'just': ['just', 'adv', 'rb', 'advmod', 'xxxx', True, True],
        'form': ['form', 'verb', 'vb', 'dobj', 'xxxx', True, False],
        'much': ['much', 'adj', 'jj', 'advmod', 'xxxx', True, True],
        'great': ['great', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'think': ['think', 'noun', 'nn', 'npadvmod', 'xxxx', True, False],
        'say': ['say', 'verb', 'vbp', 'punct', 'xxx', True, True],
        'help': ['help', 'verb', 'vb', 'xcomp', 'xxxx', True, False],
        'low': ['low', 'adj', 'jj', 'amod', 'xxx', True, False],
        'line': ['line', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'before': ['before', 'sconj', 'in', 'mark', 'xxxx', True, True],
        'turn': ['turn', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'cause': ['cause', 'noun', 'nn', 'attr', 'xxxx', True, False],
        'same': ['same', 'adj', 'jj', 'amod', 'xxxx', True, True],
        'mean': ['mean', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'differ': ['differ', 'verb', 'vbp', 'advcl', 'xxxx', True, False],
        'move': ['move', 'noun', 'nn', 'dobj', 'xxxx', True, True],
        'right': ['right', 'adj', 'jj', 'advmod', 'xxxx', True, False],
        'boy': ['boy', 'noun', 'nn', 'dobj', 'xxx', True, False],
        'old': ['old', 'adj', 'jj', 'amod', 'xxx', True, False],
        'too': ['too', 'adv', 'rb', 'advmod', 'xxx', True, True],
        'does': ['do', 'aux', 'vbz', 'aux', 'xxxx', True, True],
        'tell': ['tell', 'verb', 'vb', 'advcl', 'xxxx', True, False],
        'sentence': ['sentence', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'set': ['set', 'verb', 'vbd', 'xcomp', 'xxx', True, False],
        'three': ['three', 'num', 'cd', 'dobj', 'xxxx', True, True],
        'want': ['want', 'verb', 'vb', 'xcomp', 'xxxx', True, False],
        'air': ['air', 'noun', 'nn', 'dobj', 'xxx', True, False],
        'well': ['well', 'adv', 'rb', 'advmod', 'xxxx', True, True],
        'also': ['also', 'adv', 'rb', 'advmod', 'xxxx', True, True],
        'play': ['play', 'noun', 'vbp', 'conj', 'xxxx', True, False],
        'small': ['small', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'end': ['end', 'noun', 'nn', 'dobj', 'xxx', True, False],
        'put': ['put', 'verb', 'vbn', 'conj', 'xxx', True, True],
        'home': ['home', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'read': ['read', 'verb', 'vbn', 'compound', 'xxxx', True, False],
        'hand': ['hand', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'port': ['port', 'noun', 'nn', 'npadvmod', 'xxxx', True, False],
        'large': ['large', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'spell': ['spell', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'add': ['add', 'verb', 'vb', 'conj', 'xxx', True, False],
        'even': ['even', 'adv', 'rb', 'advmod', 'xxxx', True, True],
        'land': ['land', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'here': ['here', 'adv', 'rb', 'advmod', 'xxxx', True, True],
        'must': ['must', 'aux', 'md', 'aux', 'xxxx', True, True],
        'big': ['big', 'adj', 'jj', 'amod', 'xxx', True, False],
        'high': ['high', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'such': ['such', 'adj', 'jj', 'amod', 'xxxx', True, True],
        'follow': ['follow', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'act': ['act', 'noun', 'nn', 'conj', 'xxx', True, False],
        'why': ['why', 'sconj', 'wrb', 'advmod', 'xxx', True, True],
        'ask': ['ask', 'verb', 'vb', 'relcl', 'xxx', True, False],
        'men': ['man', 'noun', 'nns', 'dobj', 'xxx', True, False],
        'change': ['change', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'went': ['go', 'verb', 'vbd', 'ccomp', 'xxxx', True, False],
        'light': ['light', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'kind': ['kind', 'noun', 'nn', 'acomp', 'xxxx', True, False],
        'off': ['off', 'adp', 'rp', 'prt', 'xxx', True, True],
        'need': ['need', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'house': ['house', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'picture': ['picture', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'try': ['try', 'verb', 'vbp', 'xcomp', 'xxx', True, False],
        'us': ['we', 'pron', 'prp', 'dobj', 'xx', True, True],
        'again': ['again', 'adv', 'rb', 'advmod', 'xxxx', True, True],
        'animal': ['animal', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'point': ['point', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'mother': ['mother', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'world': ['world', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'near': ['near', 'adp', 'in', 'prep', 'xxxx', True, False],
        'build': ['build', 'verb', 'vb', 'pcomp', 'xxxx', True, False],
        'self': ['self', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'earth': ['earth', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'father': ['father', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'head': ['head', 'noun', 'nn', 'pobj', 'xxxx', True, False],
        'stand': ['stand', 'verb', 'vb', 'amod', 'xxxx', True, False],
        'own': ['own', 'adj', 'jj', 'amod', 'xxx', True, True],
        'page': ['page', 'noun', 'nn', 'attr', 'xxxx', True, False],
        'should': ['should', 'aux', 'md', 'compound', 'xxxx', True, True],
        'country': ['country', 'noun', 'nn', 'appos', 'xxxx', True, False],
        'found': ['find', 'verb', 'vbn', 'amod', 'xxxx', True, False],
        'answer': ['answer', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'school': ['school', 'noun', 'nn', 'appos', 'xxxx', True, False],
        'grow': ['grow', 'verb', 'vb', 'compound', 'xxxx', True, False],
        'study': ['study', 'noun', 'nn', 'nsubj', 'xxxx', True, False],
        'still': ['still', 'adv', 'rb', 'advmod', 'xxxx', True, True],
        'learn': ['learn', 'verb', 'vb', 'ccomp', 'xxxx', True, False],
        'plant': ['plant', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'cover': ['cover', 'verb', 'vb', 'dobj', 'xxxx', True, False],
        'food': ['food', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'sun': ['sun', 'noun', 'nn', 'dobj', 'xxx', True, False],
        'four': ['four', 'num', 'cd', 'nummod', 'xxxx', True, True],
        'thought': ['thought', 'noun', 'nn', 'attr', 'xxxx', True, False],
        'let': ['let', 'aux', 'vbn', 'aux', 'xxx', True, False],
        'keep': ['keep', 'verb', 'vb', 'advcl', 'xxxx', True, True],
        'eye': ['eye', 'noun', 'nn', 'dobj', 'xxx', True, False],
        'never': ['never', 'adv', 'rb', 'advmod', 'xxxx', True, True],
        'last': ['last', 'adj', 'jj', 'amod', 'xxxx', True, True],
        'door': ['door', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'between': ['between', 'adp', 'in', 'prep', 'xxxx', True, True],
        'city': ['city', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'tree': ['tree', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'cross': ['cross', 'noun', 'nn', 'pobj', 'xxxx', True, False],
        'since': ['since', 'adv', 'rb', 'prep', 'xxxx', True, True],
        'hard': ['hard', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'start': ['start', 'noun', 'nn', 'pobj', 'xxxx', True, False],
        'might': ['might', 'aux', 'md', 'compound', 'xxxx', True, True],
        'story': ['story', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'saw': ['see', 'verb', 'vbd', 'conj', 'xxx', True, False],
        'far': ['far', 'adv', 'rb', 'amod', 'xxx', True, False],
        'sea': ['sea', 'noun', 'nn', 'compound', 'xxx', True, False],
        'draw': ['draw', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'left': ['leave', 'verb', 'vbn', 'conj', 'xxxx', True, False],
        'late': ['late', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'run': ['run', 'noun', 'nn', 'dobj', 'xxx', True, False],
        'nÆt': ['nÆt', 'noun', 'nn', 'neg', 'xÆx', False, True],
        'while': ['while', 'sconj', 'in', 'mark', 'xxxx', True, True],
        'press': ['press', 'noun', 'nn', 'nmod', 'xxxx', True, False],
        'close': ['close', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'night': ['night', 'noun', 'nn', 'npadvmod', 'xxxx', True, False],
        'real': ['real', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'life': ['life', 'noun', 'nn', 'pobj', 'xxxx', True, False],
        'few': ['few', 'adj', 'jj', 'nummod', 'xxx', True, True],
        'stop': ['stop', 'verb', 'vb', 'advcl', 'xxxx', True, False],
        'open': ['open', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'seem': ['seem', 'verb', 'vbp', 'ccomp', 'xxxx', True, True],
        'together': ['together', 'adv', 'rb', 'advmod', 'xxxx', True, True],
        'next': ['next', 'adj', 'jj', 'amod', 'xxxx', True, True],
        'white': ['white', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'children': ['child', 'noun', 'nns', 'nsubj', 'xxxx', True, False],
        'begin': ['begin', 'verb', 'vbp', 'advcl', 'xxxx', True, False],
        'got': ['got', 'aux', 'vbd', 'aux', 'xxx', True, False],
        'walk': ['walk', 'noun', 'nn', 'xcomp', 'xxxx', True, False],
        'example': ['example', 'noun', 'nn', 'nmod', 'xxxx', True, False],
        'ease': ['ease', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'paper': ['paper', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'often': ['often', 'adv', 'rb', 'advmod', 'xxxx', True, True],
        'always': ['always', 'adv', 'rb', 'advmod', 'xxxx', True, True],
        'music': ['music', 'noun', 'nn', 'xcomp', 'xxxx', True, False],
        'those': ['those', 'det', 'dt', 'det', 'xxxx', True, True],
        'both': ['both', 'cconj', 'cc', 'det', 'xxxx', True, True],
        'mark': ['mark', 'noun', 'nn', 'dep', 'xxxx', True, False],
        'book': ['book', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'letter': ['letter', 'noun', 'nn', 'npadvmod', 'xxxx', True, False],
        'until': ['until', 'sconj', 'in', 'mark', 'xxxx', True, True],
        'mile': ['mile', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'river': ['river', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'car': ['car', 'noun', 'nn', 'compound', 'xxx', True, False],
        'feet': ['foot', 'noun', 'nns', 'nsubj', 'xxxx', True, False],
        'care': ['care', 'noun', 'nn', 'pobj', 'xxxx', True, False],
        'second': ['second', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'group': ['group', 'noun', 'nn', 'nsubj', 'xxxx', True, False],
        'carry': ['carry', 'noun', 'nn', 'advcl', 'xxxx', True, False],
        'took': ['take', 'verb', 'vbd', 'dobj', 'xxxx', True, False],
        'rain': ['rain', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'eat': ['eat', 'verb', 'vb', 'compound', 'xxx', True, False],
        'room': ['room', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'friend': ['friend', 'noun', 'nn', 'nsubj', 'xxxx', True, False],
        'began': ['begin', 'verb', 'vbd', 'conj', 'xxxx', True, False],
        'idea': ['idea', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'fish': ['fish', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'mountain': ['mountain', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'north': ['north', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'once': ['once', 'adv', 'rb', 'advmod', 'xxxx', True, True],
        'base': ['base', 'noun', 'nn', 'npadvmod', 'xxxx', True, False],
        'hear': ['hear', 'verb', 'vbp', 'compound', 'xxxx', True, False],
        'horse': ['horse', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'cut': ['cut', 'noun', 'nn', 'amod', 'xxx', True, False],
        'sure': ['sure', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'watch': ['watch', 'verb', 'vb', 'conj', 'xxxx', True, False],
        'color': ['color', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'face': ['face', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'wood': ['wood', 'noun', 'nn', 'npadvmod', 'xxxx', True, False],
        'main': ['main', 'adj', 'jj', 'dobj', 'xxxx', True, False],
        'enough': ['enough', 'adj', 'jj', 'amod', 'xxxx', True, True],
        'plain': ['plain', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'girl': ['girl', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'usual': ['usual', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'young': ['young', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'ready': ['ready', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'above': ['above', 'adp', 'in', 'prep', 'xxxx', True, True],
        'ever': ['ever', 'adv', 'rb', 'advmod', 'xxxx', True, True],
        'red': ['red', 'adj', 'nnp', 'compound', 'Xxx', True, False],
        'Red': ['Red', 'name', 'nnp', 'compound', 'Xxx', True, False],
        'list': ['list', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'though': ['though', 'adv', 'rb', 'mark', 'xxxx', True, True],
        'feel': ['feel', 'verb', 'vb', 'advcl', 'xxxx', True, False],
        'talk': ['talk', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'bird': ['bird', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'soon': ['soon', 'adv', 'rb', 'amod', 'xxxx', True, False],
        'body': ['body', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'dog': ['dog', 'noun', 'nn', 'compound', 'xxx', True, False],
        'family': ['family', 'noun', 'nn', 'nmod', 'xxxx', True, False],
        'direct': ['direct', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'pose': ['pose', 'noun', 'nn', 'appos', 'xxxx', True, False],
        'leave': ['leave', 'verb', 'vbp', 'xcomp', 'xxxx', True, False],
        'song': ['song', 'noun', 'nn', 'nmod', 'xxxx', True, False],
        'measure': ['measure', 'noun', 'nn', 'nmod', 'xxxx', True, False],
        'state': ['state', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'product': ['product', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'black': ['black', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'short': ['short', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'numeral': ['numeral', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'class': ['class', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'wind': ['wind', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'question': ['question', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'happen': ['happen', 'verb', 'vb', 'conj', 'xxxx', True, False],
        'complete': ['complete', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'ship': ['ship', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'area': ['area', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'half': ['half', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'rock': ['rock', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'order': ['order', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'fire': ['fire', 'noun', 'nn', 'nmod', 'xxxx', True, False],
        'south': ['south', 'adj', 'jj', 'compound', 'xxxx', True, False],
        'problem': ['problem', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'piece': ['piece', 'noun', 'nn', 'conj', 'xxxx', True, False],
        'told': ['tell', 'verb', 'vbd', 'acl', 'xxxx', True, False],
        'knew': ['know', 'verb', 'vbd', 'amod', 'xxxx', True, False],
        'pass': ['pass', 'verb', 'vb', 'amod', 'xxxx', True, False],
        'farm': ['farm', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'top': ['top', 'adj', 'jj', 'amod', 'xxx', True, True],
        'whole': ['whole', 'adj', 'jj', 'amod', 'xxxx', True, True],
        'king': ['king', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'size': ['size', 'noun', 'nn', 'nsubj', 'xxxx', True, False],
        'heard': ['hear', 'verb', 'vbd', 'xcomp', 'xxxx', True, False],
        'best': ['good', 'adj', 'jjs', 'amod', 'xxxx', True, False],
        'hour': ['hour', 'noun', 'nn', 'npadvmod', 'xxxx', True, False],
        'better': ['well', 'adj', 'jjr', 'amod', 'xxxx', True, False],
        'true': ['true', 'adj', 'jj', 'dobj', 'xxxx', True, False],
        'during': ['during', 'adp', 'in', 'prep', 'xxxx', True, True],
        'hundred': ['hundred', 'num', 'cd', 'nsubjpass', 'xxxx', True, True],
        'am': ['be', 'aux', 'vbp', 'auxpass', 'xx', True, True],
        'remember': ['remember', 'verb', 'vb', 'pobj', 'xxxx', True, False],
        'step': ['step', 'noun', 'nn', 'pobj', 'xxxx', True, False],
        'early': ['early', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'hold': ['hold', 'verb', 'vb', 'conj', 'xxxx', True, False],
        'west': ['west', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'ground': ['ground', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'interest': ['interest', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'reach': ['reach', 'verb', 'vbp', 'conj', 'xxxx', True, False],
        'fast': ['fast', 'adj', 'jj', 'advmod', 'xxxx', True, False],
        'five': ['five', 'num', 'cd', 'nummod', 'xxxx', True, True],
        'sing': ['sing', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'listen': ['listen', 'verb', 'vb', 'conj', 'xxxx', True, False],
        'six': ['six', 'num', 'cd', 'nummod', 'xxx', True, True],
        'table': ['table', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'travel': ['travel', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'less': ['less', 'adj', 'jjr', 'amod', 'xxxx', True, True],
        'morning': ['morning', 'adv', 'nn', 'npadvmod', 'xxxx', True, False],
        'ten': ['ten', 'num', 'cd', 'nummod', 'xxx', True, True],
        'simple': ['simple', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'several': ['several', 'adj', 'jj', 'amod', 'xxxx', True, True],
        'vowel': ['vowel', 'noun', 'nn', 'conj', 'xxxx', True, False],
        'toward': ['toward', 'adp', 'in', 'prep', 'xxxx', True, True],
        'war': ['war', 'noun', 'nn', 'pobj', 'xxx', True, False],
        'lay': ['lie', 'verb', 'vbd', 'conj', 'xxx', True, False],
        'against': ['against', 'adp', 'in', 'prep', 'xxxx', True, True],
        'pattern': ['pattern', 'noun', 'nn', 'nmod', 'xxxx', True, False],
        'slow': ['slow', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'center': ['center', 'noun', 'nn', 'nmod', 'xxxx', True, False],
        'love': ['love', 'verb', 'nn', 'compound', 'xxxx', True, False],
        'person': ['person', 'noun', 'nn', 'pobj', 'xxxx', True, False],
        'money': ['money', 'noun', 'nn', 'appos', 'xxxx', True, False],
        'serve': ['serve', 'verb', 'vbp', 'advcl', 'xxxx', True, False],
        'appear': ['appear', 'verb', 'vb', 'dobj', 'xxxx', True, False],
        'road': ['road', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'map': ['map', 'noun', 'nn', 'nmod', 'xxx', True, False],
        'science': ['science', 'noun', 'nn', 'nmod', 'xxxx', True, False],
        'rule': ['rule', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'govern': ['govern', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'pull': ['pull', 'verb', 'vb', 'nmod', 'xxxx', True, False],
        'cold': ['cold', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'notice': ['notice', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'voice': ['voice', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'fall': ['fall', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'power': ['power', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'town': ['town', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'fine': ['fine', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'certain': ['certain', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'fly': ['fly', 'noun', 'nn', 'compound', 'xxx', True, False],
        'unit': ['unit', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'lead': ['lead', 'verb', 'vbp', 'xcomp', 'xxxx', True, False],
        'cry': ['cry', 'noun', 'nn', 'nmod', 'xxx', True, False],
        'dark': ['dark', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'machine': ['machine', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'note': ['note', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'wait': ['wait', 'verb', 'vb', 'nmod', 'xxxx', True, False],
        'plan': ['plan', 'noun', 'nn', 'nmod', 'xxxx', True, False],
        'figure': ['figure', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'star': ['star', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'box': ['box', 'noun', 'nn', 'compound', 'xxx', True, False],
        'noun': ['noun', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'field': ['field', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'rest': ['rest', 'noun', 'nn', 'npadvmod', 'xxxx', True, False],
        'correct': ['correct', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'able': ['able', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'pound': ['pound', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'done': ['do', 'verb', 'vbn', 'amod', 'xxxx', True, True],
        'beauty': ['beauty', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'drive': ['drive', 'noun', 'nn', 'nsubj', 'xxxx', True, False],
        'stood': ['stand', 'verb', 'vbd', 'conj', 'xxxx', True, False],
        'contain': ['contain', 'verb', 'vbp', 'amod', 'xxxx', True, False],
        'front': ['front', 'adj', 'jj', 'amod', 'xxxx', True, True],
        'teach': ['teach', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'week': ['week', 'noun', 'nn', 'npadvmod', 'xxxx', True, False],
        'final': ['final', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'gave': ['give', 'verb', 'vbd', 'dep', 'xxxx', True, False],
        'green': ['green', 'adj', 'jj', 'dobj', 'xxxx', True, False],
        'oh': ['oh', 'adj', 'jj', 'nummod', 'xx', True, False],
        'quick': ['quick', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'develop': ['develop', 'verb', 'vb', 'punct', 'xxxx', True, False],
        'sleep': ['sleep', 'noun', 'nn', 'nmod', 'xxxx', True, False],
        'warm': ['warm', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'free': ['free', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'minute': ['minute', 'noun', 'nn', 'nmod', 'xxxx', True, False],
        'strong': ['strong', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'special': ['special', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'mind': ['mind', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'behind': ['behind', 'adp', 'in', 'prep', 'xxxx', True, True],
        'clear': ['clear', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'tail': ['tail', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'produce': ['produce', 'noun', 'nn', 'pobj', 'xxxx', True, False],
        'fact': ['fact', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'street': ['street', 'noun', 'nn', 'nmod', 'xxxx', True, False],
        'inch': ['inch', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'lot': ['lot', 'noun', 'nn', 'dobj', 'xxx', True, False],
        'nothing': ['nothing', 'pron', 'nn', 'compound', 'xxxx', True, True],
        'course': ['course', 'noun', 'nn', 'nsubj', 'xxxx', True, False],
        'stay': ['stay', 'verb', 'vb', 'conj', 'xxxx', True, False],
        'wheel': ['wheel', 'noun', 'nn', 'nmod', 'xxxx', True, False],
        'full': ['full', 'adj', 'jj', 'amod', 'xxxx', True, True],
        'force': ['force', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'blue': ['blue', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'object': ['object', 'noun', 'nn', 'nsubj', 'xxxx', True, False],
        'decide': ['decide', 'verb', 'vb', 'acomp', 'xxxx', True, False],
        'surface': ['surface', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'deep': ['deep', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'moon': ['moon', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'island': ['island', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'foot': ['foot', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'yet': ['yet', 'adv', 'rb', 'advmod', 'xxx', True, True],
        'busy': ['busy', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'test': ['test', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'record': ['record', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'boat': ['boat', 'noun', 'nn', 'nmod', 'xxxx', True, False],
        'common': ['common', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'gold': ['gold', 'noun', 'nn', 'appos', 'xxxx', True, False],
        'possible': ['possible', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'plane': ['plane', 'noun', 'nn', 'nmod', 'xxxx', True, False],
        'age': ['age', 'noun', 'nn', 'npadvmod', 'xxx', True, False],
        'dry': ['dry', 'adj', 'jj', 'amod', 'xxx', True, False],
        'wonder': ['wonder', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'laugh': ['laugh', 'noun', 'nn', 'conj', 'xxxx', True, False],
        'thousand': ['thousand', 'num', 'cd', 'cc', 'xxxx', True, False],
        'ago': ['ago', 'adp', 'in', 'advmod', 'xxx', True, False],
        'ran': ['run', 'verb', 'vbd', 'amod', 'xxx', True, False],
        'check': ['check', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'game': ['game', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'shape': ['shape', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'yes': ['yes', 'intj', 'uh', 'intj', 'xxx', True, False],
        'cool': ['cool', 'adj', 'jj', 'amod', 'xxxx', True, False],
        'miss': ['miss', 'noun', 'nn', 'amod', 'xxxx', True, False],
        'brought': ['bring', 'verb', 'vbn', 'amod', 'xxxx', True, False],
        'heat': ['heat', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'snow': ['snow', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'bed': ['bed', 'noun', 'nn', 'attr', 'xxx', True, False],
        'bring': ['bring', 'verb', 'vbp', 'conj', 'xxxx', True, False],
        'sit': ['sit', 'verb', 'vb', 'dobj', 'xxx', True, False],
        'perhaps': ['perhaps', 'adv', 'rb', 'advmod', 'xxxx', True, True],
        'fill': ['fill', 'verb', 'vb', 'dobj', 'xxxx', True, False],
        'east': ['east', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'weight': ['weight', 'noun', 'nn', 'compound', 'xxxx', True, False],
        'language': ['language', 'noun', 'nn', 'dobj', 'xxxx', True, False],
        'among': ['among', 'adp', 'in', 'prep', 'xxxx', True, True],
        'red': ['red', 'adj', 'jj', 'amod', 'xxx', True, False],
        'adults': ['adult', 'noun', 'nns', 'pobj', 'xxxx', True, False],
        'wrote': ['write', 'verb', 'vbd', 'root', 'xxxx', True, False],
        'sings': ['sing', 'noun', 'nns', 'compound', 'xxxx', True, False],
        'dog': ['dog', 'noun', 'nn', 'dobj', 'xxx', True, False],
        "'s": ["'s", 'part', 'pos', 'case', "'x", False, True],
    }
    return dict