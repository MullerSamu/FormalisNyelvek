from project.problem import Problem
import argparse
import re

class RegexProblem(Problem):

    def initialize_parser(self, parser: argparse.ArgumentParser):
        parser.add_argument('--rgx', help='Reguláris kifejezések feladat', type=str)
    
    def is_chosen_problem(self, args):
        return bool(args.rgx)

    def run(self, args):
        input_file = args.input
        output_file = args.output
        task_num = args.rgx
        
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        results = []

        if task_num == '1':
            patterns = [
                # 1. az összes sort, amelyik 10. hónap 15-én jött létre
                re.compile(r"^10-15 "),
                # 2. az összes sort, amelyik 10. hónap 15-én 10 óra 18 perc és 51 másodperckor jött létre
                re.compile(r"^10-15 10:18:51\."),
                # 3. az összes sort, amelyik 51 másodperckor jött létre (mindegy a perc)
                re.compile(r"^[0-9-]+ [0-9]{2}:[0-9]{2}:51\."),
                # 4. az összes lowmemorykiller taget tartalmazó sor
                re.compile(r"^[0-9-]+ [0-9:.]+ +[0-9]+ +[0-9]+ [IDVEFAW] lowmemorykiller *:"),
                # 5. az összes 10:18:51 kor keletkező 221-es process id-jú sort
                re.compile(r"^[0-9-]+ 10:18:51\.[0-9]+ +221 +[0-9]+ "),
                # 6. az összes hibát tartalmazó sort (E)
                re.compile(r"^[0-9-]+ [0-9:.]+ +[0-9]+ +[0-9]+ E "),
                # 7. az összes warningot (W) amit a PackageManager küld
                re.compile(r"^[0-9-]+ [0-9:.]+ +[0-9]+ +[0-9]+ W PackageManager *:"),
                # 8. az összes ExoPlayer-es debug (D) infót
                re.compile(r"^[0-9-]+ [0-9:.]+ +[0-9]+ +[0-9]+ D .*ExoPlayer"),
                # 9. az összes java állomány pozíciót tartalmazó hibát és warningot (EW .java:)
                re.compile(r"^[0-9-]+ [0-9:.]+ +[0-9]+ +[0-9]+ [EW] .*\.java:"),
                # 10. az összes olyan sort, ami tartalmazza a Thread szót a message részben (nem a tagben) -> tag: message
                re.compile(r"^[0-9-]+ [0-9:.]+ +[0-9]+ +[0-9]+ [IDVEFAW] .+?: .*Thread")
            ]
            results = [
                str(sum(1 for line in lines if p.search(line)))
                for p in patterns
            ]

        # --- INNENTŐL LENT MINDEN TÖKÉLETES, NEM NYÚLUNK HOZZÁ ---

        elif task_num == '2':
            p = re.compile(r"^[0-9-]+ [0-9:.]+ +\d+ +\d+ +E +[^:]+: .*?([a-zA-Z0-9_$]+\.java):")
            for line in lines:
                m = p.search(line)
                if m:
                    results.append(m.group(1))

        elif task_num == '3':
            p = re.compile(r"^[0-9-]+ [0-9:.]+ +(\d+) +")
            seen = set()
            for line in lines:
                m = p.search(line)
                if m:
                    pid = m.group(1)
                    if pid not in seen:
                        seen.add(pid)
                        results.append(pid)

        elif task_num == '4':
            p = re.compile(r"^[0-9-]+ [0-9:.]+ +(\d+) +\d+ +E ")
            err_counts = {}
            for line in lines:
                m = p.search(line)
                if m:
                    pid = m.group(1)
                    err_counts[pid] = err_counts.get(pid, 0) + 1
            if err_counts:
                max_pid = max(err_counts, key=err_counts.get)
                results.append(f"PID={max_pid} ({err_counts[max_pid]} errors)")

        elif task_num == '5':
            p = re.compile(r"^[0-9-]+ [0-9:.]+ +(\d+) +\1 +E ")
            count = 0
            for line in lines:
                if p.search(line):
                    count += 1
            results.append(str(count))

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(results) + '\n')