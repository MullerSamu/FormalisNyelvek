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

        #Megnyitja a bemeneti fájlt, beolvassa a sorokat, levágja a felesleges szóközöket/sortöréseket és kihagyja az üres sorokat.
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        orig_states = lines[0].split() # elso sorbol az eredeti allapotok listaja
        alphabet = lines[1].split() #masodik sorbol az abc betui
        start_state = lines[2] #kezdoallapot
        orig_final_states = set(lines[3].split()) #kinyeri a vegallapotokat es egy halmazba teszi oket gyors kereses miatt
        
        
        nfa_transitions = {} #ures halmaz mert egy nemdeterminisztikus automatában (NFA) egy állapotból ugyanazzal a betűvel több különböző állapotba is eljuthatunk
        for state in orig_states:
            for symbol in alphabet:
                nfa_transitions[(state, symbol)] = set()

        for line in lines[4:]:
            parts = line.split()
            if len(parts) == 3:
                curr_st, symbol, next_st = parts
                
                #ellenorizzuk hogy az el kiindoplo allapota es a celallapot benne van e az első sorban felsorolt állapotok között, illetve az él címkéje (symbol) benne van-e az ábécében
                #ha nem hiba es kilep
                if curr_st not in orig_states or next_st not in orig_states or symbol not in alphabet:
                    print(f"Hiba: Érvénytelen állapot vagy szimbólum az átmenetben: {line}")
                    return
                
                nfa_transitions[(curr_st, symbol)].add(next_st)#Hozzáadja a célállapotot az adott (állapot, betű) párhoz tartozó halmazhoz.

        
        
        dfa_states = {} #Szótár, ami összeköti az eredeti állapotok csoportját az új névvel
        dfa_state_names = [] #Lista, amiben sorrendben gyűjtjük az új neveket
        dfa_transitions = [] #Lista az új DFA éleknek
        unprocessed_states = []#Egy várakozási sor (Queue). Ide tesszük be azokat az újonnan felfedezett állapot-csoportokat, amiket még nem vizsgáltunk meg, hogy hova vezetnek belőlük élek.

        
        start_set = tuple([start_state]) #kezdoallapotbol csinalunk egy 1 elemu tupplet.
        dfa_states[start_set] = "s0"
        dfa_state_names.append("s0")
        unprocessed_states.append(start_set) #innen indul a felfedezes
        
        state_counter = 1

        #addig fut ameddig van olyan allpot csoport amit nem vizsgaltunk
        while unprocessed_states:
            #kiveszi a sor legelso element es uj nevet ker
            current_set = unprocessed_states.pop(0)
            current_name = dfa_states[current_set]
            
        #megnezzuk hogy hova tudunk lepni a csoportbol 
            for symbol in alphabet:
                next_set_list = set()
                #osszers aktualis csoport eredeti allapotan megyunk vegig
                for state in current_set:
        
                    if (state, symbol) in nfa_transitions:
                        next_set_list.update(nfa_transitions[(state, symbol)])
                
                #csak akkor csinálunk új élt, ha a halmaz nem üres
                if next_set_list:
                    #rendezett tuple a;lakitjuk a halmazt
                    next_tuple = tuple(sorted(list(next_set_list)))
                    
                    #Megnézzük, láttuk-e már ezt az állapot-kombinációt korábban. Ha még nem, akkor adunk neki egy új nevet
                    if next_tuple not in dfa_states:
                        new_name = f"s{state_counter}"
                        dfa_states[next_tuple] = new_name
                        dfa_state_names.append(new_name)
                        unprocessed_states.append(next_tuple)
                        state_counter += 1
                        
                    #feljegyezzuk az uj elt
                    dfa_transitions.append((current_name, symbol, dfa_states[next_tuple]))


        #Új végállapotok meghatározása
        dfa_final_states = []
        for state_tuple, name in dfa_states.items():
        #A szabály szerint egy új s állapot akkor lesz végállapot a determinizált automatában, ha az őt alkotó eredeti q állapotok között van legalább egy (any) olyan állapot, ami eredetileg is végállapot volt (orig_final_states). Ha igen, hozzáadjuk a dfa_final_states listához.
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