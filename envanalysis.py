from collections import OrderedDict

class Lexicon:
    def __init__(self, transcriptions: list) -> None:
        self.transcriptions = transcriptions  # an ORDERED list
        self.segments = dict() # {key: "a", value: Segment(a)}

    # With the internal lexicon, generate the immediate phonological environments of the given segment.
    # This can be accessed with self.segments[segment] 
    def generate_immediate_envs(self, segments: list) -> None:
        for s in segments:
            if s not in self.segments.keys():
                self.segments[s] = Segment(s)
            for index, t in enumerate(self.transcriptions):
                self.segments[s].generate_immediate_envs(t, index)

    # With the internal lexicon, generate the long-distance phonological environments of the given segment.
    # This can be accessed with self.segments[segment] 
    def generate_long_distance_envs(self, segments: list) -> None:
        for s in segments:
            if s not in self.segments.keys():
                self.segments[s] = Segment(s)
            for index, t in enumerate(self.transcriptions):
                self.segments[s].generate_long_distance_envs(t, index)
    
    def generate_all_envs(self, segments: list) -> None:
        self.generate_long_distance_envs(segments)
        self.generate_immediate_envs(segments)

    # Prints the immediate phonological environments for the given segments
    def print_immediate_envs_and_lexicon_indices(self, segments: list) -> None:
        for s in segments:
            self.segments[s].print_immediate_envs_and_lexicon_indices()

    # Prints the immediate phonological environments for the given segments
    def print_long_distance_envs_and_lexicon_indices(self, segments: list) -> None:
        for s in segments:
            self.segments[s].print_long_distance_envs_and_lexicon_indices()
    
    def print_all_envs_and_lexicon_indices(self, segments: list) -> None:
        self.print_immediate_envs_and_lexicon_indices(segments)
        self.print_long_distance_envs_and_lexicon_indices(segments)
        
    def to_csv(self, fname, env="immediate"):
        from pandas import DataFrame

        if env == "immediate" or env == "all":
            # make dict
            data = dict()
            for seg, envs in self.segments.items():
                data["[" + seg + "]"] = [env for env in envs.immediate_environments.environments.keys()]
            
            # make columns even by filling with placeholders
            max_len = max(len(v) for v in data.values())
            for key, values in data.items():
                if len(values) < max_len:
                    data[key] = values + ['NA'] * (max_len - len(values))

            df = DataFrame(data)

            if fname.endswith(".csv"):
                fname = fname[:-4]
            df.to_csv(fname + "__immediate-envs.csv", index=False)

        if env == "long distance" or env == "all":
            # make dict
            data = dict()
            for seg, envs in self.segments.items():
                data["[" + seg + "]"] = [env for env in envs.long_distance_environments.environments.keys()]
            
            # make columns even by filling with placeholders
            max_len = max(len(v) for v in data.values())
            for key, values in data.items():
                if len(values) < max_len:
                    data[key] = values + ['NA'] * (max_len - len(values))

            df = DataFrame(data)
            if fname.endswith(".csv"):
                fname = fname[:-4]
            df.to_csv(fname + "__long-distance-envs.csv", index=False)



# A class that keeps track of an environment's index in the lexicon's transcriptions
class Environment:
    def __init__(self, env) -> None:
        self.env = env
        self.indices = list()

    def __str__(self) -> str:
        return f"[{self.env}] @ {self.indices}"
    
    # Keeps track of indices where the environment occurs
    def add_index(self, index) -> None:
        self.indices.append(index)
    
# A class for collecting environments for ONE segment
class Environment_Collection:
    def __init__(self, segment) -> None:
        self.segment = segment
        self.environments = dict() # {"#_#": Environment() var to store indices}

    def __str__(self):
        rstring = ""
        for e in self.environments.values():
            rstring += f"\n{e.__str__()}"
        return rstring + "\n"

    # If the environment hasn't been seen before, track it.
    # Either way, track the index of the transcription it belongs to.
    def add(self, env: str, index: int) -> None:
        if env not in self.environments.keys():
            self.environments[env] = Environment(env)
        self.environments[env].add_index(index)

# A class that keeps track of all of a segment's info in the lexicon.
class Segment:
    def __init__(self, underlying_form) -> None:
        self.immediate_environments = Environment_Collection(underlying_form)
        self.long_distance_environments = Environment_Collection(underlying_form)
        self.underlying_form = underlying_form
        self.surface_form = "TBD"

    # Uses Environment_Collection.__str__()
    def print_immediate_envs_and_lexicon_indices(self):
        print( f"Immediate environments for {self.underlying_form}: {self.immediate_environments.__str__()}" )

    # Uses Environment_Collection.__str__()
    def print_long_distance_envs_and_lexicon_indices(self):
        print( f"Long-distance environments for {self.underlying_form}: {self.long_distance_environments.__str__()}" )

    # Uses Environment_Collection.__str__()
    def print_all_envs_and_lexicon_indices(self):
        self.print_immediate_envs_and_lexicon_indices()
        self.print_long_distance_envs_and_lexicon_indices()

    # Takes the underlying form/transcription of a word in the lexicon.
    # Returns the immediate phonological environments (there may be more than one).
    def generate_immediate_envs(self, transcription: str, index: int) -> None:
        for i in range(len(transcription)):
            if transcription[i] == self.underlying_form:
                # Preceding env
                env = ""
                env += ("#" if i == 0 else transcription[i - 1])
                env += "_"
                env += ("#" if i == len(transcription) - 1 else transcription[i + 1])
                self.immediate_environments.add(env, index)

    # Takes the underlying form/transcription of a word in the lexicon.
    # Returns the immediate phonological environments (there may be more than one).
    def generate_long_distance_envs(self, transcription: str, index: int) -> None:
        for i in range(len(transcription)):
            if transcription[i] == self.underlying_form:
                env = ""
                env += ("#" if i in [0, 1] else transcription[i - 2])
                env += ("#" if i in [0] else "*")
                env += "_"
                end_index = len(transcription) - 1
                env += ("#" if i in [end_index] else "*")
                env += ("#" if i in [end_index, end_index - 1] else transcription[end_index])
                self.long_distance_environments.add(env, index)

    def generate_all_envs(self, transcriptions) -> None:
        for index, t in enumerate(transcriptions):
            self.generate_immediate_envs(t)
            self.generate_long_distance_phonological_environments(t)

    