def mapping_null_values(new_data: dict, old_data: dict):
    for key in old_data.keys():
        new_value = new_data.get(key)
        if new_value is not None:
            old_data[key] = new_value

    old_data.pop("_sa_instance_state", None)
    return old_data
