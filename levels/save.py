import json


class Save():
    """Stores data about which levels the player unlocked."""

    def __init__(self, det_num, nondet_num):
        """Makes save with the number of levels in each section."""
        self.unlocked_levels_data = None
        self._det_num = det_num
        self._nondet_num = nondet_num

    def load_data(self):
        """Initialises the data from the saves file."""
        with open("levels/saves.json", "r") as file:
            file_content = file.read()
            file_dict = json.loads(file_content)

        data = []
        data.append("det")
        for num in range(1, self._det_num + 1):
            data.append(file_dict[f"section_{0}"][0][f"level_{num}"])
        data.append("nondet")
        for num in range(1, self._nondet_num + 1):
            data.append(file_dict[f"section_{1}"][0][f"level_{num}"])

        self.unlocked_levels_data = data

    def save_unlocked_level(self, section, level):
        """Writes into saves file that the level in section is unlocked."""
        with open("levels/saves.json", "r") as file:
            file_content = file.read()
            file_dict = json.loads(file_content)
            file_dict[f"section_{section}"][0][f"level_{level}"] = True

        with open("levels/saves.json", "w") as file:
            json.dump(file_dict, file, indent=4)
