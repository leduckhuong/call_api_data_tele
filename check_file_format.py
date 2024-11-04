def check_file_format(path):
    with open(path) as file:
        separate_line,separate_line2 = 0,0
        for line in file:
            if line.strip() == "":
                separate_line = separate_line + 1
            if line.strip() == "===============":
                separate_line2 = separate_line2 + 1
            if separate_line == 4:
                return 2
            if separate_line2 == 4:
                return 3
        return 1 