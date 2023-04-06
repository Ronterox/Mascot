
def module_path(path, main):
    return f"../{path}" if main == '__main__' else path
