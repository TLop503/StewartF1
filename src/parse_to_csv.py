def preprocess(list):
    return 0

def parse_to_csv(list):
    out = ""
    for res in list:
        # print(res.name)
        # print(res.position)
        # print(res.laps)
        # print(res.points)
        out = out + f"{res.position},{res.laps},{res.points},"
    
    return(out)

def postprocess(list):
    return 0