def create_id_generator():
    id = 0

    def increment_id():
        nonlocal id
        id += 1
        return id

    return increment_id
