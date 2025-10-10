import pygame


class Automaton():
    """Automaton with initial, accepting states and transition function."""

    def __init__(self, nondeterministic):
        """Initialises a blank deterministic or nondeterministic automaton."""
        self._is_nondeterministic = nondeterministic
        self._alphabet = ["z", "x", "c", "v"]
        self._current_states = []
        self._initial_states = []
        self._accepting_states = []
        # stores connections of circles and arrows, e.g. from 1 via x to 3
        self._transition_dict = {}
        self._new_transition = [None, None, None] # circle_from, arrow, circle_to

    @property
    def initial_states(self):
        return self._initial_states

    @initial_states.setter
    def initial_states(self, value):
        self._initial_states = value

    @property
    def accepting_states(self):
        return self._accepting_states

    @accepting_states.setter
    def accepting_states(self, value):
        self._accepting_states = value

    @property
    def transition_dict(self):
        return self._transition_dict

    @transition_dict.setter
    def transition_dict(self, value):
        self._transition_dict = value

    @property
    def circle_from(self):
        return self._new_transition[0]

    @circle_from.setter
    def circle_from(self, value):
        self._new_transition[0] = value

    @property
    def arrow(self):
        return self._new_transition[1]

    @arrow.setter
    def arrow(self, value):
        self._new_transition[1] = value

    @property
    def circle_to(self):
        return self._new_transition[2]

    @circle_to.setter
    def circle_to(self, value):
        self._new_transition[2] = value

    def add_initial_state(self, state):
        if state not in self._initial_states:
            self._initial_states.append(state)

    def remove_initial_state(self, state):
        self._initial_states.remove(state)

    def add_accepting_state(self, state):
        if state not in self._accepting_states:
            self._accepting_states.append(state)

    def remove_accepting_state(self, state):
        self._accepting_states.remove(state)

    def handle_new_transition(self, player_group, circle_group):
        """Handles creating a new transition and setting correct initial and or accepting states of automaton."""
        circles = pygame.sprite.spritecollide(
            player_group.sprite, circle_group, False, pygame.sprite.collide_mask)

        # adding circle from -> making sure its clear which circle player wants to make transition from
        if len(circles) == 1 and (not self._new_transition[0]):
            # doesnt need "if circles_from" because player always stands on circle when adding arrow to circle
            self.circle_from = circles[0]
            self.arrow = player_group.sprite.current_arrow
            # adding the current variant of the circle (e.g. if it were initial, before adding it to the automaton)
            self._handle_previous_circle_variants(circles[0])

        # theres only one circle colliding with player
        elif len(circles) == 1:  # adding circle to
            self.circle_to = circles[0]
            self._handle_previous_circle_variants(circles[0])
            self._add_new_transition_to_dict()

    def _handle_previous_circle_variants(self, circle):
        """Adding initial and or accepting state according to the variant of the circle."""
        circle_variant = circle.variant
        match circle_variant:
            case "accepting":
                self.add_accepting_state(circle.number)
            case "initial":
                self.add_initial_state(circle.number)
            case "initial_accepting":
                self.add_initial_state(circle.number)
                self.add_accepting_state(circle.number)

    def _add_new_transition_to_dict(self):
        """Adding new transition from circle_from to circle_to under an empty list of symbols."""
        # adding completely new transition for circle_from
        self._transition_dict.setdefault(
            self.circle_from.number, []).append([[], self.circle_to.number])

        # erasing new transition tracker (used for straight arrows)
        self._new_transition = [None, None, None]

    def _fetch_circle_from_to(self, arrow, circle_group):
        """Returns circle_from and circle_to depending on what point of arrow circle collides with."""
        arrow_circles = pygame.sprite.spritecollide(
            arrow, circle_group, False, pygame.sprite.collide_mask)

        # if player wants to add symbol to arrow, when its not yet attached to circle, it can cause errors due to circle_to variable not being assigned value
        circle_to = None
        # checkinig which circle collides with which point of the arrow, determining which circle is from/to
        for circle in arrow_circles or []:
            # loop arrow
            if len(arrow.points) == 1:
                circle_from = circle
                circle_to = circle
            # straight arrow
            elif pygame.Rect.collidepoint(circle.rect, arrow.points[0]):
                circle_from = circle
            elif pygame.Rect.collidepoint(circle.rect, arrow.points[1]):
                circle_to = circle
        return circle_from, circle_to

    def handle_update_transition(self, arrow, circle_group, new_symbol):
        """Updates transition with given symbol."""
        circle_from, circle_to = self._fetch_circle_from_to(
            arrow, circle_group)

        # setting the variables, updating transition
        if circle_to:
            return self._add_letter_to_transition_in_dict(circle_from, circle_to, new_symbol)
        else:
            # making transition couldnt be completed
            return False

    def _add_letter_to_transition_in_dict(self, circle_from, circle_to, new_symbol):
        """Determines if the symbol exists in any transition, whether it should be added, removed or whether to do nothing."""
        found = False
        delete = False
        transitions = self._transition_dict.get(circle_from.number) or []
        for transition in transitions:
            if new_symbol in transition[0]:
                found = True
                if circle_to.number == transition[1]:
                    delete = True

        # updating transition if the symbol can be added, or deleting was requested
        if not found or self._is_nondeterministic or delete:
            self._update_transition_in_dict(
                circle_from.number, circle_to.number, new_symbol)
        # automaton is deteministic, another symbol to different transition from same state couldnt be added
        else: 
            return 0

    def _update_transition_in_dict(self, circle_from_num, circle_to_num, new_symbol):
        """Find correct transition. Add symbol if it isnt there yet. Remove if it is."""
        # picking existing transitions that have the same circle_from, as the transition thats being added
        transitions = self._transition_dict.get(circle_from_num) or []
        for transition in transitions:
            # transition with same circle_from and circle_to exists, updating symbol associated with the transition
            if circle_to_num == transition[1]:
                if new_symbol in transition[0]:
                    transition[0].remove(new_symbol)
                elif new_symbol not in transition[0]:
                    transition[0].append(new_symbol)

    def handle_delete_transition_entirely(self, arrow, circle_group):
        """Finds transition to be entirely deleted from transition_dict."""
        circle_from, circle_to = self._fetch_circle_from_to(
            arrow, circle_group)

        if circle_from:
            transitions = self._transition_dict.get(circle_from.number) or []
            for transition in transitions:
                # find and delete the transition associated with the arrow (based on circle_from, circle_to)
                if circle_to:
                    if (arrow.symbols == transition[0]) and (circle_to.number == transition[1]):
                        transitions.remove(transition)
                # if not circle to not needed to delete, because transition is only added upon recieving circle to
            # if no outgoing transitions transitions remain from the state, delete the key
            if not transitions:
                self._transition_dict.pop(circle_from.number, None)

            # if in process of creation, reset, so new arrow can be created from scratch
            self._new_transition = [None, None, None]

    def handle_checking_language(self, level_automaton):
        """Checks whether there are errors in user automaton, and if it is equivalent to level automaton."""
        errors = self._handle_errors()
        if errors:
            return errors

        # initialising here, to avoid circular import
        from product_automaton import ProductAutomaton

        if self._is_nondeterministic:
            player_automaton = self.determinise_nfa()
        else:
            player_automaton = self

        product_automaton = ProductAutomaton(player_automaton, level_automaton)
        return product_automaton.check_languages_equivalent()

    def _handle_errors(self):
        """Checking for errors in user automaton."""
        # deterministic automaton cannot have more than 1 initial state
        if ((not self._is_nondeterministic) and len(self._initial_states) > 1):
            return 1  # error code, will be read by helper_dialogue, and text will be displayed
        # automaton must have at least 1 initial state
        elif len(self._initial_states) == 0:
            return 2
        # epsilon transitions arent supported, there must be at least 1 symbol in transition
        for transitions in self._transition_dict.values():
            for transition in transitions:
                if not transition[0]:
                    return 3

    def determinise_nfa(self):
        """Determinises user automaton by using subset construction."""
        # user automaton is converted every time when they want to check if languages are equivalent. player_a in automaton class can be then modified by user again. didnt want to convert already converted automaton
        # list and set cannot be used as dictionary keys
        new_initial_states = [tuple(self._initial_states)]
        new_accepting_states = [tuple(self._accepting_states)]
        for state in new_initial_states:
            if set(self._accepting_states).intersection(set(state)):
                new_accepting_states.append(state)
        new_transition_dict = {}

        queue = []
        visited = set()
        for state in new_initial_states:
            queue.append(state)

        # from nfa construct dfa
        while queue:
            states = queue.pop()
            if states in visited:
                continue  # we already checked this state, protection against looping
            visited.add(states)
            for symbol in self._alphabet:
                new_states = []

                # for every state see what are reachable transitions
                for current_state in states:
                    # using nondeterministic transition function to determinise NFA
                    result = self._transition_function(current_state, symbol)
                    current_new_states = result if result != [-1] else []
                    new_states.extend(current_new_states)
                new_states = tuple(new_states)

                # add the new states to dictionary and queue to be examined
                if new_states:
                    new_transition_dict.setdefault(
                        states, []).append([[symbol], new_states])
                    queue.append(new_states)
                    if set(self._accepting_states).intersection(set(new_states)):
                        new_accepting_states.append(new_states)

        # initialise and return new deterministic automaton for player_a
        new_player_a = Automaton(0)
        new_player_a._initial_states = new_initial_states
        new_player_a._accepting_states = new_accepting_states
        new_player_a._transition_dict = new_transition_dict
        return new_player_a

    # basis of automata logic from: https://www.youtube.com/watch?v=IhUqXgVl6jo
    def _transition_function(self, current_state, symbol):
        """Transition function. Transitions from current_state, through symbol, to a set of states."""
        if current_state == -1:
            return [-1]  # sink state

        # get transitions going from current_state
        outgoing_transitions = self._transition_dict.get(current_state, [])

        # if outgoing transitions exist, search for next_states with: from current_state under symbol to resulting state
        result_states = []
        for state in outgoing_transitions:
            if symbol in state[0]:
                result_states.append(state[1])

        # return result states, if there are none, go to sink state
        return result_states if result_states else [-1]