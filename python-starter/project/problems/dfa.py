from project.problem import Problem
import argparse

class DfaProblem(Problem):

    def initialize_parser(self, parser: argparse.ArgumentParser):
        """
        Initialize the parser with the necessary arguments for the DFA problem.
        """
        parser.add_argument('--check', help='Words to check, separated by commas', type=str)
    
    def is_chosen_problem(self, args):
        """
        Check if this problem is chosen based on the provided arguments.
        """
        return bool(args.check)

    def run(self, args):
        """
        Run the DFA simulation logic.
        """
        input_file = args.input
        output_file = args.output
        
        # Split the given string into a list of words
        words_to_check = args.check.split(',')

        # Read the input file and remove empty lines and trailing spaces
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        # Extract DFA components from the first 4 lines
        states = lines[0].split()          
        alphabet = lines[1].split()        
        start_state = lines[2]             
        final_states = set(lines[3].split()) 

        # Parse the transitions (from the 5th line onwards)
        transitions = {}
        for line in lines[4:]:
            parts = line.split()
            if len(parts) == 3:
                curr_st, symbol, next_st = parts
                # Store transition as a tuple key: (current_state, symbol) -> next_state
                transitions[(curr_st, symbol)] = next_st

        # Test each word against the DFA
        results = []
        for word in words_to_check:
            current_state = start_state
            is_valid = True
            
            for symbol in word:
                # Check if there is a valid transition for the current symbol
                if (current_state, symbol) in transitions:
                    current_state = transitions[(current_state, symbol)]
                else:
                    # If no valid transition, the automaton gets stuck and rejects the word
                    is_valid = False
                    break
            
            # If the word is fully processed and we are in a final state, it's accepted
            if is_valid and current_state in final_states:
                results.append("IGEN")
            else:
                results.append("NEM")

        # Write the results into the output file, separated by newlines
        with open(output_file, 'w') as f:
            f.write('\n'.join(results) + '\n')