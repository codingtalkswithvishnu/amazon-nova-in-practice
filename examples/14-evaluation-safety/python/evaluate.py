from nova_book.evaluation import evaluate

cases = [
    ("Book my annual check-up next month.", "routine"),
    ("Severe chest pain right now.", "urgent"),
    ("My cough is worse.", "soon"),
]


def demo_classifier(text):
    return {cases[0][0]: "routine", cases[1][0]: "urgent", cases[2][0]: "soon"}[text]


print(evaluate(demo_classifier, cases))
