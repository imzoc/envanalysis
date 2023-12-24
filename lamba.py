import pandas as pd

from envanalysis import Lexicon

df = pd.read_csv("assets/lamba/lamba-315LING-p73.csv")
categories = ["Past", "Passive", "Neuter", "Applied", "Reciprocal"]
segments = ["i", "e", "n", 'l', 's', 'ʃ', 'k', 'c']

transcriptions = df[categories].values.flatten().tolist()

lexicon = Lexicon(transcriptions)
lexicon.generate_all_envs(segments)

lexicon.print_all_envs_and_lexicon_indices(segments)
lexicon.to_csv('assets/lamba/lamba-test.csv', env="all")