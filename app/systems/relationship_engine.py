def should_support(entity, target):
    init_relationship(entity)
    entity_id = ensure_handle(entity)

    ensure_handle(target)

    # friends support
    if target["handle"] in relationships[entity_id]["friends"]:
        return True

    # dating support
    if target["handle"] in relationships[entity_id]["dating"]:
        return True

    # family support
    if target["handle"] in relationships[entity_id]["family"]:
        return True

    return False
