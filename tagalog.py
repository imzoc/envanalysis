import pandas as pd

from envanalysis import Lexicon

df = pd.read_csv("assets/tagalog/tagalog-315LING-p61.csv")
categories = ["Root", "Root + in", "Root + an"]
segments = ["u", "o", "m", "n", "ŋ"]

transcriptions = df[categories].values.flatten().tolist()

lexicon = Lexicon(transcriptions)
lexicon.generate_all_envs(segments)

lexicon.print_all_envs_and_lexicon_indices(segments)

lexicon.to_csv('assets/tagalog/tagalog.csv', env="all")