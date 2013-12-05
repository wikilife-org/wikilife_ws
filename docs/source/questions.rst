.. role:: magenta

Questions
=========

.. _question:

Question Object
---------------

A question object holds a question's text and the id of the value-node which has it's possible answers. ::

    {
        "quesiton_id": 40,
        "text": "How many cigarettes a day do you smoke?",
        "node_id": 241559
    }

* ``question_id`` is the question's unique id.
* ``text`` a string containing the question in the user's locale. 
* ``node_id`` the id of the value-node which defines the type of answer this question has.

Questions API
-------------

.. automodule:: wikilife_ws.rest.questions
   :members:

