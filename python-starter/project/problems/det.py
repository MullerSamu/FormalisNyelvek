from project.problem import Problem
import argparse

class DetProblem(Problem):

    def initialize_parser(self, parser: argparse.ArgumentParser):
        """
        Kezeli a 2. feladathoz tartozó parancssori argumentumot.
        """
        parser.add_argument('--det', help='Determinizálja az adott automatát', action='store_true')
    
    def is_chosen_problem(self, args):
        """
        Ha a --det flag jelen van, ez a probléma fut le.
        """
        return bool(args.det)

    def run(self, args):
        input_file = args.input
        output_file = args.output
        
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        orig_states = lines[0].split()
        alphabet = lines[1].split()
        start_state = lines[2]
        orig_final_states = set(lines[3].split())
        
        
        nfa_transitions = {}
        for state in orig_states:
            for symbol in alphabet:
                nfa_transitions[(state, symbol)] = set()

        for line in lines[4:]:
            parts = line.split()
            if len(parts) == 3:
                curr_st, symbol, next_st = parts
                
        
                if curr_st not in orig_states or next_st not in orig_states or symbol not in alphabet:
                    print(f"Hiba: Érvénytelen állapot vagy szimbólum az átmenetben: {line}")
                    return
                
                nfa_transitions[(curr_st, symbol)].add(next_st)

        
        
        dfa_states = {} 
        dfa_state_names = []
        dfa_transitions = []
        unprocessed_states = []

        
        start_set = tuple([start_state])
        dfa_states[start_set] = "s0"
        dfa_state_names.append("s0")
        unprocessed_states.append(start_set)
        
        state_counter = 1

        
        while unprocessed_states:
            current_set = unprocessed_states.pop(0)
            current_name = dfa_states[current_set]
            
        
            for symbol in alphabet:
                next_set_list = set()
        
                for state in current_set:
        
                    if (state, symbol) in nfa_transitions:
                        next_set_list.update(nfa_transitions[(state, symbol)])
                
        
                if next_set_list:
        
                    next_tuple = tuple(sorted(list(next_set_list)))
                    
        
                    if next_tuple not in dfa_states:
                        new_name = f"s{state_counter}"
                        dfa_states[next_tuple] = new_name
                        dfa_state_names.append(new_name)
                        unprocessed_states.append(next_tuple)
                        state_counter += 1
                        
        
                    dfa_transitions.append((current_name, symbol, dfa_states[next_tuple]))

        
        dfa_final_states = []
        for state_tuple, name in dfa_states.items():
        
            if any(s in orig_final_states for s in state_tuple):
                dfa_final_states.append(name)


        dfa_transitions.sort(key=lambda x: (int(x[0][1:]), x[1], int(x[2][1:])))
        
        with open(output_file, 'w') as f:

            f.write(" ".join(dfa_state_names) + "\n")
            f.write(" ".join(alphabet) + "\n")
            f.write("s0\n")
            dfa_final_states.sort(key=lambda x: int(x[1:])) 
            f.write(" ".join(dfa_final_states) + "\n")
            for src, sym, dst in dfa_transitions:
                f.write(f"{src} {sym} {dst}\n")