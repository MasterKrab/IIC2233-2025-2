def create_id_generator(id: int = 0):
    def generate():
        nonlocal id
        id += 1
        return id - 1

    return generate
