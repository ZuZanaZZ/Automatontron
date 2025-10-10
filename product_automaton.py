from automaton import Automaton


class ProductAutomaton(Automaton):
    """Product automaton simulating player_automaton and level_automaton."""

    def __init__(self, player_automaton, level_automaton):
        """Creates product automaton and initialises initial states."""
        super().__init__(0)  # the input automata for product automaton are always deterministic, so product automaton is deterministic as well
        self._player_a = player_automaton
        self._level_a = level_automaton

        self._initial_states = []
        for state_u, state_l in zip(self._player_a._initial_states, self._level_a._initial_states):
            self._initial_states.append((state_u, state_l))

    def check_languages_equivalent(self):
        """Checks if the languages of user automaton and level automaton are equivalent."""
        queue = []
        for initial_state in self._initial_states:
            queue.append((initial_state, ""))
        visited = set()

        while queue:
            current_state, current_word = queue.pop()

            counter_examples = self._check_accepting_states(
                current_state, current_word)
            if counter_examples:
                return counter_examples  # languages arent equivalent, return the offending string

            for symbol in self._alphabet:
                if (current_state, symbol) in visited:
                    continue

                state_u, state_l = self._transition_function(current_state, symbol)
                # if next states exist (under this symbol), check if both states arent a sink state
                if not ((state_u == - 1) and (state_l == - 1)):
                    queue.append(
                        ((state_u, state_l), current_word + symbol))
                    # add to visited, so we will not repeat further
                    visited.add((current_state, symbol))

        return True  # languages are equivalent

    def _check_accepting_states(self, current_state, current_word):
        """Check if user automaton does accept and level automaton doesnt, or vice versa."""
        if ((current_state[0] in self._player_a._accepting_states) and (current_state[1] not in self._level_a._accepting_states)):
            # automaton shouldnt accept string, does
            return (current_word, False)
        if ((current_state[0] not in self._player_a._accepting_states) and (current_state[1] in self._level_a._accepting_states)):
            # automaton should accept string, doesnt
            return (current_word, True)

    def _transition_function(self, current_state, symbol):
        """Returns next state of product automaton."""
        state_u = self._player_a._transition_function(current_state[0], symbol)
        state_l = self._level_a._transition_function(current_state[1], symbol)
        # automata are deterministic, no need for list of next states
        return (state_u[0], state_l[0])