from project.problem import Problem
import argparse
import re

class RegexProblem(Problem):

    def initialize_parser(self, parser: argparse.ArgumentParser):
        """
        Kezeli a 4. feladathoz (Regex) tartozó parancssori argumentumot.
        """
        parser.add_argument('--rgx', help='Reguláris kifejezések feladat', type=str)
    
    def is_chosen_problem(self, args):
        """
        Ellenőrzi, hogy a --rgx flag jelen van-e.
        """
        return bool(args.rgx)

    def run(self, args):
        """
        Lefuttatja a reguláris kifejezések szerinti kereséseket a logfájlban.
        """
        input_file = args.input
        output_file = args.output
        task_num = args.rgx
        
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        results = []

        if task_num == '1':
            counts = [0] * 10
            # 1. 10. hónap 15-én létrejött sorok
            p1 = re.compile(r"^10-15\b")
            # 2. 10. hónap 15-én 10:18:51-kor létrejött sorok
            p2 = re.compile(r"^10-15 10:18:51\.")
            # 3. 51 másodperckor létrejött sorok
            p3 = re.compile(r"^[0-9-]+ \d{2}:\d{2}:51\.")
            # 4. lowmemorykiller taget tartalmazó sorok
            p4 = re.compile(r"^[0-9-]+ [0-9:.]+ +\d+ +\d+ +[A-Z] +lowmemorykiller *:")
            # 5. 10:18:51-kor keletkező 221-es PID
            p5 = re.compile(r"^[0-9-]+ 10:18:51\.\d+ +221 +")
            # 6. Hibát (E) tartalmazó sorok
            p6 = re.compile(r"^[0-9-]+ [0-9:.]+ +\d+ +\d+ +E ")
            # 7. Warningot (W) tartalmazó PackageManager sorok
            p7 = re.compile(r"^[0-9-]+ [0-9:.]+ +\d+ +\d+ +W +PackageManager *:")
            # 8. ExoPlayer-es debug (D) infó
            p8 = re.compile(r"^[0-9-]+ [0-9:.]+ +\d+ +\d+ +D +.*?ExoPlayer.*?:")
            # 9. Java állomány pozícióját tartalmazó hiba (E) vagy warning (W)
            p9 = re.compile(r"^[0-9-]+ [0-9:.]+ +\d+ +\d+ +[EW] +.*?[a-zA-Z0-9_$]+\.java:")
            # 10. A Thread szó a message részben (nem a tagben)
            p10 = re.compile(r"^[0-9-]+ [0-9:.]+ +\d+ +\d+ +[A-Z] +[^:]+: .*Thread")

            for line in lines:
                if p1.search(line): counts[0] += 1
                if p2.search(line): counts[1] += 1
                if p3.search(line): counts[2] += 1
                if p4.search(line): counts[3] += 1
                if p5.search(line): counts[4] += 1
                if p6.search(line): counts[5] += 1
                if p7.search(line): counts[6] += 1
                if p8.search(line): counts[7] += 1
                if p9.search(line): counts[8] += 1
                if p10.search(line): counts[9] += 1
                
            results = [str(c) for c in counts]

        elif task_num == '2':
            # Összes hiba (E) származási helye (stack trace fájlnév)
            p = re.compile(r"^[0-9-]+ [0-9:.]+ +\d+ +\d+ +E +[^:]+: .*?([a-zA-Z0-9_$]+\.java):")
            for line in lines:
                m = p.search(line)
                if m:
                    results.append(m.group(1))

        elif task_num == '3':
            # Különböző PID-k az előfordulás sorrendjében
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
            # Legtöbb errort tartalmazó processz formázva
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
            # Fő szálon történt hibák (amikor a PID és TID megegyezik)
            # A \1 regex visszahivatkozás (backreference) ellenőrzi, hogy a TID megegyezik-e az első zárójelben lévő PID-val.
            p = re.compile(r"^[0-9-]+ [0-9:.]+ +(\d+) +\1 +E ")
            count = 0
            for line in lines:
                if p.search(line):
                    count += 1
            results.append(str(count))

        # Kimenet fájlba írása új sorokkal elválasztva
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(results) + '\n')