# utils/csv_reader.py

import csv


class CSVReader:

    @staticmethod
    def read_csv(file_path):

        data = []

        with open(file_path, mode='r', encoding='utf-8') as file:

            csv_data = csv.DictReader(file)

            for row in csv_data:
                data.append(row)

        return data