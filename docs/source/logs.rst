.. role:: magenta
.. _log:

Logs
=====

Log Object
----------

A single log is a single event submited by a user or device, regarding a single activity.

When submitting a log, the following format should be used::

    {
        "id": 123,
        "origId": 0,
        "category": "profile",
        "start": ISODate("2011-06-08T23:31:31.491Z"),
        "end": ISODate("2011-06-08T23:31:31.491Z"),
        "text": "<string>",
        "nodes": [
            {
                "nodeId": 17,
                "value": 15,
            }
        ]
    }
    
``id`` should be omitted for new logs.

When requesting logs, some additional fields are present::

    {
        "id": 123,
        "origId": 0,
        "oper": "i",
        "createUTC": ISODate("2011-06-08T23:31:31.491Z"),
        "update": ISODate("2011-06-08T23:31:31.491Z"),
        "source": "client.iphone",
        "category": "profile",
        "userId":"QWERTY",
        "start": ISODate("2011-06-08T23:31:31.491Z"),
        "end": ISODate("2011-06-08T23:31:31.491Z"),
        "text": "<string>",
        "nodes": [
            {
                "nodeId": 17,
                "value": 15,
                "propertyId": 5595,
                "loggableId": 4884
            }
        ]
    }



Logs API
--------

.. automodule:: wikilife_ws.rest.logs
   :members:
