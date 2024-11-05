# Selenium API Documentation

This API provides a RESTful interface for browser automation using Selenium WebDriver. All endpoints are accessed through POST requests to `/execute` with different actions specified in the request body.

## Base URL

`http://localhost:5000`

## HTTP Method

All requests use the **POST** method to the `/execute` endpoint.

## Common Response Format

All endpoints return responses in the following JSON format:

### Success Response

```json
{
  "status": "success",
  "message": "Description of the result",
  "data": "Optional data field depending on the action"
}
```

### Error Response

```json
{
  "status": "error",
  "message": "Description of the error"
}
```

## Available Actions

### Session Management

#### Create Session

Creates a new browser session.

**Request:**

```json
{
  "action": "create_session",
  "params": {
    "session": "session_name",
    "profile": "profile_name"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Created the session with name session_name"
}
```

### Navigation

#### Navigate to URL

**Request:**

```json
{
  "action": "navigate",
  "params": {
    "session": "session_name",
    "url": "https://example.com"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Navigated to https://example.com"
}
```

#### Get Current URL

**Request:**

```json
{
  "action": "get_current_url",
  "params": {
    "session": "session_name"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Current URL: https://example.com",
  "data": "https://example.com"
}
```

### Element Interactions

#### Click Element

**Request:**

```json
{
  "action": "click_element",
  "params": {
    "session": "session_name",
    "css_selector": "button.submit-btn"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Clicked element with selector button.submit-btn"
}
```

#### Paste Text

**Request:**

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

**Response:**

```json
{
  "status": "success",
  "message": "Pasted text into element with selector textarea#content"
}
```

#### Send Enter Key

**Request:**

```json
{
  "action": "send_enter_key",
  "params": {
    "session": "session_name",
    "css_selector": "input#search"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Sent Enter key to element with selector input#search"
}
```

### Element State

#### Check Element Exists

**Request:**

```json
{
  "action": "check_element_exists",
  "params": {
    "session": "session_name",
    "css_selector": "div.content"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Element with selector div.content exists",
  "data": true
}
```

#### Count Elements

**Request:**

```json
{
  "action": "count_elements",
  "params": {
    "session": "session_name",
    "css_selector": "li.item"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Number of elements with selector li.item",
  "data": 5
}
```

#### Get Element Info

**Request:**

```json
{
  "action": "get_element_info",
  "params": {
    "session": "session_name",
    "css_selector": "div#main"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Information for element with selector div#main:",
  "data": {
    "tag_name": "div",
    "attributes": {
      "id": "main",
      "class": "container"
    }
  }
}
```

### Element Content

#### Get innerHTML

**Request:**

```json
{
  "action": "get_innerHTML",
  "params": {
    "session": "session_name",
    "css_selector": "div.content"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "message": "innerHTML retrieved for element with selector div.content",
  "data": "<p>Content here</p>"
}
```

#### Set innerHTML

**Request:**

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

**Response:**

```json
{
  "status": "success",
  "message": "innerHTML set for element with selector div.content"
}
```

### Form Interactions

#### Get Input Value

**Request:**

```json
{
  "action": "get_input_value",
  "params": {
    "session": "session_name",
    "css_selector": "input#username"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Got value for element with selector input#username",
  "data": "john_doe"
}
```

#### Set Input Value

**Request:**

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

**Response:**

```json
{
  "status": "success",
  "message": "Set value for element with selector input#username"
}
```

### Page State

#### Is Page Loading

**Request:**

```json
{
  "action": "is_page_loading",
  "params": {
    "session": "session_name"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Page is still loading: false",
  "data": false
}
```

#### Get Page Source

**Request:**

```json
{
  "action": "get_page_source",
  "params": {
    "session": "session_name"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Got page source",
  "data": "<html>...</html>"
}
```

#### Get Screenshot

**Request:**

```json
{
  "action": "get_screenshot",
  "params": {
    "session": "session_name"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Screenshot taken",
  "data": "base64_encoded_image_data"
}
```

### Scrolling

#### Scroll to Element

**Request:**

```json
{
  "action": "scroll_to_element",
  "params": {
    "session": "session_name",
    "css_selector": "div#target"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Scrolled to element with selector div#target"
}
```

#### Scroll to Top

**Request:**

```json
{
  "action": "scroll_to_top",
  "params": {
    "session": "session_name"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Scrolled to the top of the page"
}
```

#### Scroll to Bottom

**Request:**

```json
{
  "action": "scroll_to_bottom",
  "params": {
    "session": "session_name"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Scrolled to bottom of the page"
}
```

### JavaScript Execution

#### Execute JavaScript

**Request:**

```json
{
  "action": "execute_js",
  "params": {
    "session": "session_name",
    "js": "document.title"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "message": "JavaScript code executed",
  "data": "Page Title"
}
```

#### Execute JavaScript on Element

**Request:**

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

**Response:**

```json
{
  "status": "success",
  "message": "JavaScript code executed on element with selector div#target",
  "data": null
}
```

### Network Requests

#### Send Request

**Request:**

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

**Response:**

```json
{
  "status": "success",
  "message": "Request sent to https://api.example.com/data",
  "response": "Response data from the server"
}
```

### Element Attributes

#### Get Element Attribute

**Request:**

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

**Response:**

```json
{
  "status": "success",
  "message": "Attribute value for src:",
  "data": "https://example.com/logo.png"
}
```

#### Get All Element Attributes

**Request:**

```json
{
  "action": "get_all_element_attributes",
  "params": {
    "session": "session_name",
    "css_selector": "div#main"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "message": "All attributes for element with selector div#main:",
  "data": {
    "id": "main",
    "class": "container",
    "data-role": "content"
  }
}
```

#### Set Element Attribute

**Request:**

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

**Response:**

```json
{
  "status": "success",
  "message": "Set attribute src with value new-image.jpg for element with selector img#logo"
}
```

### Element Relationships

#### Get Element Children

**Request:**

```json
{
  "action": "get_element_children",
  "params": {
    "session": "session_name",
    "css_selector": "ul#menu"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "message": "Children for element with selector ul#menu:",
  "data": [
    {
      "tag_name": "li",
      "attributes": {
        "class": "menu-item"
      }
    }
  ]
}
```

### Waiting

#### Wait for Element

**Request:**

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

**Response:**

```json
{
  "status": "success",
  "message": "Element with selector div.loading is visible"
}
```
