
import csv


class CSVReader:

    @staticmethod
    def read_csv(file_path):

        data = []

        try:

            with open(file_path, mode='r') as file:

                csv_data = csv.reader(file)

                for row in csv_data:
                    data.append(row)

            return data

        except Exception as e:

            print("Error reading CSV file:", e)

            return []