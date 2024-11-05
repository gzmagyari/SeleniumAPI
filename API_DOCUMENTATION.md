# Selenium API Documentation

This API provides a RESTful interface for browser automation using Selenium WebDriver. All endpoints accept POST requests to `/execute` with different actions specified in the request body.

## Base URL

`http://localhost:5000`

## Common Response Format

All endpoints return responses in the following JSON format:

```json
{
  "status": "success|error",
  "message": "Description of the result",
  "data": "Optional data field depending on the action"
}
```

## Available Actions

### Session Management

#### Create Session

Creates a new browser session.

```json
{
  "action": "create_session",
  "params": {
    "session": "session_name",
    "profile": "profile_name"
  }
}
```

- `session`: (required) Name of the session to create
- `profile`: (optional) Profile name to use, defaults to "default"

### Navigation

#### Navigate to URL

```json
{
  "action": "navigate",
  "params": {
    "session": "session_name",
    "url": "https://example.com"
  }
}
```

- `url`: (required) The URL to navigate to
- `session`: (optional) Session name to use

#### Get Current URL

```json
{
  "action": "get_current_url",
  "params": {
    "session": "session_name"
  }
}
```

### Element Interactions

#### Click Element

```json
{
  "action": "click_element",
  "params": {
    "session": "session_name",
    "css_selector": "button.submit-btn"
  }
}
```

- `css_selector`: (required) CSS selector of the element to click

#### Paste Text

```json
{
  "action": "paste_text",
  "params": {
    "session": "session_name",
    "css_selector": "textarea#content",
    "text": "Text to paste",
    "use_shift": true
  }
}
```

- `css_selector`: (required) CSS selector of the target element
- `text`: (required) Text to paste
- `use_shift`: (optional) Whether to use shift+enter for newlines, defaults to true

#### Send Enter Key

```json
{
  "action": "send_enter_key",
  "params": {
    "session": "session_name",
    "css_selector": "input#search"
  }
}
```

- `css_selector`: (required) CSS selector of the target element

### Element State

#### Check Element Exists

```json
{
  "action": "check_element_exists",
  "params": {
    "session": "session_name",
    "css_selector": "div.content"
  }
}
```

- `css_selector`: (required) CSS selector to check

#### Count Elements

```json
{
  "action": "count_elements",
  "params": {
    "session": "session_name",
    "css_selector": "li.item"
  }
}
```

- `css_selector`: (required) CSS selector to count

#### Get Element Info

```json
{
  "action": "get_element_info",
  "params": {
    "session": "session_name",
    "css_selector": "div#main"
  }
}
```

- `css_selector`: (required) CSS selector of the element

### Element Content

#### Get innerHTML

```json
{
  "action": "get_innerHTML",
  "params": {
    "session": "session_name",
    "css_selector": "div.content"
  }
}
```

- `css_selector`: (required) CSS selector of the element

#### Set innerHTML

```json
{
  "action": "set_innerHTML",
  "params": {
    "session": "session_name",
    "css_selector": "div.content",
    "html": "<p>New content</p>"
  }
}
```

- `css_selector`: (required) CSS selector of the element
- `html`: (required) New HTML content

### Form Interactions

#### Get Input Value

```json
{
  "action": "get_input_value",
  "params": {
    "session": "session_name",
    "css_selector": "input#username"
  }
}
```

- `css_selector`: (required) CSS selector of the input element

#### Set Input Value

```json
{
  "action": "set_input_value",
  "params": {
    "session": "session_name",
    "css_selector": "input#username",
    "value": "john_doe"
  }
}
```

- `css_selector`: (required) CSS selector of the input element
- `value`: (required) New value to set

### Page State

#### Is Page Loading

```json
{
  "action": "is_page_loading",
  "params": {
    "session": "session_name"
  }
}
```

#### Get Page Source

```json
{
  "action": "get_page_source",
  "params": {
    "session": "session_name"
  }
}
```

#### Get Screenshot

```json
{
  "action": "get_screenshot",
  "params": {
    "session": "session_name"
  }
}
```

### Scrolling

#### Scroll to Element

```json
{
  "action": "scroll_to_element",
  "params": {
    "session": "session_name",
    "css_selector": "div#target"
  }
}
```

- `css_selector`: (required) CSS selector of the target element

#### Scroll to Top

```json
{
  "action": "scroll_to_top",
  "params": {
    "session": "session_name"
  }
}
```

#### Scroll to Bottom

```json
{
  "action": "scroll_to_bottom",
  "params": {
    "session": "session_name"
  }
}
```

### JavaScript Execution

#### Execute JavaScript

```json
{
  "action": "execute_js",
  "params": {
    "session": "session_name",
    "js": "document.title"
  }
}
```

- `js`: (required) JavaScript code to execute

#### Execute JavaScript on Element

```json
{
  "action": "execute_js_on_element",
  "params": {
    "session": "session_name",
    "css_selector": "div#target",
    "js": "arguments[0].style.backgroundColor = 'red'"
  }
}
```

- `css_selector`: (required) CSS selector of the target element
- `js`: (required) JavaScript code to execute on the element

### Network Requests

#### Send Request

```json
{
  "action": "send_request",
  "params": {
    "session": "session_name",
    "url": "https://api.example.com/data",
    "method": "POST",
    "data": { "key": "value" },
    "json": true,
    "multipart": false,
    "headers": { "Authorization": "Bearer token" }
  }
}
```

- `url`: (required) URL to send the request to
- `method`: (optional) HTTP method (GET, POST, PUT, DELETE), defaults to GET
- `data`: (optional) Request data/parameters
- `json`: (optional) Whether to send data as JSON, defaults to false
- `multipart`: (optional) Whether to send as multipart/form-data, defaults to false
- `headers`: (optional) Request headers

### Element Attributes

#### Get Element Attribute

```json
{
  "action": "get_element_attribute",
  "params": {
    "session": "session_name",
    "css_selector": "img#logo",
    "attribute": "src"
  }
}
```

- `css_selector`: (required) CSS selector of the element
- `attribute`: (required) Name of the attribute to get

#### Get All Element Attributes

```json
{
  "action": "get_all_element_attributes",
  "params": {
    "session": "session_name",
    "css_selector": "div#main"
  }
}
```

- `css_selector`: (required) CSS selector of the element

#### Set Element Attribute

```json
{
  "action": "set_element_attribute",
  "params": {
    "session": "session_name",
    "css_selector": "img#logo",
    "attribute": "src",
    "value": "new-image.jpg"
  }
}
```

- `css_selector`: (required) CSS selector of the element
- `attribute`: (required) Name of the attribute to set
- `value`: (required) New value for the attribute

### Element Relationships

#### Get Element Children

```json
{
  "action": "get_element_children",
  "params": {
    "session": "session_name",
    "css_selector": "ul#menu"
  }
}
```

- `css_selector`: (required) CSS selector of the parent element

### Waiting

#### Wait for Element

```json
{
  "action": "wait_for_element",
  "params": {
    "session": "session_name",
    "css_selector": "div.loading",
    "timeout": 10
  }
}
```

- `css_selector`: (required) CSS selector of the element to wait for
- `timeout`: (optional) Maximum time to wait in seconds, defaults to 10
