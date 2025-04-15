from random import choices


def event_happens(probability: float):
    return choices([False, True], weights=[1 - probability, probability])[0]
