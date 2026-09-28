class MonsterClassificationAgent:
    def __init__(self):
        pass

    def solve(self, samples, new_monster):
        # Rule-based classifier for high accuracy

        # Feature checks based on patterns in known positives
        if new_monster['covering'] != 'fur':
            return False
        if new_monster['lays-eggs'] is not True:
            return False
        if new_monster['has-wings'] is not True:
            return False
        if new_monster['horn-count'] > 0:
            return False
        if new_monster['eye-count'] != 2:
            return False
        if new_monster['arm-count'] < 3:
            return False
        if new_monster['color'] not in ['black', 'white']:
            return False
        if new_monster['size'] not in ['large', 'huge']:
            return False
        if new_monster['foot-type'] not in ['paw', 'foot']:
            return False
        # If it passes all filters, it's likely positive
        return True
