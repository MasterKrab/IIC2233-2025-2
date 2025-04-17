from random import choices


def event_happens(probability: float):
    """
    Returns True with a given probability.
    """

    return choices([False, True], weights=[1 - probability, probability])[0]
