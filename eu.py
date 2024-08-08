from pyfuzzymind.pyfuzzymind import FuzzyRule, FuzzySet, InferenceEngine

# Define fuzzy sets for urgency and complexity
urgency_set = FuzzySet('Urgency', lambda urgency: 0 if urgency < 3 else (
    urgency - 3) / 4 if urgency < 7 else 1)
complexity_set = FuzzySet('Complexity', lambda complexity: 0 if complexity < 2 else (
    complexity - 2) / 3 if complexity < 5 else 1)

# Define fuzzy rules
rules = [
    FuzzyRule(
        lambda inputs: urgency_set.membership_degree(
            inputs['urgency']) > 0.7 and complexity_set.membership_degree(inputs['complexity']) > 0.7,
        FuzzySet('Urgent', lambda x: 1 if x >= 7 else x / 7)
    ),
    FuzzyRule(
        lambda inputs: urgency_set.membership_degree(inputs['urgency']) > 0.5,
        lambda _: 'High Priority'
    ),
    FuzzyRule(
        lambda inputs: complexity_set.membership_degree(
            inputs['complexity']) > 0.5,
        lambda _: 'Medium Priority'
    ),
    FuzzyRule(
        lambda inputs: urgency_set.membership_degree(
            inputs['urgency']) <= 0.5 and complexity_set.membership_degree(inputs['complexity']) <= 0.5,
        lambda _: 'Low Priority'
    )
]

engine = InferenceEngine(rules)

# Example ticket
ticket = {'urgency': 8, 'complexity': 6}
priority = engine.infer(ticket)
print(f'Ticket Priority: {priority}')

# Defuzzification examples
centroid = urgency_set.centroid(0, 10)
print(f'Centroid defuzzification: {centroid}')

defuzzified_centroid = engine.defuzzify_centroid(0, 10)
print(f'Defuzzified Centroid: {defuzzified_centroid}')

defuzzified_mom = engine.defuzzify_mom(0, 10)
print(f'Defuzzified MOM: {defuzzified_mom}')

defuzzified_bisector = engine.defuzzify_bisector(0, 10)
print(f'Defuzzified Bisector: {defuzzified_bisector}')
