from collections import deque

class SemanticNetsAgent:
    def __init__(self):
        # No initialization needed for this implementation
        pass

    def solve(self, initial_sheep, initial_wolves):
        # Define the initial state
        initial_state = (initial_sheep, initial_wolves, 0, 0, 1)  # (left_sheep, left_wolves, right_sheep, right_wolves, boat_position)

        # Define the goal state
        goal_state = (0, 0, initial_sheep, initial_wolves, 0)

        # Queue for BFS and set for visited states
        queue = deque([(initial_state, [])])
        visited = set()

        # Helper function to check if a state is valid
        def is_valid_state(state):
            ls, lw, rs, rw, _ = state
            if ls < 0 or lw < 0 or rs < 0 or rw < 0:
                return False
            if (ls > 0 and ls < lw) or (rs > 0 and rs < rw):
                return False
            return True

        # Define possible moves (sheep, wolves)
        moves = [(1, 0), (0, 1), (1, 1), (2, 0), (0, 2)]

        while queue:
            current_state, path = queue.popleft()

            # Skip already visited states
            if current_state in visited:
                continue

            visited.add(current_state)

            # Check if goal state is reached
            if current_state == goal_state:
                return path

            # Generate next states
            for move in moves:
                sheep, wolves = move
                ls, lw, rs, rw, boat = current_state

                if boat == 1:  # Boat on the left side
                    new_state = (ls - sheep, lw - wolves, rs + sheep, rw + wolves, 0)
                else:  # Boat on the right side
                    new_state = (ls + sheep, lw + wolves, rs - sheep, rw - wolves, 1)

                # Add the new state only if it's valid and hasn't been visited
                if is_valid_state(new_state) and new_state not in visited:
                    queue.append((new_state, path + [(sheep, wolves)]))

        # No solution found
        return []

