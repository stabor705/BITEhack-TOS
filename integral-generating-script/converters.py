from random import randint

class ConverterToCsv:
    @staticmethod
    def a_to_csv(difficulty : int, first_id : int):
        n = f'{difficulty}'
        integral_text = []
        integral_indexes = []
        flag = 0
        with open("Lvl" + n + 'A.tex') as file:
            for line in file:
                if flag == 2:
                    if line[0] == '%':
                        replaced_line = line.replace(" ", "")
                        index = int(replaced_line[1:-1])
                        integral_indexes.append(index)
                    else:
                        flag = 1
                        to_insert = line[:-1]
                        integral_text.append(to_insert)
                elif line == '$\n':
                    if flag == 1:
                        flag = 0
                    else:
                        flag = 2
        if len(integral_indexes) == 0:
            integral_indexes = [1 for _ in range(len(integral_text))]
            flag = 0
        else:
            flag = 1
        with open("Lvl" + n + "A.csv", 'w') as file:
            counter = first_id + flag - 1
            for i in range(len(integral_text)):
                if (i > 0 and flag == 1 and integral_indexes[i] <= integral_indexes[i-1]) or flag == 0:
                    counter += 1
                file.write(f"{counter},{integral_text[i]},{integral_indexes[i]},\n")

    @staticmethod
    def q_to_csv(difficulty : int, first_id : int):
        n = f'{difficulty}'
        integral_type = 'Podstawowa'
        integral_text = []
        flag = 0
        with open("Lvl" + n + 'Q.tex') as file:
            for line in file:
                if flag == 2:
                    if line[0] == '%':
                        replaced_line = line.replace(" ", "")
                        replaced_line = replaced_line[1:-1]
                        integral_type = replaced_line
                    elif line != '\n':
                        flag = 1
                        to_insert = line[:-1]
                        integral_text.append(to_insert)
                elif line == '$\n':
                    if flag == 1:
                        flag = 0
                    else:
                        flag = 2
        with open("Lvl" + n + "Q.csv", 'w') as file:
            for i in range(len(integral_text)):
                file.write(f"{i+first_id},{integral_text[i]},{integral_type},{n},\n")
        return first_id + len(integral_text), len(integral_text)

    @staticmethod
    def u_to_csv(difficulty : int, first_id : int, no_integrals : int):
        n = f"{difficulty}"
        integral_text = []
        flag = 0
        with open("Lvl" + n + 'U.tex') as file:
            for line in file:
                if flag == 2:
                    flag = 1
                    to_insert = line[:-1]
                    integral_text.append(to_insert)
                elif line == '$\n':
                    if flag == 1:
                        flag = 0
                    else:
                        flag = 2
                if line[0] == '%':
                    integral_text.append(line)
        if len(integral_text) <= 1:
            ConverterToCsv.generate_u(difficulty, first_id, no_integrals)
            return
        with open("Lvl" + n + "U.csv", 'w') as file:
            k = 1
            for i in range(len(integral_text)):
                if integral_text[i][0] == '%':
                    str_k = integral_text[i][2:]
                    str_k = str_k[:-1]
                    k = int(str_k) - 1 + first_id
                else:
                    file.write(f"{k},{integral_text[i]},\n")

    @staticmethod
    def generate_u(difficulty : int, first_id : int, no_integrals : int):
        integral_index = []
        integral_text = []
        integral_answers = []
        with open(f"Lvl{difficulty}A.csv", "r") as r_file:
            for line in r_file:
                data = line.split(",")
                integral_answers.append((data[0], data[1]))
        for i in range(first_id, first_id + no_integrals):
            indexes_set = set()
            while len(indexes_set) < 5:
                rand_integral_num = randint(0, len(integral_answers)-1)
                while integral_answers[rand_integral_num] == i:
                    rand_integral_num = randint(0, len(integral_answers)-1)
                indexes_set.add(rand_integral_num)
            for j in indexes_set:
                integral_index.append(i)
                integral_text.append(integral_answers[j][1])
        with open(f"Lvl{difficulty}U.csv", 'w') as w_file:
            for i in range(len(integral_index)):
                w_file.write(f"{integral_index[i]},{integral_text[i]},\n")


class ConverterToInserts:
    @staticmethod
    def q_to_inserts(levels_number : int):
        with open("insertsQ.sql", "w") as wFile:
            wFile.write("INSERT INTO integrals (id, integral_string, integral_type, integral_level)\nVALUES\n")
            for i in range(levels_number):
                with open(f"Lvl{i}Q.csv", "r") as rFile:
                    list_of_lines = []
                    for line in rFile:
                        list_of_lines.append(line)
                    be = 0
                    if i == 0:
                        line_parsed = list_of_lines[0].split(",")
                        wFile.write(f"({line_parsed[0]},'{line_parsed[1]}','{line_parsed[2]}',{line_parsed[3]})")
                        be = 1
                    for j in range(be, len(list_of_lines)):
                        line_parsed = list_of_lines[j].split(",")
                        wFile.write(f",\n({line_parsed[0]},'{line_parsed[1]}','{line_parsed[2]}',{line_parsed[3]})")
            wFile.write(";\n")

    @staticmethod
    def a_to_insert(levels_number : int):
        with open("insertsA.sql", "w") as wFile:
            wFile.write("INSERT INTO ans_windows (id, answers, window_number)\nVALUES\n")
            for i in range(levels_number):
                with open(f"Lvl{i}A.csv", "r") as rFile:
                    list_of_lines = []
                    for line in rFile:
                        list_of_lines.append(line)
                    be = 0
                    if i == 0:
                        line_parsed = list_of_lines[0].split(",")
                        wFile.write(f"({line_parsed[0]},'{line_parsed[1]}',{line_parsed[2]})")
                        be = 1
                    for j in range(be, len(list_of_lines)):
                        line_parsed = list_of_lines[j].split(",")
                        wFile.write(f",\n({line_parsed[0]},'{line_parsed[1]}',{line_parsed[2]})")
            wFile.write(";\n")

    @staticmethod
    def u_to_insert(levels_number : int):
        with open("insertsU.sql", "w") as wFile:
            wFile.write("INSERT INTO user_windows (id, proposed_answers)\nVALUES\n")
            for i in range(levels_number):
                with open(f"Lvl{i}U.csv", "r") as rFile:
                    list_of_lines = []
                    for line in rFile:
                        list_of_lines.append(line)
                    be = 0
                    if i == 0:
                        line_parsed = list_of_lines[0].split(",")
                        wFile.write(f"({line_parsed[0]},'{line_parsed[1]}')")
                        be = 1
                    for j in range(be, len(list_of_lines)):
                        line_parsed = list_of_lines[j].split(",")
                        wFile.write(f",\n({line_parsed[0]},'{line_parsed[1]}')")
            wFile.write(";\n")
