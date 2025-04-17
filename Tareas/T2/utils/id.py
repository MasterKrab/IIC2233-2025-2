def create_id_generator(start: int = 1):
    id = start - 1

    def increment_id():
        nonlocal id
        id += 1
        return id

    return increment_id
