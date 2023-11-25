from src.dependencies import emails
from src import config

from src.views.create_document import create_pdf_report_external
from src.dependencies import account_api
from src.views import property_info


class NewDocSqs(object):
    def __init__(self, body):

        print("doing some stuff", flush=True)

        report_id = body.get('report_id', None)

        # get report data from account_api
        report_details = account_api.set_report_creation_time(report_id)

        # get the following from account_api and add to body
        queue_data = {
            "type": report_details.get("house_type", ""),
            "house_number": report_details.get("house_number", ""),
            "street": report_details.get('street', ""),
            "postcode": report_details.get('postcode'),
            "address": {
                "address": f"{report_details.get('house_number','')} {report_details.get('street','')} {report_details.get('postcode','')}"
            },
            "lon": report_details.get('longitude'),
            "lat": report_details.get('latitude'),
            "uprn": report_details.get('uprn', ''),
            "company_id": "None",
            "company_name": "UK Property Report",
            "template_name": "propery_report.html",
            "subject": "Your property report has arrived",
            "doc_type": "None",
            "external": "yes",
            "pdf_name": "property_report",
            "logo_url": f"{config.website_url_cdn}/logo.jpg",
            "letterhead_image": f"{config.website_url_cdn}/logo.jpg",
            "location": "email",
            "uprn": report_details.get('uprn', ''),
            "headervalue": report_details.get('headervalue', ''),
            "headingvaluefound": report_details.get('headingvaluefound', "false"),
        }

        body.update(queue_data)

        if report_details.get("report_data_stored", False):
            property_data = account_api.get_report_data(report_id)
        else:
            property_data = property_info.get_info(
                queue_data.get("postcode"),
                queue_data.get("house_number"),
                queue_data.get("street"),
                4,
                queue_data.get("type"),
                queue_data.get("lon"),
                queue_data.get("lat"),
                queue_data.get("uprn")
            )
            account_api.store_report_data(report_id, property_data)

        print("ok finished now", flush=True)

        # create pdf version of report
        doc_name = create_pdf_report_external(report_id, body, property_data)

        account_api.report_created(report_id)
