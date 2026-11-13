import os
import requests

# original curl:
# curl -X POST https://cpee.org/transformation/mermaid/cpee/ -F "description=@gdpr_1_data_breach.cpee.xml;type=text/xml" -F "type=description"
URL = "https://cpee.org/transformation/mermaid/cpee/"


def convert_cpee_mermaid(xml_file):
    """Converts a cpee xml file into mermaid via the cpee.org transformation service. Returns the mermaid as string."""
    with open(xml_file, "rb") as file:
        files = {
            "description": (os.path.basename(xml_file), file, "text/xml"),  # -F "description=@<file>;type=text/xml"
            "type": (None, "description"),                                  # -F "type=description"
        }
        response = requests.post(URL, files=files)
    response.raise_for_status()
    return response.text
