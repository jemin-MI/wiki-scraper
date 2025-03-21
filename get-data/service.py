import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from fastapi.responses import FileResponse


def get_data(domain, is_sheet):
    domain_list = domain.split(',')

    company_data = {}
    for domain in domain_list:
        if domain.strip() != '':
            url = f'https://en.wikipedia.org/wiki/{domain}'
            response = requests.get(url)

            if response.status_code != 200:
                company_data[domain] = {"error": f"Failed to fetch data. Status code: {response.status_code}"}

            soup = BeautifulSoup(response.content, 'html.parser')
            table_body = soup.tbody
            data_dict = {}

            if table_body:  # Ensure table_body exists
                for data in table_body.find_all('tr'):
                    if data.th:
                        heading = data.th.text.strip()
                        if data.td:
                            if data.find_all('li'):
                                data_list = [i.text.strip() for i in data.find_all('li')]
                            else:
                                data_list = data.td.text.strip()
                            data_dict[heading] = data_list
                        data_dict['Domain'] = domain

                if data_dict:
                    company_data[domain] = {
                        "status_code": 200,
                        "data": data_dict
                    }
                else:
                    company_data[domain] = {
                        "status_code": 204,  # No Content
                        "error": "No relevant data found in the table."
                    }
            else:
                company_data[domain] = {
                    "status_code": 204,  # No Content
                    "error": "No table data found on the page."
                }

    if is_sheet:

        wb = Workbook()
        sheet = wb.active
        sheet.title = "Company Data"
        columns_list = []

        for company, details in company_data.items():
            if company_data[company]['status_code'] == 200:
                columns_list.extend(company_data[company]['data'].keys())

        columns_list = list(set(columns_list))
        columns_list.insert(0, 'Domain')
        sheet.append(columns_list)

        for company, details in company_data.items():
            if company_data[company]['status_code'] == 200:
                value_list = []
                for column in columns_list:
                    value = company_data.get(company, {}).get('data', {}).get(column, '')
                    if isinstance(value, list):
                        value = ', '.join(value)
                    value_list.append(value)
                sheet.append(value_list)

        file_path = "CompanyDataSimplified.xlsx"
        wb.save(file_path)
        return FileResponse(
            file_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename="CompanyDataSimplified.xlsx"
        )
    return {"your_data": company_data}
