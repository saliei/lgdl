color = {
        'purple'   : '\x1b[95m',
        'cyan'     : '\x1b[96m',
        'darkcyan' : '\x1b[36m',
        'blue'     : '\x1b[94m',
        'green'    : '\x1b[92m',
        'yellow'   : '\x1b[93m',
        'red'      : '\x1b[91m',
        'bold'     : '\x1b[1m',
        'underline': '\x1b[4m',
        'end'      : '\x1b[0m'
        }

def pretty_print(result, index):
    _id = index + 1
    print("\nID: {}\n{}".format(_id, "----" + '-'*len(str(_id))))
    print("      Title: {}".format(color["bold"] + result["title"]  + color["end"]))
    print("     Author: {}".format(color["bold"] + result["author"] + color["end"]))
    print("       Year: {}".format(result["year"]))
    print("  Publisher: {}".format(result["publisher"]))
    print("     Format: {}".format(result["extension"]))
