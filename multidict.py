import simplejson as json
from collections import defaultdict

def multidict(ordered_pairs):
    """Convert duplicate keys values to lists."""
    # read all values into lists
    d = defaultdict(list)
    for k, v in ordered_pairs:
        d[k].append(v)

    # unpack lists that have only 1 item
    for k, v in d.items():
        if len(v) == 1:
            d[k] = v[0]
    return dict(d)

text = """{ "type": "Person","subType": "Athlete","subType": "AwardWinner"}"""

print json.JSONDecoder(object_pairs_hook=multidict).decode(text)
