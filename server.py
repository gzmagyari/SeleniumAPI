import argparse
import time
from flask import Flask, request, jsonify
from selenium import webdriver
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import re
import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import pyperclip

app_path = os.path.dirname(__file__)
app = Flask(__name__)

sessions = {}

def get_session(name, profile = ""):
    if name in sessions:
        return sessions[name]
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--window-size=375x667')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--no-first-run --no-service-autorun --password-store=basic --no-default-browser-check')

    profile = profile.lower();
    if profile != "" and profile != "default":
        profile_path = os.path.join(app_path, "Data/Profiles/" + profile)
        chrome_options.user_data_dir = profile_path

    driver = uc.Chrome(options=chrome_options)
    sessions[name] = driver
    return driver

def find_elements(driver, css_selector, element_list=None):
    if element_list is None:
        element_list = []

    def find_parent_element(element):
        try:
            return driver.execute_script("return arguments[0].parentNode;", element)
        except NoSuchElementException:
            raise NoSuchElementException(f'No parent element found for the selector "{css_selector}"')

    if "::" not in css_selector:
        print("css_selector:"+css_selector)
        if element_list:
            return element_list[0].find_elements(By.CSS_SELECTOR, css_selector)
        else:
            return driver.find_elements(By.CSS_SELECTOR, css_selector)
    css_selector = re.sub(r'\s?([>+~])\s?', lambda match: match.group(1), css_selector)
    css_selector = css_selector.replace("::", " ::")
    print("processed:"+css_selector)
    parts = css_selector.split(" ")

    for index, part in enumerate(parts):
        print("part:"+part)
        if part.startswith("::"):
            modifier = part[2:]
            if modifier == "parent":
                element_list = [find_parent_element(element_list[0])]
            elif modifier.isdigit():
                index = int(modifier)
                if 0 <= index < len(element_list):
                    element_list = [element_list[index]]
                else:
                    raise NoSuchElementException(f'No element found with the selector "{css_selector}" at index {index}')
        else:  # Regular CSS selector
            element_list = find_elements(driver, part, element_list)
        if not element_list:
            return []

    return element_list

def find_element(driver, css_selector):
    element_list = find_elements(driver, css_selector)
    if element_list:
        return element_list[0]
    else:
        raise NoSuchElementException(f'No element found with the selector "{css_selector}"')


@app.route('/execute', methods=['POST'])
def execute():
    try:
        action = request.json.get('action')
        params = request.json.get('params')
        session_name = params.get("session", "default")
        profile = params.get("profile", "default")
        driver = get_session(session_name, profile)
        if action == 'create_session':
            if session_name:
                get_session(session_name, profile)
                return jsonify({'status': 'success', 'message': f'Created the session with name {session_name}'}), 200
            else:
                return jsonify({'status': 'error', 'message': 'Please specify the name'}), 400
        if action == 'navigate':
            url = params.get('url')
            if url:
                driver.get(url)
                return jsonify({'status': 'success', 'message': f'Navigated to {url}'}), 200
            else:
                return jsonify({'status': 'error', 'message': 'URL is missing'}), 400
        elif action == 'get_element_info':
            css_selector = params.get('css_selector')
            if css_selector:
                try:
                    element = find_element(driver, css_selector)
                    tag_name = element.tag_name
                    attributes = driver.execute_script('''
                        var element = arguments[0];
                        var attributes = {};
                        for (var i = 0; i < element.attributes.length; i++) {
                            var attr = element.attributes[i];
                            attributes[attr.name] = attr.value;
                        }
                        return attributes;
                    ''', element)
                    return jsonify({'status': 'success', 'message': f'Information for element with selector {css_selector}:', 'data': {'tag_name': tag_name, 'attributes': attributes}}), 200
                except NoSuchElementException:
                    return jsonify({'status': 'error', 'message': f'Element with selector {css_selector} not found'}), 404
            else:
                return jsonify({'status': 'error', 'message': 'CSS selector is missing'}), 400
        elif action == 'get_all_matching_elements_info':
            css_selector = params.get('css_selector')
            if css_selector:
                elements = find_elements(driver, css_selector)
                elements_data = []
                for (element, index) in enumerate(elements):
                    try:
                        tag_name = element.tag_name
                        attributes = driver.execute_script('''
                            var element = arguments[0];
                            var attributes = {};
                            for (var i = 0; i < element.attributes.length; i++) {
                                var attr = element.attributes[i];
                                attributes[attr.name] = attr.value;
                            }
                            return attributes;
                        ''', element)
                        elements_data.append({'tag_name': tag_name, 'attributes': attributes})
                    except Exception as e:
                        try:
                            element = find_element(driver, css_selector + "::" + index)
                            tag_name = element.tag_name
                            attributes = driver.execute_script('''
                                var element = arguments[0];
                                var attributes = {};
                                for (var i = 0; i < element.attributes.length; i++) {
                                    var attr = element.attributes[i];
                                    attributes[attr.name] = attr.value;
                                }
                                return attributes;
                            ''', element)
                            elements_data.append({'tag_name': tag_name, 'attributes': attributes})
                        except Exception as e2:
                            elements_data.append({'tag_name': "error", 'attributes': {}})
                return jsonify({'status': 'success', 'message': f'Information for all elements with selector {css_selector}:', 'data': elements_data}), 200
            else:
                return jsonify({'status': 'error', 'message': 'CSS selector is missing'}), 400

        elif action == 'get_element_parent_info':
            css_selector = params.get('css_selector')
            if css_selector:
                try:
                    element = find_element(driver, css_selector)
                    parent_element = driver.execute_script("return arguments[0].parentNode;", element)
                    if parent_element:
                        tag_name = parent_element.tag_name
                        attributes = driver.execute_script('''
                            var element = arguments[0];
                            var attributes = {};
                            for (var i = 0; i < element.attributes.length; i++) {
                                var attr = element.attributes[i];
                                attributes[attr.name] = attr.value;
                            }
                            return attributes;
                        ''', parent_element)
                        return jsonify({'status': 'success', 'message': f'Parent information for element with selector {css_selector}:', 'data': {'tag_name': tag_name, 'attributes': attributes}}), 200
                    else:
                        return jsonify({'status': 'error', 'message': f'Element with selector {css_selector} does not have a parent'}), 404
                except NoSuchElementException:
                    return jsonify({'status': 'error', 'message': f'Element with selector {css_selector} not found'}), 404
            else:
                return jsonify({'status': 'error', 'message': 'CSS selector is missing'}), 400
        elif action == 'execute_js_on_element':
            css_selector = params.get('css_selector')
            js = params.get('js')
            if css_selector and js:
                element = find_element(driver, css_selector)
                result = driver.execute_script(js, element)
                return jsonify({'status': 'success', 'message': f'JavaScript code executed on element with selector {css_selector}', 'data': result}), 200
            elif not css_selector:
                return jsonify({'status': 'error', 'message': 'CSS selector is missing'}), 400
            else:
                return jsonify({'status': 'error', 'message': 'JavaScript code is missing'}), 400
        elif action == 'click_element':
            css_selector = params.get('css_selector')
            if css_selector:
                element = find_element(driver, css_selector)
                element.click()
                return jsonify({'status': 'success', 'message': f'Clicked element with selector {css_selector}'}), 200
            else:
                return jsonify({'status': 'error', 'message': 'CSS selector is missing'}), 400
        elif action == 'paste_text':
            css_selector = params.get('css_selector')
            text = params.get('text')
            use_shift = params.get('use_shift', True)
            if css_selector and text is not None:
                pyperclip.copy(text)

                element = find_element(driver, css_selector)
                if use_shift:
                    element.send_keys(Keys.CONTROL + 'a')
                    lines = text.split('\n')
                    for i, part in enumerate(lines):
                        element.send_keys(part)
                        if i < len(lines) - 1:
                            ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
                else:
                    text = text.replace('\n', '\\n').replace('\r', '\\r').replace('\'', '\\\'')
                    copy_js = f"""
                        var textarea = document.createElement('textarea');
                        textarea.value = '{text}';
                        document.body.appendChild(textarea);
                        textarea.select();
                        document.execCommand('copy');
                        document.body.removeChild(textarea);
                    """
                    print("js:" + copy_js)

                    driver.execute_script(copy_js)
                    time.sleep(0.5)
                    element.click()
                    time.sleep(0.5)

                    element.send_keys(Keys.CONTROL + 'a')
                    element.send_keys(Keys.DELETE)

                    actions = ActionChains(driver)
                    actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                return jsonify({'status': 'success', 'message': f'Pasted text into element with selector {css_selector}'}), 200
            else:
                return jsonify({'status': 'error', 'message': 'CSS selector or text is missing'}), 400
        elif action == 'send_enter_key':
            css_selector = params.get('css_selector')
            if css_selector:
                element = find_element(driver, css_selector)
                element.send_keys(Keys.ENTER)
                return jsonify({'status': 'success', 'message': f'Sent Enter key to element with selector {css_selector}'}), 200
            else:
                return jsonify({'status': 'error', 'message': 'CSS selector is missing'}), 400
        elif action == 'get_innerHTML':
            css_selector = params.get('css_selector')
            if css_selector:
                element = find_element(driver, css_selector)
                inner_html = element.get_attribute('innerHTML')
                return jsonify({'status': 'success', 'message': f'innerHTML retrieved for element with selector {css_selector}', 'data': inner_html}), 200
            else:
                return jsonify({'status': 'error', 'message': 'CSS selector is missing'}), 400
        elif action == 'set_innerHTML':
            css_selector = params.get('css_selector')
            new_inner_html = params.get('html')
            if css_selector and new_inner_html is not None:
                element = find_element(driver, css_selector)
                driver.execute_script("arguments[0].innerHTML = arguments[1];", element, new_inner_html)
                return jsonify({'status': 'success', 'message': f'innerHTML set for element with selector {css_selector}'}), 200
            elif not css_selector:
                return jsonify({'status': 'error', 'message': 'CSS selector is missing'}), 400
            else:
                return jsonify({'status': 'error', 'message': 'html is missing'}), 400
        elif action == 'get_innerHTML_for_each':
            css_selector = params.get('css_selector')
            if css_selector:
                elements = find_elements(driver, css_selector)
                inner_htmls = []
                for element in elements:
                    try:
                        inner_html = element.get_attribute('innerHTML')
                        inner_htmls.append(inner_html)
                    except Exception as e:
                        inner_htmls.append("")
                return jsonify({'status': 'success', 'message': f'innerHTML retrieved for elements with selector {css_selector}', 'data': inner_htmls}), 200
            else:
                return jsonify({'status': 'error', 'message': 'CSS selector is missing'}), 400
        elif action == 'check_element_exists':
            css_selector = params.get('css_selector')
            if css_selector:
                try:
                    find_element(driver, css_selector)
                    return jsonify({'status': 'success', 'message': f'Element with selector {css_selector} exists', 'data': True}), 200
                except NoSuchElementException:
                    return jsonify({'status': 'success', 'message': f'Element with selector {css_selector} does not exist', 'data': False}), 200
            else:
                return jsonify({'status': 'error', 'message': 'CSS selector is missing'}), 400
        elif action == 'count_elements':
            css_selector = params.get('css_selector')
            if css_selector:
                elements = find_elements(driver, css_selector)
                count = len(elements)
                return jsonify({'status': 'success', 'message': f'Number of elements with selector {css_selector}', 'data': count}), 200
            else:
                return jsonify({'status': 'error', 'message': 'CSS selector is missing'}), 400
        elif action == 'get_current_url':
            current_url = driver.current_url
            return jsonify({'status': 'success', 'message': f'Current URL: {current_url}', 'data': current_url}), 200
        elif action == 'execute_js':
            js = params.get('js')
            if js:
                result = driver.execute_script(f"return {js}")
                return jsonify({'status': 'success', 'message': 'JavaScript code executed', 'data': result}), 200
            else:
                return jsonify({'status': 'error', 'message': 'JavaScript code is missing'}), 400
        elif action == 'get_screenshot':
            screenshot = driver.get_screenshot_as_base64()
            return jsonify({'status': 'success', 'message': 'Screenshot taken', 'data': screenshot}), 200
        elif action == 'is_page_loading':
            ready_state = driver.execute_script("return document.readyState;")
            is_loading = ready_state != 'complete'
            return jsonify({'status': 'success', 'message': f'Page is still loading: {is_loading}', 'data': is_loading}), 200
        elif action == 'get_page_source':
            page_source = driver.page_source
            return jsonify({'status': 'success', 'message': 'Got page source', 'data': page_source}), 200
        elif action == 'scroll_to_element':
            css_selector = params.get('css_selector')
            if css_selector:
                element = find_element(driver, css_selector)
                driver.execute_script("arguments[0].scrollIntoView();", element)
                return jsonify({'status': 'success', 'message': f'Scrolled to element with selector {css_selector}'}), 200
            else:
                return jsonify({'status': 'error', 'message': 'CSS selector is missing'}), 400
        elif action == 'scroll_to_top':
            driver.execute_script("window.scrollTo(0, 0);")
            return jsonify({'status': 'success', 'message': 'Scrolled to the top of the page'}), 200
        elif action == 'scroll_to_bottom':
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            return jsonify({'status': 'success', 'message': 'Scrolled to bottom of the page'}), 200
        elif action == 'get_input_value':
            css_selector = params.get('css_selector')
            if css_selector:
                element = find_element(driver, css_selector)
                value = driver.execute_script("return arguments[0].value;", element)
                return jsonify({'status': 'success', 'message': f'Got value for element with selector {css_selector}', 'data': value}), 200
            else:
                return jsonify({'status': 'error', 'message': 'CSS selector is missing'}), 400
        elif action == 'set_input_value':
            css_selector = params.get('css_selector')
            value = params.get('value')
            if css_selector and value is not None:
                element = find_element(driver, css_selector)
                driver.execute_script("arguments[0].value = arguments[1];", element, value)
                return jsonify({'status': 'success', 'message': f'Set value for element with selector {css_selector}'}), 200
            else:
                return jsonify({'status': 'error', 'message': 'CSS selector or value is missing'}), 400

        elif action == 'get_element_attribute':
            css_selector = params.get('css_selector')
            attribute = params.get('attribute')
            if css_selector and attribute:
                element = find_element(driver, css_selector)
                attribute_value = element.get_attribute(attribute)
                return jsonify({'status': 'success', 'message': f'Attribute value for {attribute}:', 'data': attribute_value}), 200
            else:
                return jsonify({'status': 'error', 'message': 'CSS selector or attribute is missing'}), 400
        elif action == 'get_all_element_attributes':
            css_selector = params.get('css_selector')
            if css_selector:
                element = find_element(driver, css_selector)
                attributes = driver.execute_script('''
                    var element = arguments[0];
                    var attributes = {};
                    for (var i = 0; i < element.attributes.length; i++) {
                        var attr = element.attributes[i];
                        attributes[attr.name] = attr.value;
                    }
                    return attributes;
                ''', element)
                return jsonify({'status': 'success', 'message': f'All attributes for element with selector {css_selector}:', 'data': attributes}), 200
            else:
                return jsonify({'status': 'error', 'message': 'CSS selector is missing'}), 400
        elif action == 'set_element_attribute':
            css_selector = params.get('css_selector')
            attribute = params.get('attribute')
            value = params.get('value')
            if css_selector and attribute and value is not None:
                element = find_element(driver, css_selector)
                driver.execute_script(f"arguments[0].setAttribute(arguments[1], arguments[2]);", element, attribute, value)
                return jsonify({'status': 'success', 'message': f'Set attribute {attribute} with value {value} for element with selector {css_selector}'}), 200
            else:
                return jsonify({'status': 'error', 'message': 'CSS selector, attribute, or value is missing'}), 400
        elif action == 'get_element_children':
            css_selector = params.get('css_selector')
            if css_selector:
                try:
                    element = find_element(driver, css_selector)
                    children = driver.execute_script("return Array.from(arguments[0].children);", element)
                    children_data = []
                    for child in children:
                        child_info = {
                            'tag_name': child.tag_name,
                            'attributes': driver.execute_script('''
                                var element = arguments[0];
                                var attributes = {};
                                for (var i = 0; i < element.attributes.length; i++) {
                                    var attr = element.attributes[i];
                                    attributes[attr.name] = attr.value;
                                }
                                return attributes;
                            ''', child)
                        }
                        children_data.append(child_info)
                    return jsonify({'status': 'success', 'message': f'Children for element with selector {css_selector}:', 'data': children_data}), 200
                except NoSuchElementException:
                    return jsonify({'status': 'error', 'message': f'Element with selector {css_selector} not found'}), 404
            else:
                return jsonify({'status': 'error', 'message': 'CSS selector is missing'}), 400
        elif action == 'wait_for_element':
            css_selector = params.get('css_selector')
            timeout = params.get('timeout', 10)  # Default timeout is 10 seconds
            if css_selector:
                WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
                return jsonify({'status': 'success', 'message': f'Element with selector {css_selector} is visible'}), 200
            else:
                return jsonify({'status': 'error', 'message': 'CSS selector is missing'}), 400
        elif action == 'send_request':
            url = params.get('url')
            method = params.get('method', 'GET').upper()
            data = params.get('data', {})
            is_json = params.get('json', False)
            is_multipart = params.get('multipart', False)
            headers = params.get('headers', {})
            if url:
                try:
                    cookies = driver.get_cookies()
                    s = requests.Session()
                    for cookie in cookies:
                        s.cookies.set(cookie['name'], cookie['value'])
                    if is_multipart:
                        data = MultipartEncoder(fields=data)
                        headers['Content-Type'] = data.content_type
                    if method == 'POST':
                        if is_json:
                            response = s.post(url, json=data, headers=headers)
                        else:
                            response = s.post(url, data=data, headers=headers)
                    elif method == 'PUT':
                        if is_json:
                            response = s.put(url, json=data, headers=headers)
                        else:
                            response = s.put(url, data=data, headers=headers)
                    elif method == 'DELETE':
                        response = s.delete(url, params=data, headers=headers)
                    else:
                        response = s.get(url, params=data, headers=headers)
                    return jsonify({'status': 'success', 'message': f'Request sent to {url}', 'response': response.text}), 200
                except Exception as e:
                    return jsonify({'status': 'error', 'message': f'Error while sending request to {url}: {str(e)}'}), 500
            else:
                return jsonify({'status': 'error', 'message': 'Url is missing'}), 400
        else:
            return jsonify({'status': 'error', 'message': 'Invalid action'}), 400
    except Exception as e:
        print(str(e))
        return jsonify({'status': 'error', 'message': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the Flask web app.")
    parser.add_argument('--port', type=int, default=5000, help="Port number to use for the web server (default: 5000)")
    args = parser.parse_args()
    app.run(port=args.port)