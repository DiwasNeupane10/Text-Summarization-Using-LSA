import os


def clear_dir(path):
    directory = os.listdir(f"./{path}")
    for dir in directory:
        if dir != ".gitkeep":
            os.remove(os.path.join(f"./{path}", dir))
