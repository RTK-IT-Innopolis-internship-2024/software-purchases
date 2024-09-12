from datetime import UTC, date, datetime
from pathlib import Path

from openpyxl import load_workbook

from src.backend.objects.company import Company
from src.backend.objects.country import Country
from src.backend.objects.license_type import LicenseType
from src.backend.objects.order import Order
from src.backend.objects.order_template import OrderTemplate
from src.backend.objects.software import Software
from src.backend.objects.software_class import SoftwareClass
from src.backend.objects.supervisor import Supervisor
from src.utils.config import AppConfig


def get_main_order_template() -> OrderTemplate:  # TODO: implement compare and edit events by some changes from xlsx file
    main_order_template_path = Path(AppConfig.get_order_path("orders/main_template"))

    order_templates_paths = [str(file) for file in main_order_template_path.glob("*.xlsx")]

    if not order_templates_paths:
        error_message = "No main order template file found in the specified directory."
        raise FileNotFoundError(error_message)

    if len(order_templates_paths) != 1:
        error_message = f"Expected exactly one main order template file, found {len(order_templates_paths)}."
        raise ValueError(error_message)

    order_template_file_path = order_templates_paths[0]

    return get_order_template(order_template_file_path)


def parse_quarter(quarter: str) -> int:
    if quarter == "1 квартал":
        return 1
    if quarter == "2 квартал":
        return 2
    if quarter == "3 квартал":
        return 3
    if quarter == "4 квартал":
        return 4
    error_message = f"Invalid quarter: {quarter}"
    raise ValueError(error_message)


def get_order_template(order_template_file_path: str) -> OrderTemplate:
    order_template_workbook = load_workbook(filename=order_template_file_path, data_only=True)
    sheets_data = {}
    sheets_titles = []
    for sheet in order_template_workbook.worksheets:
        sheet_data = [list(row) for row in sheet.iter_rows(values_only=True)]
        sheets_titles.append(sheet.title)
        sheets_data[sheet.title] = sheet_data
    check_mandatory_sheets(sheets_titles)
    countries = []
    for row in sheets_data["Страны"][1:]:
        if row[0] is not None:
            country_name = str(row[0])
            countries.append(Country(name=country_name))
    if len(countries) == 0:
        error_message = "No valid country data found in the 'Страны' sheet."
        raise ValueError(error_message)
    companies = []
    companies_map = {}
    for row in sheets_data["Наименование проекта"][1:]:
        if row[0] is not None:
            company_name = str(row[0])
            company = Company(name=company_name)
            companies.append(company)
            companies_map[company_name] = company
    if len(companies) == 0:
        error_message = "No valid company data found in the 'Наименование проекта' sheet."
        raise ValueError(error_message)
    supervisors = []
    supervisors_map = {}
    for row in sheets_data["ФИО Руководителя"][1:]:
        if row[0] is not None:
            supervisor_name = str(row[0])
            supervisor_email = str(row[1]) if row[1] is not None else None
            supervisor = Supervisor(name=supervisor_name, email=supervisor_email)
            supervisors.append(supervisor)
            supervisors_map[supervisor_name] = supervisor
    if len(supervisors) == 0:
        error_message = "No valid supervisor data found in the 'ФИО Руководителя' sheet."
        raise ValueError(error_message)
    licenses_types = []
    licenses_types_map = {}
    for row in sheets_data["тип лицензии"][1:]:
        if row[0] is not None:
            license_type_name = str(row[0])
            license_type = LicenseType(name=license_type_name)
            licenses_types.append(license_type)
            licenses_types_map[license_type_name] = license_type
    if len(licenses_types) == 0:
        error_message = "No valid license type data found in the 'тип лицензии' sheet."
        raise ValueError(error_message)
    software_classes = []
    for row in sheets_data["Классификатор Минкомсвязи"][3:]:
        if row[2] is not None:
            software_class_point = str(row[1]) if row[1] is not None else None
            software_class_name = str(row[2])
            software_class_target_indicator_name = str(row[3]) if row[3] is not None else None
            software_class_target_indicator_value = float(row[4]) if row[4] is not None else None
            software_classes.append(
                SoftwareClass(
                    class_point=software_class_point,
                    class_name=software_class_name,
                    target_indicator_name=software_class_target_indicator_name,
                    target_indicator_value=software_class_target_indicator_value,
                )
            )
    software_list = []
    software_list_map = {}
    for row in sheets_data["Наименование ПО"][1:]:
        if row[0] is not None:
            software_name = str(row[0])
            software_maker_name = str(row[1]) if row[1] is not None else None
            for country in countries:
                if country.name == row[2]:
                    software_country = country
                    break
            try:
                software_country
            except NameError:
                software_country = row[2]

            for software_class in software_classes:
                if software_class.__str__ == row[5]:
                    software_software_class = software_class
                    break
            try:
                software_software_class
            except NameError:
                software_software_class = row[5]
            software_website = str(row[3]) if row[3] is not None else None
            software_purpose = str(row[4]) if row[4] is not None else None
            software_software_analogs = str(row[6]) if row[6] is not None else None
            if row[7] is not None:
                for company in companies:
                    if company.name == row[7]:
                        software_company = company
                        break
                try:
                    software_company
                except NameError:
                    software_company = row[7]
            else:
                software_company = None
            software_registry_link = str(row[9]) if row[9] is not None else None
            software_is_in_registry = row[8] in ["да", "Да", "ДА"]
            software = Software(
                country=software_country,
                software_class=software_software_class,
                name=software_name,
                maker_name=software_maker_name,
                website=software_website,
                purpose=software_purpose,
                software_analogs=software_software_analogs,
                company=software_company,
                registry_link=software_registry_link,
                is_in_registry=software_is_in_registry,
            )
            software_list.append(software)
            software_list_map[software_name] = software
    if len(software_list) == 0:
        error_message = "No valid software data found in the 'Наименование ПО' sheet."
        raise ValueError(error_message)
    order_list = []
    for row in sheets_data["Заявки"][3:]:
        if row[3] is not None:
            order_year = int(row[1])
            order_quarter = parse_quarter(row[2])
            order_supervisor_name = str(row[3])
            if order_supervisor_name not in supervisors_map:
                error_message = f"Supervisor '{order_supervisor_name}' not found in the 'ФИО Руководителя' sheet."
                raise ValueError(error_message)
            order_supervisor = supervisors_map[order_supervisor_name]
            order_employee_name = str(row[4])
            order_software_name = str(row[5])
            if order_software_name not in software_list_map:
                error_message = f"Software '{order_software_name}' not found in the 'Наименование ПО' sheet."
                raise ValueError(error_message)
            order_software = software_list_map[order_software_name]
            order_tariff_plan = str(row[7])
            order_login_and_password = str(row[8]) if row[8] is not None else None
            order_number_license = int(row[10])
            order_is_new_license = row[11] in ["новая", "Новая", "НОВАЯ"]
            order_price_for_one = float(row[12])
            order_licenses_period = row[14] if row[14] is not None else None
            if order_licenses_period is not None:
                order_licenses_period = order_licenses_period.date()
            order_license_type_name = str(row[15])
            if order_license_type_name not in licenses_types_map:
                error_message = f"License type '{order_license_type_name}' not found in the 'Тип лицензии' sheet."
                raise ValueError(error_message)
            order_license_type = licenses_types_map[order_license_type_name]
            order_useful_life = str(row[16])
            order_is_registered = row[18] in ["да", "Да", "ДА"]
            order_is_analog_in_registry = row[19] in ["да", "Да", "ДА"]
            order_company_which_will_use_name = str(row[20])
            if order_company_which_will_use_name not in companies_map:
                error_message = f"Company '{order_company_which_will_use_name}' not found in the 'Наименование проекта' sheet."
                raise ValueError(error_message)
            order_company_which_will_use = companies_map[order_company_which_will_use_name]
            order_list.append(
                Order(
                    year=order_year,
                    quarter=order_quarter,
                    supervisor=order_supervisor,
                    software=order_software,
                    employee_name=order_employee_name,
                    tariff_plan=order_tariff_plan,
                    login_and_password=order_login_and_password,
                    number_license=order_number_license,
                    is_new_license=order_is_new_license,
                    price_for_one=order_price_for_one,
                    licenses_period=order_licenses_period,
                    license_type=order_license_type,
                    useful_life=order_useful_life,
                    is_registered=order_is_registered,
                    is_analog_in_registry=order_is_analog_in_registry,
                    company_which_will_use=order_company_which_will_use,
                )
            )

    return OrderTemplate(
        file_path=order_template_file_path,
        companies=companies,
        countries=countries,
        supervisors=supervisors,
        license_types=licenses_types,
        software_classes=software_classes,
        software_list=software_list,
        order_list=order_list,
    )


def check_mandatory_sheets(sheets_titles: list[str]) -> None:
    mandatory_sheet_titles = [
        "Заявки",
        "Классификатор Минкомсвязи",
        "Наименование ПО",
        "Страны",
        "ФИО Руководителя",
        "тип лицензии",
        "Наименование проекта",
    ]
    missing_sheets = [title for title in mandatory_sheet_titles if title not in sheets_titles]
    if missing_sheets:
        error_message = f"The following mandatory sheets are missing: {', '.join(missing_sheets)}"
        raise ValueError(error_message)


def get_order_templates_paths(start_date: date, end_date: date) -> list[str]:
    order_templates_path = Path(AppConfig.get_order_path("orders/order_templates"))
    # take files, that were last modified in this period
    files = []
    for file in order_templates_path.glob("*.xlsx"):
        file_date = datetime.fromtimestamp(file.stat().st_mtime, tz=UTC).date()
        if file_date >= start_date and file_date <= end_date:
            files.append(str(file))

    return files


def get_order_templates_by_period(start_date: date, end_date: date) -> list[OrderTemplate]:
    order_templates_paths = get_order_templates_paths(start_date, end_date)

    return [get_order_template(order_template_path) for order_template_path in order_templates_paths]
