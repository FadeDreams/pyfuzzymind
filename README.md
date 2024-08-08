### pyFuzzyMind
This library provides a set of classes for implementing fuzzy logic systems in Python. It includes support for defining fuzzy sets, fuzzy rules, and performing inference using an inference engine. It also provides methods for defuzzification using different techniques. For example, you can use this library to build a fuzzy logic-based risk assessment system for financial investments. In this system, fuzzy sets could represent risk levels (such as "Low Risk", "Medium Risk", "High Risk"), and rules could determine investment strategies based on market indicators. The inference engine would evaluate these rules to suggest an appropriate investment strategy, and defuzzification methods like the Mean of Maximum (MOM) could be used to provide a precise risk score for decision-making.

#### FuzzySet
Represents a fuzzy set with a membership function. Provides methods for operations on fuzzy sets.

```python
FuzzySet(name, membership_function)
# name: The name of the fuzzy set.
# membership_function: A function that defines the membership degree of the set.
```
##### Methods
- membership_degree(x): Returns the membership degree of x.
- union(other_set): Returns a new fuzzy set representing the union of this set and other_set.
- intersection(other_set): Returns a new fuzzy set representing the intersection of this set and other_set.
- complement(): Returns a new fuzzy set representing the complement of this set.
- normalize(): Returns a new fuzzy set with a normalized membership function.
- centroid(min, max, step): Performs defuzzification using the centroid method.

#### FuzzyRule
Represents a fuzzy rule consisting of a condition and a consequence.

```python
FuzzyRule(condition, consequence, weight=1)
# condition: A function that takes inputs and returns a boolean indicating if the rule condition is satisfied.
# consequence: The result of the rule if the condition is true. Can be a fuzzy set or a function.
# weight: An optional weight for the rule (default is 1).
```
##### Methods
- evaluate(inputs): Evaluates the rule against the given inputs and returns the result and weight if the condition is satisfied.
#### InferenceEngine
Uses a set of fuzzy rules to perform inference and defuzzification.
```python
InferenceEngine(rules)
# rules: A list of FuzzyRule instances.
```
##### Methods
- infer(inputs): Performs inference based on the input values and returns the aggregated result.
- aggregate_results(results): Aggregates results from the fuzzy rules.
- defuzzify_centroid(min, max, step): Performs defuzzification using the centroid method.
- defuzzify_mom(min, max, step): Performs defuzzification using the Mean of Maxima (MOM) method.
- defuzzify_bisector(min, max, step): Performs defuzzification using the Bisector method.
- get_fuzzy_set_consequences(): Returns a list of fuzzy sets as consequences of the rules.

##### Example Usage
```python
from pyfuzzymind import FuzzySet, FuzzyRule, InferenceEngine
InferenceEngine(rules)

# Define fuzzy sets for urgency and complexity
urgency_set = FuzzySet('Urgency', lambda urgency: 0 if urgency < 3 else (urgency - 3) / 4 if urgency < 7 else 1)
complexity_set = FuzzySet('Complexity', lambda complexity: 0 if complexity < 2 else (complexity - 2) / 3 if complexity < 5 else 1)

# Define fuzzy rules
rules = [
    FuzzyRule(
        lambda inputs: urgency_set.membership_degree(inputs['urgency']) > 0.7 and complexity_set.membership_degree(inputs['complexity']) > 0.7,
        FuzzySet('Urgent', lambda x: 1 if x >= 7 else x / 7)
    ),
    FuzzyRule(
        lambda inputs: urgency_set.membership_degree(inputs['urgency']) > 0.5,
        lambda inputs: 'High Priority'
    ),
    FuzzyRule(
        lambda inputs: complexity_set.membership_degree(inputs['complexity']) > 0.5,
        lambda inputs: 'Medium Priority'
    ),
    FuzzyRule(
        lambda inputs: urgency_set.membership_degree(inputs['urgency']) <= 0.5 and complexity_set.membership_degree(inputs['complexity']) <= 0.5,
        lambda inputs: 'Low Priority'
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

```
