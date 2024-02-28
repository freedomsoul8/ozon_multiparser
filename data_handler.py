import pandas as pd

class data_handler:

    container = []
    breadcrumbs = []


    def read_input_column(self,filename,column_name):
        df = pd.read_excel(filename)
        result = df[f"{column_name}"].tolist()
        return result

    def create_columns(self,input_data):
        columns = ["Название", "Категория"]
        columns.extend(input_data)
        return columns

    def export_data(self,container,columns,filename):
        df = pd.DataFrame(columns=columns)
        print(columns)
        print(len(columns))
        for row in container:
            print(row)
            print(row[:4] + row[5])
            print(len(row[:4] + row[5]))
            df.loc[-1] = row[:4] + row[5]

        df.to_excel(filename)

    def export_urls(self,filename, urls):
        df = pd.DataFrame({"url": urls})
        df.to_excel(filename)

    def sort_data(self, input_data):
        categories = {}
        for item in input_data:
            title, breadcrumb, price, imgs, chars_title, chars_data = item
            if breadcrumb in categories:
                categories[breadcrumb].append([title, breadcrumb, price, imgs, chars_title, chars_data])
            else:
                categories[breadcrumb] = [[title, breadcrumb, price, imgs, chars_title, chars_data]]
        return categories

    def create_excel_table(self,data):
        categories = {}
        for item in data:
            name, category, code, imgs, characteristics_names, characteristics_values = item
            if category not in categories:
                categories[category] = []
            category_data = {"Название": name, "Код": code, "Картинки": imgs}
            for i in range(len(characteristics_names)):
                if i < len(characteristics_values):
                    category_data[characteristics_names[i]] = characteristics_values[i]
                else:
                    category_data[characteristics_names[i]] = ''
            categories[category].append(category_data)
        for category, items in categories.items():
            df = pd.DataFrame(items)
            df.to_excel(f'{category}_table.xlsx', index=False)

    def new_breadcrumbs(self,breadcrumbs_list):
        df = pd.DataFrame({"Категории":breadcrumbs_list})
        df.to_excel("Категории.xlsx",index=False)

data_handler = data_handler()

