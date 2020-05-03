import csv
# from pprint import pprint


class AscData:
    """
    The class represents a Asc data type for the .asc files.
    """

    topo_file_path = r".\Input Files\topo.asc"  # Topo file relative file path
    topo_file_metadata = {}
    with open(topo_file_path, "r") as file:
        lines = csv.reader(file, delimiter=" ")
        """extract the metadata of the topo file from the first six rows."""
        __file_col_size = tuple(filter(None, next(lines)))
        topo_file_metadata[__file_col_size[0]] = __file_col_size[1]
        __file_row_size = tuple(filter(None, next(lines)))
        topo_file_metadata[__file_row_size[0]] = __file_row_size[1]
        __file_xllcorner_details = tuple(filter(None, next(lines)))
        topo_file_metadata[__file_xllcorner_details[0]] = __file_xllcorner_details[1]
        __file_cell_size_details = tuple(filter(None, next(lines)))
        topo_file_metadata[__file_cell_size_details[0]] = __file_cell_size_details[1]
        __file_yllcorner_details = tuple(filter(None, next(lines)))
        topo_file_metadata[__file_yllcorner_details[0]] = __file_yllcorner_details[1]
        __file_NODATA_value = tuple(filter(None, next(lines)))
        topo_file_metadata[__file_NODATA_value[0]] = __file_NODATA_value[1]

        """Data content of the topo file."""
        topo_data = list(lines)

    def __init__(self, file_path):
        self.file_path = file_path
        self.file_metadata = {}
        self.sensor_data = []
        with open(self.file_path, "r") as file:
            lines = csv.reader(file, delimiter=" ")
            """extract the metadata of the file from the first six rows."""
            __file_col_size = tuple(filter(None, next(lines)))
            self.file_metadata[__file_col_size[0]] = __file_col_size[1]
            __file_row_size = tuple(filter(None, next(lines)))
            self.file_metadata[__file_row_size[0]] = __file_row_size[1]
            __file_xllcorner_details = tuple(filter(None, next(lines)))
            self.file_metadata[__file_xllcorner_details[0]] = __file_xllcorner_details[1]
            __file_cell_size_details = tuple(filter(None, next(lines)))
            self.file_metadata[__file_cell_size_details[0]] = __file_cell_size_details[1]
            __file_yllcorner_details = tuple(filter(None, next(lines)))
            self.file_metadata[__file_yllcorner_details[0]] = __file_yllcorner_details[1]
            __file_NODATA_value = tuple(filter(None, next(lines)))
            self.file_metadata[__file_NODATA_value[0]] = __file_NODATA_value[1]

            """Data content of the file."""
            self.sensor_data = list(lines)

    def adjust_with_topo(self):
        adjusted_data = []
        for i in range(int(self.file_metadata["nrows"])):
            adj_col_vals = []
            for j in range(int(self.file_metadata["ncols"])):
                if self.sensor_data[i][j] == self.file_metadata["NODATA_value"]:
                    adj_col_vals.append(float(self.sensor_data[i][j]) + float(AscData.topo_data[i][j]))
                else:
                    adj_col_vals.append(float(self.sensor_data[i][j]))
            adjusted_data.append(adj_col_vals)
        # topo_adjusted_data = adjusted_data
        return adjusted_data


if __name__ == "__main__":
    ascdata1 = AscData(r"Input Files\wd_day1.asc")
    print(ascdata1.file_metadata)
    print(type(ascdata1.sensor_data[0][0]))
    print(ascdata1.topo_file_metadata)
    # ascdata2 = AscData(r"Input Files\wd_day2.asc")
    # print(id(ascdata1.topo_data) == id(ascdata2.topo_data))
    print(ascdata1.adjust_with_topo())
