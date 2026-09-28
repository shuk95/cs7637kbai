class BlockWorldAgent:
    def __init__(self):
        #If you want to do any initial processing, add it here.
        pass

    def solve(self, initial_arrangement, goal_arrangement):    
        # Step 1: Convert lists into a dictionary representation
        def build_block_map(arrangement):
            block_map = {}
            for stack in arrangement:
                for i, block in enumerate(stack):
                    block_map[block] = stack[i - 1] if i > 0 else "Table"
            return block_map
        
        initial_map = build_block_map(initial_arrangement)
        goal_map = build_block_map(goal_arrangement)
        
        # Step 2: Identify misplaced blocks
        misplaced_blocks = {block for block in initial_map if initial_map[block] != goal_map[block]}
        
        # Step 3: Move blocks into correct position
        while misplaced_blocks:
            for block in list(misplaced_blocks):
                correct_location = goal_map[block]
                current_location = initial_map[block]
                
                # Ensure the block has no dependencies on top before moving it
                if not any(initial_map[b] == block for b in misplaced_blocks):
                    moves.append((block, correct_location))
                    initial_map[block] = correct_location
                    misplaced_blocks.remove(block)
        
        return moves



