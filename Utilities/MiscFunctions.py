import math, sys, gc, pympler, os

import numpy as np
from pympler import asizeof
import DIContainer


def get_classes_counts():
    """Returns how many images contains each cluster"""
    k = DIContainer.image_searcher.k
    predicted_values = DIContainer.image_searcher.predicted_values
    counts = np.zeros(k, dtype='int')
    for i in range(0, len(predicted_values)):
        counts[predicted_values[i]] += 1

    return counts


def actual_size(input_obj):
    memory_size = 0
    ids = set()
    objects = [input_obj]
    while objects:
        new = []
        for obj in objects:
            if id(obj) not in ids:
                ids.add(id(obj))
                memory_size += sys.getsizeof(obj)
                new.append(obj)
        objects = gc.get_referents(*new)
    return memory_size


def print_collection_size(collection, name: str):
    size = asizeof.asizeof(collection)
    formated_size = size
    unit = "Bytes"

    if (size / math.pow(10, 3) > 1):
        formated_size = str(size / math.pow(10, 3)).split(".")[0]
        unit = "KB"

    print(f"Size of {len(collection) if isinstance(collection, list) else 1} {name}: {formated_size} {unit}")


def get_all_texture_images():
    texture_images = []
    for obj in DIContainer.scene.objects:
        texture_images.append(obj.material.texture_image)

    return texture_images


def format_number_string(number: int):
    formatted = '{:,}'.format(number)
    return formatted

def get_dataset_length(directory):
    files = os.listdir(directory)
    return len(files)

