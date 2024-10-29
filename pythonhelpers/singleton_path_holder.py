import os.path

from pythonhelpers.singleton_metaclass import SingletonMetaclass


def make_singleton_path_holder(folder_name: str, start_folder: str = os.getcwd(), max_depth: int = 5):
    """
    Creates a singleton path holder for a specified folder within a defined search depth.

    :param folder_name: Name of the folder for which a singleton path holder will be made.
    :param max_depth: Maximum depth to search for the folder upwards and downwards.
    :return: A singleton path holder class with a method to construct paths relative to the found folder.
    :raises FileNotFoundError: If the specified folder is not found within the search depth.
    :raises FileExistsError: If multiple instances of the specified folder are found.
    """

    def find_folder() -> list:
        """
        Find a folder within max_depth levels above or below the starting directory.

        :param folder_name: Name of the folder to find.
        :param start_dir: Directory to start the search from.
        :param max_depth: Maximum depth to search upwards and downwards.
        :return: List of paths to the folders that match the folder_name.
        """
        matching_folders = []

        # Helper to search downwards
        def search_down(current_dir: str, current_depth: int, max_depth: int):
            if current_depth > max_depth:
                return
            for root, dirs, files in os.walk(current_dir):
                if folder_name in dirs:
                    matching_folders.append(os.path.join(root, folder_name))
                if current_depth < max_depth:
                    for d in dirs:
                        search_down(os.path.join(root, d), current_depth + 1, max_depth)

        # Helper to search upwards
        def search_up(current_dir: str, current_depth: int, max_depth: int):
            if current_depth > max_depth:
                return
            parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
            if parent_dir == current_dir:  # Reached root of filesystem
                return
            if folder_name in os.listdir(parent_dir):
                matching_folders.append(os.path.join(parent_dir, folder_name))
            search_up(parent_dir, current_depth + 1, max_depth)

        search_down(start_folder, 0, max_depth)
        search_up(start_folder, 0, max_depth)

        matching_folders = list(set(matching_folders))

        return matching_folders

    folders = find_folder()
    if len(folders) == 0:
        raise FileNotFoundError(f'Impossible to find the folder "{folder_name}"')
    elif len(folders) > 1:
        raise FileExistsError(f'Found several folders "{folder_name}": {folders}')

    class _SingletonPathHolder(metaclass=SingletonMetaclass):
        """
        A singleton class to manage and generate filesystem paths.

        This class ensures that there is only one instance maintaining the root directory path
        and provides a method to create full paths by appending resource names to the root path.

        Attributes:
            root (str): The root directory path.

        Methods:
            make_path(resource_name: str = "") -> str:
                Constructs a full filesystem path by appending the given resource name to the root path.
        """
        root: str = folders[0]

        def make_path(self, resource_name: str = "") -> str:
            return os.path.join(self.root, resource_name)

    return _SingletonPathHolder
