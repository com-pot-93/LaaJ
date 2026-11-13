import os
import time
from contextlib import contextmanager

import requests
from playwright.sync_api import sync_playwright

CHROME_PATH = "/home/i17/projects/SAP/t2p_clean/src/chrome/linux-140.0.7339.207/chrome-linux64/chrome"
INSTANCE_NUMBER = "9734"


@contextmanager
def open_instance(instance_number=INSTANCE_NUMBER, chrome_path=CHROME_PATH):
    """Opens the monitor of the cpee instance in a headless chrome and accepts the terms, yields the page.
    Use it to convert several models with one browser:
        with open_instance("9734") as page:
            bpmn = convert_cpee_bpmn(xml_file, "9734", page)"""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=chrome_path, headless=True)
        try:
            page = browser.new_page(accept_downloads=True)
            page.goto("https://autobpmn.ai/flow/?monitor=https://autobpmn.ai/flow/engine/{}/".format(instance_number))
            page.click("input[type='checkbox']#iagree")
            page.click("button#icontinue")
            page.wait_for_load_state("networkidle")
            time.sleep(2)
            yield page
        finally:
            browser.close()


def convert_cpee_bpmn(xml_file, instance_number=INSTANCE_NUMBER, page=None):
    """Converts a cpee xml file into bpmn via the cpee instance on autobpmn.ai. Returns the bpmn xml as string.
    page: an opened instance (open_instance) of the same instance number, otherwise a browser is started for this call only."""
    if page is None:
        with open_instance(instance_number) as page:
            return convert_cpee_bpmn(xml_file, instance_number, page)

    url = "https://autobpmn.ai/flow/engine/{}/properties/dslx/".format(instance_number)
    with open(xml_file, "rb") as file:
        response = requests.put(url, files={"dslx": (os.path.basename(xml_file), file, "text/xml")})
    response.raise_for_status()
    time.sleep(1)  # the monitor needs a moment to show the new model

    with page.expect_download() as download_info:
        page.click("button[name='savebpmnfile']")
    with open(download_info.value.path(), "r") as file:  # temporary download of playwright, removed with the browser
        return file.read()
