import pandas as pd

from envanalysis import Lexicon

df = pd.read_csv("assets/polish/polish-315LING-p62.csv")
categories = ["Sg.", "Pl."]
segments = ["u", "o"]

transcriptions = df[categories].values.flatten().tolist()

lexicon = Lexicon(transcriptions)
lexicon.generate_all_envs(segments)

lexicon.print_all_envs_and_lexicon_indices(segments)

lexicon.to_csv('assets/polish/polish-quiz3.csv', env="all")