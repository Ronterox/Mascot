
def module_path(path):
    return path if __name__ == '__main__' else f"../{path}"
