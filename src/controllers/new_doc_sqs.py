from src.dependencies import emails
from src.dependencies.account_api import AccountAPIHandler
from src.views.create_document import create_pdf_report_external
from src.views import property_info
from src import config

class NewDocSqs:
    def __init__(self, body):
        print("Starting document creation process", flush=True)

        report_id = body.get('report_id')
        if report_id is None:
            print("Report ID is missing", flush=True)
            return

        # Retrieve report details
        report_details = AccountAPIHandler().set_report_creation_time(report_id)
        self._update_body_with_report_details(body, report_details)

        property_data = self._get_or_fetch_property_data(report_id, body)

        print("Document creation process completed", flush=True)

        doc_name = create_pdf_report_external(report_id, body, property_data)
        AccountAPIHandler().report_created(report_id)

    def _update_body_with_report_details(self, body, report_details):
        address = f"{report_details.get('house_number','')} {report_details.get('street','')} {report_details.get('postcode','')}"
        queue_data = {
            "type": report_details.get("house_type", ""),
            "house_number": report_details.get("house_number", ""),
            "street": report_details.get('street', ""),
            "postcode": report_details.get('postcode'),
            "address": {"address": address},
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
            "headervalue": report_details.get('headervalue', ''),
            "headingvaluefound": report_details.get('headingvaluefound', "false"),
        }

        body.update(queue_data)

    def _get_or_fetch_property_data(self, report_id, body):
        if AccountAPIHandler().get_report_data_stored(report_id):
            return AccountAPIHandler().get_report_data(report_id)
        else:
            property_data = property_info.get_info(
                body.get("postcode"),
                body.get("house_number"),
                body.get("street"),
                4,
                body.get("type"),
                body.get("lon"),
                body.get("lat"),
                body.get("uprn")
            )
            AccountAPIHandler().store_report_data(report_id, property_data)
            return property_data
