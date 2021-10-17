# VK User's Friends Report

A Python script to view or save a report about VK user's friends in CSV, TSV, JSON data formats.<br>
The script uses [friends.get](https://vk.com/dev/friends.get) request - one of
the [VK API](https://vk.com/dev/first_guide) methods that requires [access token](#access-token).

### Output report:

<img src="https://i.imgur.com/pG6hFt2.png" title="source: imgur.com" width="588" height="250"/>

### Report in data formats (JSON as example):

<img src="https://i.imgur.com/fzdHoOG.png" title="source: imgur.com"/></a>

## Setup

### 1. Install Python3 interpreter

Additional information on https://www.python.org/downloads/

### 2. Clone this repository into your directory

    $ git clone https://github.com/AbornevAA/VK_Friends_Report.git
    $ cd VK_Friends_Report

### 3. Install requirements

    $ pip install -r requirements.txt

### 4. Run application

    python main.py

## Access token

Tokens are API access keys. They are used for authorization during API requests.<br><br>
Tokens allow you to restrict access to user data using the scope parameter.<br>
It defines the scope of visibility for your application. A token with scope=friends gives access to friends and nothing
else. The token becomes less dangerous than the login and password.

### How to get access token

The token can be obtained directly from the browser. To do this, you just need to click on the correct link. How to make
the right link:

#### 1. Create a Standalone application.

Applications are created on [the page with your applications](https://vk.com/apps?act=manage). Give the application a
clear name so that in the future it is easy to remember why it was created.

#### 2. Get Standalone application client_id

Go back to the page with your applications. Click on the "Edit" button next to the desired application. His id will
appear in the field "App ID".

#### 3. Collect the link to get the key

Example of a link from the [Implicit Flow documentation](https://vk.com/dev/implicit_flow_user):

    https://oauth.vk.com/authorize?client_id=1&display=page&scope=friends&response_type=token&v=5.92&state=123456

* leave response_type and display the same as in the example.
* you got the client_id in the second step.
* v take from the page with [API versions](https://vk.com/dev/versions). Choose the most recent one.
* select scope "friends" for the script to work correctly

#### 4. Follow the collected link

You will get an access_token string like 533bacf01e1165b57531ad114461ae8736d6506a3. It will appear in the address bar,
signed as access_token. If code= appears in the address bar instead of access_token=, check that the response_type
parameter is correct.