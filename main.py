from datetime import datetime
import pandas as pd
import numpy as np


class Generator:
    def __init__(self,
                 rows: int,
                 example_file: str,
                 start_date: datetime = datetime(2023, 8, 1),
                 end_date: datetime = datetime(2025, 5, 1)
                 ):
        """
        Generator for ILMT values returning DataFrame object upon calling generate() method

        :param rows: number of rows to be generated
        :type rows: int
        :param example_file: file that will work as an example(path to the file)
        :type example_file: str
        :param start_date: start date of our generation
        :type start_date: datetime
        :param end_date: end date of our generation
        :type end_date: datetime
        """
        self.rows = rows
        self.example_data = pd.read_csv(example_file)
        self.start_date = start_date
        self.end_date = end_date

    def _generate_endpoints(self) -> dict:
        """
        Generates columns with endpoints values

        :return: dictionary with values of endpoints
        :rtype: dict
        """

        endpoints = {}

        for endpoint in self.example_data.columns[self.example_data.columns.str.contains("endpoints_os_")]:
            endpoints[endpoint] = np.random.randint(self.example_data[endpoint].max(), size=self.rows)

        endpoints["endpoints_all"] = np.zeros(self.rows)

        for endpoints_count in endpoints.values():
            endpoints["endpoints_all"] += endpoints_count

        left_columns = ["endpoints_on_cloud",
                        "endpoints_disconnected",
                        "endpoints_managed_by_vm_manager",
                        "endpoints_deleted",
                        "endpoints_custom_pvu_rate",
                        "endpoints_disconnected_deleted"
                        ]

        for endpoint in left_columns:
            endpoints[endpoint] = np.random.randint(self.example_data[endpoint].max(), size=self.rows)

        return endpoints

    def _generate_instances(self) -> dict:
        """
        Generates columns with instances values

        :return: dictionary with instances
        :rtype: dict
        """
        instances = {}
        for instance in self.example_data.columns[self.example_data.columns.str.contains("instances")]:
            instances[instance] = np.random.randint(self.example_data[instance].max(), size=self.rows)
        return instances

    def _generate_other(self) -> dict:
        """
        Generates columns not falling into main categories

        :return: dictionary with values of other categories
        :rtype: dict
        """
        other_columns = {}
        # selects columns that have not been yet used
        columns = self.example_data.columns
        columns = columns[~columns.str.contains("endpoints")]
        columns = columns[~columns.str.contains("instances")]

        # columns which will be omitted
        to_be_omitted = [
            "data_collection_time",
            "lmt_server_install_time",
            "lmt_database_type",
            "lmt_database_version",
            "lmt_server_version",
            "last_import_status",
            "lmt_scanner_version_oldest"
        ]
        # checks whether a column should be omitted or not
        for column in (omitted for omitted in columns if omitted not in to_be_omitted):
            other_columns[column] = np.random.randint(self.example_data[column].max(), size=self.rows)

        other_columns["lmt_database_type"] = np.random.choice(
            self.example_data["lmt_database_type"].unique(),
            size=self.rows
        )
        other_columns["lmt_database_version"] = np.random.choice(
            self.example_data["lmt_database_version"].unique(),
            size=self.rows
        )
        other_columns["lmt_server_version"] = np.random.choice(
            self.example_data["lmt_server_version"].unique(),
            size=self.rows
        )
        other_columns["last_import_status"] = np.random.choice(
            self.example_data["last_import_status"].unique(),
            size=self.rows
        )

        other_columns["lmt_scanner_version_oldest"] = np.random.choice(
            self.example_data["lmt_scanner_version_oldest"].unique(),
            size=self.rows
        )

        return other_columns

    def _generate_date(self) -> dict:
        """
        Generates a dictionary of date related columns

        :return: dictionary of date related values
        :rtype: dict
        """
        date_columns = {
            "data_collection_time": pd.date_range(self.start_date, self.end_date, periods=self.rows),
            "lmt_server_install_time": pd.date_range(self.start_date, self.end_date, periods=self.rows)
        }

        return date_columns

    def generate(self) -> pd.DataFrame:
        """
        Generates Dataframe using all other methods

        :return: Dataframe made of all columns
        :rtype: pd.DataFrame
        """
        data_connected = {
            **self._generate_date(),
            **self._generate_endpoints(),
            **self._generate_instances(),
            **self._generate_other()
        }
        return pd.DataFrame(data_connected)


if __name__ == '__main__':
    gen = Generator(1000, "history.csv")
    print(gen.generate())
