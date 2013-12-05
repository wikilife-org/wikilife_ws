OAuth API
=========

Wikilife OAuth 2.0
------------------

Apps connect with Wikilife via `OAuth 2.0 <http://oauth.net/2/>`_ (`rfc6749 <http://tools.ietf.org/html/rfc6749>`_). This is the standard used by most major API providers, including Facebook.

Registration
------------

Start by `registering your app <https://wikilife.org/dev/dashboard/>`_ to obtain its Wikilife API credentials. Be sure to use an account with a secure password to own these credentials. Since each set of credentials is tied to a particular URL, you may want to create different credentials for your development server and production server. For the purposes of OAuth, your “key” from that registration process is your “client id” here, and your secret from registering is your secret here.

Access token
------------

Access tokens allow apps to make requests to Wikilife on the behalf of a user. Each access token is unique to the user and consumer key. Access tokens do not expire, but they may be revoked by the user.
There are two flows for authenticating a user and obtaining an access token: code and token, which are generally used by web and client apps, respectively

**Code flow (preferred)**

Web server applications

    - Redirect users who wish to authenticate to
        ``https://api.wikilife.org/oauth2/authorize?client_id=YOUR_CLIENT_ID&response_type=code&redirect_uri=YOUR_REGISTERED_REDIRECT_URI``
    - If a user accepts, they will be redirected back to
        ``https://YOUR_REGISTERED_REDIRECT_URI/?code=CODE``
    - Your server will make a request for
        ``https://api.wikilife.org/oauth2/access_token?client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&grant_type=authorization_code&code=CODE``
    - The response will be JSON:
        ``{ status: OK, data: {access_token:  ACCESS_TOKEN , user_id: USER_ID } }``
                    

Save this access token for this user in your database.


**Token flow**

Client applications. If you have no substantive server code, you can use the token flow outlined below.
 
    - Redirect users who wish to authenticate to
        ``https://api.wikilife.org/oauth2/authorize?client_id=CLIENT_ID&response_type=token&redirect_uri=YOUR_REGISTERED_REDIRECT_URI``
    - If a user accepts, they will be redirected back to:
        ``http://YOUR_REGISTERED_REDIRECT_URI/?access_token=ACCESS_TOKEN&user_id=USER_ID``

If your app is pure Javascript, you can easily parse the token from the URL. If your app is a native phone app then perform the flow in an embedded webview, redirecting the user to a dummy website. You can then grab the token off of the URL and close the browser.

Requests
--------
Once you have an access token. It’s easy to use any of the endpoints, by just adding ``oauth_token=ACCESS_TOKEN`` to your GET or POST request. For example, from the command line, you can do

``$ curl https://api.wikilife.org/PATH_TO_ENDPOINT?oauth_token=ACCESS_TOKEN``

Userless access
---------------
Some of our endpoints that don’t pertain to specific user information, such as ``/2/logs/latest`` are enabled for userless access (meaning you don’t need to have a user auth your app for access). To make a userless request, specify your ``consumer`` key's Client ID and Secret instead of an auth token in the request URL.
``https://api.wikilife.org/2/logs/latest?amount=20&client_id=CLIENT_ID&client_secret=CLIENT_SECRET``

Notes on OAuth
--------------
Although at this time we do not expire OAuth access tokens, you should be prepared for this possibility in the future. Also remember that a user may disconnect via the Wikilife settings page at any time. Using ``/authorize`` will ask the user to re-authenticate their identity and reauthorize your app while giving the user the option to login under a different account.