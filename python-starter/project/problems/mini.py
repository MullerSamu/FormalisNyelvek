from project.problem import Problem
import argparse
import re

class MiniProblem(Problem):

    def initialize_parser(self, parser: argparse.ArgumentParser):
        """
        Initialize the parser with the --mini argument for minimization.
        """
        parser.add_argument('--mini', help='Minimize the given DFA', action='store_true')
    
    def is_chosen_problem(self, args):
        """
        Check if the minimization problem is chosen.
        """
        return bool(args.mini)

    def get_num(self, state_str):
        """
        Helper method to extract the integer number from a state string.
        E.g., 'q12' -> 12, 's2' -> 2.
        """
        nums = re.findall(r'\d+', state_str)
        return int(nums[0]) if nums else 0

    def run(self, args):
        """
        Run the DFA minimization (Moore's algorithm / Equivalence classes).
        """
        input_file = args.input
        output_file = args.output
        
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        orig_states = lines[0].split()
        alphabet = lines[1].split()
        start_state = lines[2]
        orig_final_states = set(lines[3].split())
        
        transitions = {state: {} for state in orig_states}

        # Parse transitions and perform basic error checking
        for line in lines[4:]:
            parts = line.split()
            if len(parts) == 3:
                curr_st, symbol, next_st = parts
                
                # Check if states and symbols are valid based on the definitions
                if curr_st not in orig_states or next_st not in orig_states or symbol not in alphabet:
                    print(f"Hiba: Ervenytelen allapot vagy szimbolum az atmenetben: {line}")
                    return
                
                transitions[curr_st][symbol] = next_st

        # Step 1: Remove unreachable states
        reachable = set([start_state])
        unprocessed = [start_state]
        while unprocessed:
            curr = unprocessed.pop(0)
            for sym, nxt in transitions[curr].items():
                if nxt not in reachable:
                    reachable.add(nxt)
                    unprocessed.append(nxt)
                    
        # Filter original definitions to keep only reachable states
        orig_states = [s for s in orig_states if s in reachable]
        orig_final_states = orig_final_states.intersection(reachable)

        # Step 2: Initialize equivalence classes (Final vs. Non-Final states)
        non_final_states = set(orig_states) - orig_final_states
        partitions = []
        if orig_final_states:
            partitions.append(orig_final_states)
        if non_final_states:
            partitions.append(non_final_states)

        # Step 3: Moore's algorithm to refine partitions
        while True:
            new_partitions = []
            for group in partitions:
                splits = {}
                for state in group:
                    # Create a signature of where this state goes for each symbol
                    signature = []
                    for sym in alphabet:
                        next_st = transitions[state].get(sym)
                        target_idx = -1
                        if next_st:
                            # Find which partition the target state belongs to
                            for i, p in enumerate(partitions):
                                if next_st in p:
                                    target_idx = i
                                    break
                        signature.append(target_idx)
                    signature = tuple(signature)
                    
                    if signature not in splits:
                        splits[signature] = set()
                    splits[signature].add(state)
                
                new_partitions.extend(splits.values())
            
            # If no groups were split, the partitions are final
            if len(new_partitions) == len(partitions):
                break
            partitions = new_partitions

        # Step 4: Determine new minimum names for the merged groups
        group_rep = {}
        for group in partitions:
            # Find the state with the smallest number in the group
            sorted_group = sorted(list(group), key=self.get_num)
            rep = sorted_group[0]
            new_name = f"s{self.get_num(rep)}"
            for state in group:
                group_rep[state] = new_name

        # Step 5: Construct the new minimal DFA
        min_states = sorted(list(set(group_rep.values())), key=self.get_num)
        min_start = group_rep[start_state]
        min_finals = sorted(list(set([group_rep[s] for s in orig_final_states])), key=self.get_num)
        
        min_transitions = set()
        for state in orig_states:
            for sym, next_st in transitions[state].items():
                min_transitions.add((group_rep[state], sym, group_rep[next_st]))
                
        # Sort transitions: first by source node, then symbol, then target node
        sorted_transitions = sorted(list(min_transitions), key=lambda x: (self.get_num(x[0]), x[1], self.get_num(x[2])))

        # Step 6: Write to output file
        with open(output_file, 'w') as f:
            f.write(" ".join(min_states) + "\n")
            f.write(" ".join(alphabet) + "\n")
            f.write(min_start + "\n")
            f.write(" ".join(min_finals) + "\n")
            for src, sym, dst in sorted_transitions:
                f.write(f"{src} {sym} {dst}\n")