
import json


def load_strings(path):
    fileref = open(path, "r")
    rtn = fileref.readlines()
    fileref.close()
    return rtn


def load_preferences(path):
    text = load_strings(path)
    width = 800
    height = 400
    decorated = True
    for line in text:
        value = line.split("=")
        if(len(value) < 2):
            continue
        key = value[0]
        value = value[1].rstrip()

        if key == "width":
            width = int(value)
        if key == "height":
            height = int(value)
        if key == "decorated":
            if value.lower() == "false":
                decorated = False
            else:
                decorated = True

    print("Loaded config. Width="+str(width)+"  Height="+str(height)+"  Decorated="+str(decorated))
    return (width, height, decorated)


class Handle(object):
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=0)