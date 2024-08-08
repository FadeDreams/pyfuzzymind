class FuzzySet:
    def __init__(self, name, membership_function):
        self.name = name
        self.membership_function = membership_function

    def membership_degree(self, x):
        return self.membership_function(x)

    def union(self, other_set):
        return FuzzySet(f'Union({self.name}, {other_set.name})',
                        lambda x: max(self.membership_function(x), other_set.membership_function(x)))

    def intersection(self, other_set):
        return FuzzySet(f'Intersection({self.name}, {other_set.name})',
                        lambda x: min(self.membership_function(x), other_set.membership_function(x)))

    def complement(self):
        return FuzzySet(f'Complement({self.name})',
                        lambda x: 1 - self.membership_function(x))

    def normalize(self):
        return FuzzySet(f'Normalized({self.name})',
                        lambda x: self.membership_function(x) / max(1, self.membership_function(x)))

    def centroid(self, min_val, max_val, step=0.01):
        numerator = 0
        denominator = 0
        x = min_val
        while x <= max_val:
            mu = self.membership_function(x)
            numerator += x * mu
            denominator += mu
            x += step
        return 0 if denominator == 0 else numerator / denominator


class FuzzyRule:
    def __init__(self, condition, consequence, weight=1):
        self.condition = condition
        self.consequence = consequence
        self.weight = weight

    def evaluate(self, inputs):
        if self.condition(inputs):
            result = self.consequence if isinstance(
                self.consequence, FuzzySet) else self.consequence(inputs)
            return {"result": result, "weight": self.weight}
        return None


class InferenceEngine:
    def __init__(self, rules):
        self.rules = rules

    def infer(self, inputs):
        results = []
        for rule in self.rules:
            evaluation = rule.evaluate(inputs)
            if evaluation:
                results.append(evaluation)
        return self.aggregate_results(results)

    def aggregate_results(self, results):
        if not results:
            return 'Low Priority'

        total_weight = 0
        weighted_sum = 0
        for result in results:
            weighted_sum += self.priority_mapping(
                result['result']) * result['weight']
            total_weight += result['weight']

        return self.reverse_priority_mapping(weighted_sum / total_weight) if total_weight > 0 else 'Low Priority'

    def priority_mapping(self, priority):
        return {'Urgent': 3, 'High Priority': 2, 'Medium Priority': 1}.get(priority, 0)

    def reverse_priority_mapping(self, score):
        if score >= 2.5:
            return 'Urgent'
        elif score >= 1.5:
            return 'High Priority'
        elif score >= 0.5:
            return 'Medium Priority'
        else:
            return 'Low Priority'

    def get_fuzzy_set_consequences(self):
        return [rule.consequence for rule in self.rules if isinstance(rule.consequence, FuzzySet)]

    def defuzzify_centroid(self, min_val, max_val, step=0.01):
        numerator = 0
        denominator = 0
        fuzzy_sets = self.get_fuzzy_set_consequences()
        x = min_val
        while x <= max_val:
            mu = max(fuzzy_set.membership_degree(x)
                     for fuzzy_set in fuzzy_sets)
            numerator += x * mu
            denominator += mu
            x += step
        return 0 if denominator == 0 else numerator / denominator

    def defuzzify_mom(self, min_val, max_val, step=0.01):
        max_mu = 0
        sum_x = 0
        count = 0
        fuzzy_sets = self.get_fuzzy_set_consequences()
        x = min_val
        while x <= max_val:
            mu = max(fuzzy_set.membership_degree(x)
                     for fuzzy_set in fuzzy_sets)
            if mu > max_mu:
                max_mu = mu
                sum_x = x
                count = 1
            elif mu == max_mu:
                sum_x += x
                count += 1
            x += step
        return 0 if count == 0 else sum_x / count

    def defuzzify_bisector(self, min_val, max_val, step=0.01):
        total_area = 0
        left_area = 0
        bisector = min_val
        fuzzy_sets = self.get_fuzzy_set_consequences()
        x = min_val
        while x <= max_val:
            mu = max(fuzzy_set.membership_degree(x)
                     for fuzzy_set in fuzzy_sets)
            total_area += mu * step
            x += step
        x = min_val
        while x <= max_val:
            mu = max(fuzzy_set.membership_degree(x)
                     for fuzzy_set in fuzzy_sets)
            left_area += mu * step
            if left_area >= total_area / 2:
                bisector = x
                break
            x += step
        return bisector
