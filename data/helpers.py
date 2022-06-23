import csv


def get_symbol_list(path_to_csv: str):
    symbol_list = []
    with open(path_to_csv) as f:
        for line in f:
            if "," not in line:
                continue
            symbol = line.split(",")[0]
            symbol_list.append(symbol)
    return symbol_list