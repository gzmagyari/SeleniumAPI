# Selenium API Server

A Flask-based REST API that provides Selenium automation capabilities through HTTP endpoints. This server allows you to control Chrome browser sessions and perform various automated actions through a simple HTTP interface.

## Features

- Create and manage multiple browser sessions
- Execute various browser actions like navigation, clicking, scrolling
- Interact with page elements using CSS selectors
- Handle JavaScript execution
- Take screenshots
- Manage form inputs
- File upload support
- Custom request handling
- Wait for elements
- Scroll control
- Element attribute management

## Requirements

- Python 3.7+
- Chrome browser
- ChromeDriver (automatically managed by undetected-chromedriver)

## Installation

1. Clone the repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:

```bash
python server.py --port 5000
```

2. Send HTTP POST requests to `/execute` endpoint with JSON payload containing:
   - `action`: The action to perform
   - `params`: Parameters for the action

### Example Request

```json
{
  "action": "navigate",
  "params": {
    "session": "default",
    "url": "https://example.com"
  }
}
```

### Available Actions

1. Session Management:

   - `create_session`: Create a new browser session with optional profile

2. Navigation:

   - `navigate`: Navigate to a URL
   - `get_current_url`: Get the current page URL
   - `get_page_source`: Get the current page's HTML source

3. Element Interaction:

   - `click_element`: Click on an element
   - `paste_text`: Paste text into an element
   - `send_enter_key`: Send Enter key to an element
   - `set_input_value`: Set value of an input element
   - `get_input_value`: Get value of an input element

4. Element Information:

   - `get_element_info`: Get detailed information about an element
   - `get_all_matching_elements_info`: Get information about all matching elements
   - `get_element_parent_info`: Get information about an element's parent
   - `check_element_exists`: Check if an element exists
   - `count_elements`: Count number of matching elements
   - `get_element_children`: Get information about an element's children

5. Element Content:

   - `get_innerHTML`: Get innerHTML of an element
   - `set_innerHTML`: Set innerHTML of an element
   - `get_innerHTML_for_each`: Get innerHTML for each matching element

6. Element Attributes:

   - `get_element_attribute`: Get specific attribute of an element
   - `get_all_element_attributes`: Get all attributes of an element
   - `set_element_attribute`: Set attribute value for an element

7. JavaScript:

   - `execute_js`: Execute JavaScript code
   - `execute_js_on_element`: Execute JavaScript code on specific element

8. Scrolling:

   - `scroll_to_element`: Scroll element into view
   - `scroll_to_top`: Scroll to top of page
   - `scroll_to_bottom`: Scroll to bottom of page

9. Page State:

   - `is_page_loading`: Check if page is still loading
   - `wait_for_element`: Wait for element to appear
   - `get_screenshot`: Take screenshot of current page

10. Network:
    - `send_request`: Send HTTP request with various options (GET, POST, multipart)

## API Response Format

All API responses follow this format:

```json
{
  "status": "success/error",
  "message": "Description of what happened",
  "data": "Optional data returned by the action"
}
```

## Error Handling

The API includes comprehensive error handling and returns appropriate HTTP status codes and error messages when something goes wrong.

## Notes

- The server uses undetected-chromedriver to avoid detection by anti-bot systems
- Multiple browser sessions can be managed simultaneously
- Custom user profiles can be used for browser sessions
- The server supports both regular and multipart requests

## License

This project is open source and available under the MIT License.
