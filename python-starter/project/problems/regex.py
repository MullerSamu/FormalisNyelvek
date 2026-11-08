from project.problem import Problem
import argparse

class RegexProblem(Problem):

    def initialize_parser(self, parser: argparse.ArgumentParser):
        """
        Kezeli a 4. feladathoz (Regex) tartozó parancssori argumentumot.
        """
        # A log alapján a tesztelő számokat ad át (pl. --rgx 1), ezért type=str
        parser.add_argument('--rgx', help='Reguláris kifejezések feladat', type=str)
    
    def is_chosen_problem(self, args):
        return bool(args.rgx)

    def run(self, args):
        """
        Ide kerül majd a 4. házi logikája. Egyelőre üresen hagyjuk.
        """
        pass