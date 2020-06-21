
def negate_verb(verb):
    if verb[len(verb)-1] == "s" and len(verb) > 2:
        return "does not {}".format(verb[:len(verb)-1])
    else:
        return "{} not".format(verb)
