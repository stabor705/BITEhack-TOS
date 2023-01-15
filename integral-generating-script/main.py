from converters import ConverterToCsv
from converters import ConverterToInserts

if __name__ == '__main__':
    max_lvl = 2
    first_id = 0
    for i in range(max_lvl + 1):
        next_first_id, noIntegrals = ConverterToCsv.q_to_csv(i, first_id)
        ConverterToCsv.a_to_csv(i, first_id)
        ConverterToCsv.u_to_csv(i, first_id, noIntegrals)
        first_id = next_first_id
    ConverterToInserts.q_to_inserts(max_lvl+1)
    ConverterToInserts.a_to_insert(max_lvl+1)
    ConverterToInserts.u_to_insert(max_lvl+1)
