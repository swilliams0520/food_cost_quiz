import re
import xlrd

class FoodDataParser:

    @property
    def addendum_regex(self):
        addendum_pattern = r'^([0-9]+)(.+)'
        return re.compile(addendum_pattern)

    def get_valid_cell_rows(self, cell_cursor=3):
        while not self.addendum_regex.match(self.data.cell_value(rowx=cell_cursor, colx=0)):
            if cell_cursor > self.data.nrows: break
            yield (cell_cursor, self.data.cell_value(rowx=cell_cursor, colx=0))
            cell_cursor += 1

    def get_addendum_by_id(self, addendum_id):
        addendum_start = None
        for row, _ in self.get_valid_cell_rows(): addendum_start = row

        addendum = self.addendum_regex
        cell_cursor = addendum_start + 1
        while cell_cursor < self.data.nrows:
            cell_data = self.data.cell_value(rowx=cell_cursor, colx=0)
            match = addendum.match(cell_data)
            if match:
                if int(match.groups()[0]) == addendum_id:
                    return match.groups()[1]

            cell_cursor += 1


    def get_data_columns(self, row):
        row = self.data.row(row)[1:]

        data = dict()
        data['avg_retail_price'] = (row[0].value, row[1].value.strip())
        data['prep_yield_factor'] = row[2].value
        data['size_of_cup_eq'] = (row[3].value, row[4].value)
        data['avg_price_per_cup'] = row[5].value

        return data

    def get_food_variants(self):
        sub_column_name = None
        for row, first_column in self.get_valid_cell_rows():
            cell_pattern = r'([\w ]+)([0-9]+)$'
            column_data = re.compile(cell_pattern).match(first_column.strip())

            if column_data is None and not self.data.cell_value(rowx=row, colx=1) and row > 0:
                sub_column_name = first_column
                continue
            elif column_data is None:
                continue

            column_info = column_data.groups()
            column_data = self.get_data_columns(row)
            column_data['storage_type'] = column_info[0] if not sub_column_name else f'{sub_column_name}: {column_info[0]}'

            addendum_id = int(column_info[1])
            column_data['addendum'] = self.get_addendum_by_id(addendum_id)

            yield column_data

    def get_sources(self):
        for row in self.data.col(0):
            sources = re.compile(r'Source: (.+)').match(row.value)
            if sources:
                return sources.groups()[0]

    def __call__(self, _file):
        file_data = _file.read() if hasattr(_file, 'read') else _file
        self.data = xlrd.open_workbook(file_contents=file_data)
        self.data = self.data.sheet_by_index(0)

        food_data = dict()
        food_data['name'] = self.data.name
        food_data['variants'] = list(self.get_food_variants())
        food_data['sources'] = self.get_sources()

        return food_data
