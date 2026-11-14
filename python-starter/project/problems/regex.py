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
            counts = [0] * 10
            for line in lines:
                # 1. 10. hónap 15-én jött létre
                if re.search(r"^10-15\b", line): counts[0] += 1
                # 2. 10-15 10:18:51 (milliszekundumok nélkül is működik)
                if re.search(r"^10-15 10:18:51\b", line): counts[1] += 1
                # 3. 51 másodperckor (milliszekundumok nélkül is működik)
                if re.search(r"^[0-9-]+ \d{2}:\d{2}:51\b", line): counts[2] += 1
                # 4. lowmemorykiller taget tartalmazó sor (kezeli, ha van előtte/utána más is a tagben)
                if re.search(r"^[0-9-]+ [0-9:.]+ +\d+ +\d+ +[IDVEFAW] +[^:]*lowmemorykiller[^:]*:", line): counts[3] += 1
                # 5. 10:18:51-kor, 221-es PID (pontosan a PID-t nézi)
                if re.search(r"^[0-9-]+ 10:18:51\b[^\s]* +221\b", line): counts[4] += 1
                # 6. Hibát (E) tartalmazó sor
                if re.search(r"^[0-9-]+ [0-9:.]+ +\d+ +\d+ +E ", line): counts[5] += 1
                # 7. Warning (W) a PackageManager-től
                if re.search(r"^[0-9-]+ [0-9:.]+ +\d+ +\d+ +W +[^:]*PackageManager[^:]*:", line): counts[6] += 1
                # 8. ExoPlayer debug (D)
                if re.search(r"^[0-9-]+ [0-9:.]+ +\d+ +\d+ +D +[^:]*ExoPlayer[^:]*:", line): counts[7] += 1
                # 9. E vagy W, tartalmazza a .java:-t
                if re.search(r"^[0-9-]+ [0-9:.]+ +\d+ +\d+ +[EW] +.*\.java:", line): counts[8] += 1
                # 10. Thread szó a message részben
                if re.search(r"^[0-9-]+ [0-9:.]+ +\d+ +\d+ +[IDVEFAW] +[^:]+: .*Thread", line): counts[9] += 1
                
            results = [str(c) for c in counts]

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