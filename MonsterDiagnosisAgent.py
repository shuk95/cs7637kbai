import itertools

class MonsterDiagnosisAgent:
    def __init__(self):
        pass

    def combine_effects(self, subset, diseases):
        net_effect = {chr(c): 0 for c in range(ord('A'), ord('Z') + 1)}
        for disease in subset:
            for vit, effect in diseases[disease].items():
                if effect == "+":
                    net_effect[vit] += 1
                elif effect == "-":
                    net_effect[vit] -= 1
                # '0' has no effect

        result = {}
        for vit, value in net_effect.items():
            if value > 0:
                result[vit] = "+"
            elif value < 0:
                result[vit] = "-"
            else:
                result[vit] = "0"
        return result

    def matches(self, combined, patient):
        return all(combined[vit] == patient[vit] for vit in patient)

    def solve(self, diseases, patient):
        disease_names = list(diseases.keys())
        for r in range(1, len(disease_names) + 1):
            for combo in itertools.combinations(disease_names, r):
                combined = self.combine_effects(combo, diseases)
                #print(combo)
                #print(diseases)
                if self.matches(combined, patient):
                    return list(combo)
                    
        return []
