import json

from automaton import Automaton


class Level():
    """Represents a level in game. Stores associated infomration."""

    def __init__(self, section, level):
        """Create a blank level."""
        self.section = section
        self.max_levels_in_current_section = None
        self.level = level
        self.text_lines = None
        self.language = None
        self.automaton = None

    def initialize_data(self):
        """Initialising the level data from a json file."""
        with open("levels.json", "r", encoding="utf-8") as file:
            file_content = file.read()
            file_dict = json.loads(file_content)

            self.max_levels_in_current_section = len(
                file_dict[f"section_{self.section}"])
            # levels are indexed from 1 in menu, but from 0 in dictionary
            level_index = self.level - 1

            initial_states = file_dict[f"section_{self.section}"][level_index]["initial_states"]
            accepting_states = file_dict[f"section_{self.section}"][level_index]["accepting_states"]
            transition_dict = file_dict[f"section_{self.section}"][level_index]["transition_dict"]
            # converting json keys from strings to ints
            transition_dict = {int(key): value for key,
                               value in transition_dict.items()}
            self.language = file_dict[f"section_{self.section}"][level_index]["language"]
            self.text_lines = file_dict[f"section_{self.section}"][level_index]["text_lines"]

            # 0 -> DFA since DFA and NFA recognise the same languages. deterministic product automaton makes language checking easier
            self.automaton = Automaton(0)
            self.automaton.initial_states = initial_states
            self.automaton.accepting_states = accepting_states
            self.automaton.transition_dict = transition_dict
