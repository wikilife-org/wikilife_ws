# coding=utf-8

from wikilife_utils.parsers.json_parser import JSONParser
from wikilife_ws.rest.base_handler import BaseHandler, BaseHandlerV2
from wikilife_ws.utils.catch_exceptions import catch_exceptions
from wikilife_ws.utils.deprecated import Deprecated
from wikilife_ws.utils.oauth import authenticated, userless
from wikilife_ws.utils.route import Route

USER_STATS_BY_TAG = 5
USER_STATS_BY_QUESTION = 6


class BaseQuestionsHandlerV2(BaseHandlerV2):

    _question_srv = None

    def initialize(self):
        super(BaseQuestionsHandlerV2, self).initialize()
        self._question_srv = self._service_builder.build_question_service()

    def _q_v3_to_v2(self, qv3):
        qv2 = None

        if qv3 != None:
            qv2 = {}
            qv2["pk"] = qv3["id"]
            qv2["fields"] = {}
            qv2["fields"]["create_time"] = qv3["createUTC"]
            qv2["fields"]["status"] = qv3["status"] 
            qv2["fields"]["text"] = qv3["statement"]
            qv2["fields"]["tags"] = qv3["tags"]
            qv2["fields"]["frequency"] = qv3["frequency"] 
            qv2["fields"]["answer"] = qv3["answerTemplate"]
            qv2["fields"]["condition"] = qv3["_old_condition"]
            qv2["fields"]["node"] = qv3["_old_target"]
        
        return qv2


class BaseQuestionsHandler(BaseHandler):

    _question_srv = None

    def initialize(self):
        super(BaseQuestionsHandler, self).initialize()
        self._question_srv = self._service_builder.build_question_service()


@Deprecated(20130201)
@Route("/2/questions/show/(?P<user_id>[-\w]+)")
@Route("/2/questions/show/(?P<user_id>[-\w]+).json")
class QuestionsNextHandlerV2(BaseQuestionsHandlerV2):
    """
    """

    def get(self, user_id):
        """
        Returns next question for a user.

        :rtype: A :ref:`question`

        """
        try:
            tag = self.get_argument("tag", None)
            question_dto = self._question_srv.get_next_question(user_id, tag)
            self.success("", question_dto)

        except Exception, e:
            self._logger.exception("")
            self.error(str(e))


@Route("/3/questions/next")
class QuestionsNextHandler(BaseQuestionsHandler):
    """
    """

    @authenticated
    @catch_exceptions
    def get(self, user_id):
        """
        Returns next question for a user.

        :rtype: A :ref:`question`

        """
        tag = self.get_argument("tag", None)
        question_dto = self._question_srv.get_next_question(user_id, tag)
        self.success(question_dto)


@Deprecated(20130201)
@Route("/2/questions/tags/all")
@Route("/2/questions/categories/all.json")
class QuestionsUserStatusHandlerV2(BaseQuestionsHandlerV2):
    """
    """

    def get(self):
        """
        Return a list of tags, and the amount of answered/unanswered questions.

        :param user_id:

        Response::

            {
              "status": "OK",
              "message": "",
              "data": [
                {
                  "pending_questions": 0,
                  "tag": "Education",
                  "total_questions": 3
                },
                {
                  "pending_questions": 0,
                  "tag": "Exercise",
                  "total_questions": 4
                },
                {
                  "pending_questions": 0,
                  "tag": "Family",
                  "total_questions": 23
                },
                {
                  "pending_questions": 0,
                  "tag": "Health",
                  "total_questions": 37
                },
                {
                  "pending_questions": 7,
                  "tag": "Leisure",
                  "total_questions": 16
                },
                {
                  "pending_questions": 5,
                  "tag": "Lifestyle",
                  "total_questions": 22
                },
                {
                  "pending_questions": 7,
                  "tag": "Nutrition",
                  "total_questions": 13
                },
                {
                  "pending_questions": 1,
                  "tag": "Profile",
                  "total_questions": 3
                },
                {
                  "pending_questions": 19,
                  "tag": "Psychological",
                  "total_questions": 29
                },
                {
                  "pending_questions": 0,
                  "tag": "Sex",
                  "total_questions": 3
                },
                {
                  "pending_questions": 7,
                  "tag": "Travel",
                  "total_questions": 10
                },
                {
                  "pending_questions": 1,
                  "tag": "Work",
                  "total_questions": 1
                }
              ]
            }

        """
        try:
            user_id = self.get_argument("user_id")
            categories = self._question_srv.get_categories(user_id)
            self.success("", categories)

        except Exception, e:
            self._logger.exception("")
            self.error(str(e))


@Route("/3/questions/user/status")
class QuestionsUserStatusHandler(BaseQuestionsHandler):
    """
    """

    @authenticated
    @catch_exceptions
    def get(self ,user_id):
        """
        Return a list of tags, and the amount of answered/unanswered questions.

        Response::

              [
                {
                  "pending_questions": 0,
                  "tag": "Education",
                  "total_questions": 3
                },
                {
                  "pending_questions": 0,
                  "tag": "Exercise",
                  "total_questions": 4
                },
                {
                  "pending_questions": 0,
                  "tag": "Family",
                  "total_questions": 23
                }
              ]
        """
        categories = self._question_srv.get_categories(user_id)
        self.success(categories)


@Deprecated(20130201)
@Route("/2/questions/tags.json")
class QuestionsTagsHandlerV2(BaseQuestionsHandlerV2):
    """
    """

    def get(self):
        """
        Return the list of questions tags::

            ["tag-1", "tag-2", "tag-n"]
        """
        try:
            tags = self._question_srv.get_questions_tags()
            self.success("", tags)

        except Exception, e:
            self._logger.exception("")
            self.error(str(e))


@Route("/3/questions/tags")
class QuestionsTagsHandler(BaseQuestionsHandler):
    """
    """

    @userless
    @catch_exceptions
    def get(self):
        """
        Return the list of questions tags::

            ["tag-1", "tag-2", "tag-n"]
        """
        tags = self._question_srv.get_questions_tags()
        self.success(tags)


@Deprecated(20130201)
@Route("/2/questions/(?P<tag>[-\w]+).json")
class QuestionsByTagHandlerV2(BaseQuestionsHandlerV2):
    """
    """

    def get(self, tag):
        """
        Return the list of questions with specified tag
        """
        try:
            questions = self._question_srv.get_questions_by_tag(tag)
            qv2s = []

            for qv3 in questions:
                qv2s.append(self._q_v3_to_v2(qv3))

            self.success("", qv2s)

        except Exception, e:
            self._logger.exception("")
            self.error(str(e))


@Route("/3/questions/(?P<tag>[-\w]+)")
class QuestionsByTagHandler(BaseQuestionsHandler):
    """
    """

    @userless
    @catch_exceptions
    def get(self, tag):
        """
        Return the list of questions with specified tag
        """
        questions = self._question_srv.get_questions_by_tag(tag)
        self.success(questions)


@Deprecated(20130201)
@Route("/2/questions/answer/add.json")
class AnswersHandlerV2(BaseQuestionsHandlerV2):
    """
    """

    def post(self):
        """
        Add an answer and returns stats

        Request::

            {
              "answer": {
                "execute_time": "2012-10-29 12:53:29 -0300",
                "answer_value": "Yes",
                "question_id": 1046,
                "answer_id": 0
              },
              "user_id": "32UJ6R",
              "answer_type": "1"
            }

        Response::

            {
              "status": "OK",
              "message": "",
              "data": {
                "answer": {
                  "answer_value": "Yes",
                  "answer_id": 2414,
                  "question_id": 1046,
                  "log_id": 380910,
                  "execute_time": "2012-10-29 12:53:29 -0300"
                },
                "stat": {
                  "p": {
                    "stats_name": "Are you currently working?",
                    "users_count": "16"
                  },
                  "rows": [
                    {
                      "c": [
                        {
                          "v": "14"
                        },
                        {
                          "v": "Yes"
                        }
                      ]
                    },
                    {
                      "c": [
                        {
                          "v": "2"
                        },
                        {
                          "v": "No"
                        }
                      ]
                    }
                  ],
                  "cols": [
                    {
                      "type": "number",
                      "id": "num_answers",
                      "label": "Number of Answers"
                    },
                    {
                      "type": "string",
                      "id": "option",
                      "label": "Option"
                    }
                  ]
                },
                "question": {
                  "text": "Are you currently working?",
                  "node_id": 400052,
                  "question_id": 1046
                }
              }
            }

        """
        try:
            request_body = JSONParser.to_collection(self.request.body)
            user_id = request_body["user_id"]
            answer = request_body["answer"]
            ans_type = int(request_body["answer_type"])

            result = self._question_srv.add_answer(user_id, answer, ans_type)
            self.success("", result)

        except Exception, e:
            self._logger.exception("")
            self.error(str(e))


@Route("/3/questions/answers/")
class AnswersAddHandler(BaseQuestionsHandler):
    """
    """

    @authenticated
    @catch_exceptions
    def post(self, user_id):
        """
        Add an answer and returns stats

        Request::

        {
          "answer": {
            "execute_time": "2012-10-29 12:53:29 -0300",
            "answer_value": "Yes",
            "question_id": 1046,
            "answer_id": 0
          },
          "answer_type": "1"
        }

        Response::

          {
            "answer": {
              "answer_value": "Yes",
              "answer_id": 2414,
              "question_id": 1046,
              "log_id": 380910,
              "execute_time": "2012-10-29 12:53:29 -0300"
            },
            "stat": {
              "p": {
                "stats_name": "Are you currently working?",
                "users_count": "16"
              },
              "rows": [
                {
                  "c": [
                    {
                      "v": "14"
                    },
                    {
                      "v": "Yes"
                    }
                  ]
                },
                {
                  "c": [
                    {
                      "v": "2"
                    },
                    {
                      "v": "No"
                    }
                  ]
                }
              ],
              "cols": [
                {
                  "type": "number",
                  "id": "num_answers",
                  "label": "Number of Answers"
                },
                {
                  "type": "string",
                  "id": "option",
                  "label": "Option"
                }
              ]
            },
            "question": {
              "text": "Are you currently working?",
              "node_id": 400052,
              "question_id": 1046
            }
        }

        """
        request_body = JSONParser.to_collection(self.request.body)
        answer = request_body["answer"]
        ans_type = int(request_body["answer_type"])

        dto = self._question_srv.add_answer(user_id, answer, ans_type)
        self.success(dto)


@Deprecated(20130201)
@Route("/2/questions/answer/get/(?P<answer_id>[-\w]+).json")
class AnswerHandlerV2(BaseQuestionsHandlerV2):
    """
    """

    def get(self, answer_id):
        """
        Returns the answer `answer_id`.

        Respose::

            {
                "answer": "An answer_dto",
                "question": "A question_dto"
            }

        """
        try:
            user_id = self.get_argument("user_id")
            #answer_id = int(answer_id)
            result = self._question_srv.get_answer_by_id(user_id, answer_id)
            self.success("", result)

        except Exception, e:
            self._logger.exception("")
            self.error(str(e))


@Deprecated(20130201)
@Route("/2/questions/answer/edit.json")
class AnswerHandler2V2(BaseQuestionsHandlerV2):
    """
    """

    def post(self):
        """
        Edit an answer and returns stats

        Request::

            {
                "answer": {
                    "execute_time": "2012-03-01 12:13:01 -0300",
                    "answer_value": "2 unit",
                    "question_id": 40,
                    "answer_id": 3
                },
                "user_id": "8MPLXE",
                "answer_type": "1"
            }

        Response::

            {
                "question": {
                    "quesiton_id": 40,
                    "text": "How many cigarettes a day do you smoke?",
                    "node_id": 241559
                },
                "answer": {
                    "execute_time": "2012-03-01 12:13:01 -0300",
                    "answer_value": "2 unit",
                    "question_id": 40,
                    "answer_id": 3
                },
                "stat": "#google format"
            }
        """

        try:
            request_body = JSONParser.to_collection(self.request.body)
            user_id = request_body["user_id"]
            answer = request_body["answer"]
            ans_type = int(request_body["answer_type"])

            result = self._question_srv.edit_answer(user_id, answer, ans_type)
            self.success("", result)

        except Exception, e:
            self._logger.exception("")
            self.error(str(e))


@Deprecated(20130201)
@Route("/2/questions/answer/remove.json")
class RemoveAnswerHandlerV2(BaseQuestionsHandlerV2):
    """
    """

    def post(self):
        """
        Remove an answer and returns stats

        Request::

            {
                "user_id": "8MPLXE",
                "answer_id": 3,
            }

        """

        try:
            request_body = JSONParser.to_collection(self.request.body)
            user_id = request_body["user_id"]
            answer_id = request_body["answer_id"]

            self._question_srv.remove_answer(user_id, answer_id)
            self.success("")

        except Exception, e:
            self._logger.exception("")
            self.error(str(e))



@Route("/3/questions/answers/(?P<answer_id>[-\w]+)")
class AnswersHandler(BaseQuestionsHandler):
    """
    """

    @authenticated
    @catch_exceptions
    def get(self, user_id, answer_id):
        """
        Returns the answer `answer_id`.

        Respose::

            {
                "answer": "An answer_dto",
                "question": "A question_dto"
            }

        """
        dto = self._question_srv.get_answer_by_id(user_id, answer_id)
        self.success(dto)

    @authenticated
    @catch_exceptions
    def put(self, user_id, answer_id):
        """
        Edit an answer and returns stats

        Request::

            {
                "answer": {
                    "execute_time": "2012-03-01 12:13:01 -0300",
                    "answer_value": "2 unit",
                    "question_id": 40,
                    "answer_id": 3
                },
                "user_id": "8MPLXE",
                "answer_type": "1"
            }

        Response::

            {
                "question": {
                    "quesiton_id": 40,
                    "text": "How many cigarettes a day do you smoke?",
                    "node_id": 241559
                },
                "answer": {
                    "execute_time": "2012-03-01 12:13:01 -0300",
                    "answer_value": "2 unit",
                    "question_id": 40,
                    "answer_id": 3
                },
                "stat": "#google format"
            }
        """

        request_body = JSONParser.to_collection(self.request.body)
        answer = request_body["answer"]
        ans_type = int(request_body["answer_type"])

        dto = self._question_srv.edit_answer(user_id, answer, ans_type)
        self.success(dto)

    @authenticated
    @catch_exceptions
    def delete(self, user_id, answer_id):
        """
        """
        self._question_srv.remove_answer(user_id, answer_id)
        self.success()


@Deprecated(20130201)
@Route("/2/questions/stats/tag/(?P<tag>[-\w]+)")
@Route("/2/questions/stats/tag/(?P<tag>[-\w]+).json")
class QuestionStatsByTagHandlerV2(BaseQuestionsHandlerV2):
    """
    """

    def get(self, tag):
        """
        Returns all questions which match a certain tag.

        :rtype: A list of :ref:`question`

        Response::

            {
              "status": "OK",
              "message": "",
              "data": [
                {
                  "answer": {
                    "log_id": 378769,
                    "answer_value": "Yes",
                    "execute_time": "2012-06-29 00:55:48 -0300",
                    "question_id": 1003,
                    "answer_id": 1406
                  },
                  "stat": {
                    "p": {
                      "stats_name": "Do you wash your hands before eating?",
                      "users_count": "30"
                    },
                    "rows": [
                      {
                        "c": [
                          {
                            "v": "20"
                          },
                          {
                            "v": "Yes"
                          }
                        ]
                      },
                      {
                        "c": [
                          {
                            "v": "4"
                          },
                          {
                            "v": "Sometimes"
                          }
                        ]
                      },
                      {
                        "c": [
                          {
                            "v": "6"
                          },
                          {
                            "v": "No"
                          }
                        ]
                      }
                    ],
                    "cols": [
                      {
                        "type": "number",
                        "id": "num_answers",
                        "label": "Number of Answers"
                      },
                      {
                        "type": "string",
                        "id": "option",
                        "label": "Option"
                      }
                    ]
                  },
                  "question": {
                    "text": "Do you wash your hands before eating?",
                    "node_id": 400002,
                    "question_id": 1003
                  }
                },
                {
                  "answer": {
                    "log_id": 0,
                    "answer_value": "",
                    "execute_time": "2012-06-29 12:58:41 -0300",
                    "question_id": 1004,
                    "answer_id": 1411
                  },
                  "stat": {
                    "p": {
                      "stats_name": "Do you consider yourself a morning person or a night person?",
                      "users_count": "21"
                    },
                    "rows": [
                      {
                        "c": [
                          {
                            "v": "4"
                          },
                          {
                            "v": "Night"
                          }
                        ]
                      },
                      {
                        "c": [
                          {
                            "v": "17"
                          },
                          {
                            "v": "Morning"
                          }
                        ]
                      }
                    ],
                    "cols": [
                      {
                        "type": "number",
                        "id": "num_answers",
                        "label": "Number of Answers"
                      },
                      {
                        "type": "string",
                        "id": "option",
                        "label": "Option"
                      }
                    ]
                  },
                  "question": {
                    "text": "Do you consider yourself a morning person or a night person?",
                    "node_id": 400003,
                    "question_id": 1004
                  }
                }
              ]
            }

        """
        try:
            user_id = self.get_argument("user_id")
            user_stats = self._question_srv.get_stats_by_tag(tag, user_id)
            self.success("", user_stats)

        except Exception, e:
            self._logger.exception("")
            self.error(str(e))


@Route("/3/questions/stats/tag/(?P<tag>[-\w]+)")
class QuestionStatsByTagHandler(BaseQuestionsHandler):
    """
    """

    @authenticated
    @catch_exceptions
    def get(self, user_id, tag):
        """
        Returns all questions which match a certain tag.

        :rtype: A list of :ref:`question`

        Response::

          [
            {
              "answer": {
                "log_id": 378769,
                "answer_value": "Yes",
                "execute_time": "2012-06-29 00:55:48 -0300",
                "question_id": 1003,
                "answer_id": 1406
              },
              "stat": {
                "p": {
                  "stats_name": "Do you wash your hands before eating?",
                  "users_count": "30"
                },
                "rows": [
                  {
                    "c": [
                      {
                        "v": "20"
                      },
                      {
                        "v": "Yes"
                      }
                    ]
                  },
                  {
                    "c": [
                      {
                        "v": "4"
                      },
                      {
                        "v": "Sometimes"
                      }
                    ]
                  },
                  {
                    "c": [
                      {
                        "v": "6"
                      },
                      {
                        "v": "No"
                      }
                    ]
                  }
                ],
                "cols": [
                  {
                    "type": "number",
                    "id": "num_answers",
                    "label": "Number of Answers"
                  },
                  {
                    "type": "string",
                    "id": "option",
                    "label": "Option"
                  }
                ]
              },
              "question": {
                "text": "Do you wash your hands before eating?",
                "node_id": 400002,
                "question_id": 1003
              }
            },
            {
              "answer": {
                "log_id": 0,
                "answer_value": "",
                "execute_time": "2012-06-29 12:58:41 -0300",
                "question_id": 1004,
                "answer_id": 1411
              },
              "stat": {
                "p": {
                  "stats_name": "Do you consider yourself a morning person or a night person?",
                  "users_count": "21"
                },
                "rows": [
                  {
                    "c": [
                      {
                        "v": "4"
                      },
                      {
                        "v": "Night"
                      }
                    ]
                  },
                  {
                    "c": [
                      {
                        "v": "17"
                      },
                      {
                        "v": "Morning"
                      }
                    ]
                  }
                ],
                "cols": [
                  {
                    "type": "number",
                    "id": "num_answers",
                    "label": "Number of Answers"
                  },
                  {
                    "type": "string",
                    "id": "option",
                    "label": "Option"
                  }
                ]
              },
              "question": {
                "text": "Do you consider yourself a morning person or a night person?",
                "node_id": 400003,
                "question_id": 1004
              }
            }
          ]

        """
        user_stats = self._question_srv.get_stats_by_tag(tag, user_id)
        self.success(user_stats)


@Deprecated(20130201)
@Route("/2/questions/stats/question/(?P<question_id>[-\w]+)")
@Route("/2/questions/stats/question/(?P<question_id>[-\w]+).json")
class QuestionStatsByQuestionHandlerV2(BaseQuestionsHandlerV2):
    """
    :param user_id: The user for whom the stats are returned.

    Response::

            {
                "question": {
                    "quesiton_id": 40,
                    "text": "How many cigarettes a day do you smoke?",
                    "node_id": 241559
                },
                "stat": "#google format"
            }
    """

    def get(self, question_id):
        try:
            user_id = self.get_argument("user_id")
            question_id = int(question_id)
            user_stats = self._question_srv.get_stats_by_question(user_id, question_id)
            self.success("", user_stats)

        except Exception, e:
            self._logger.exception("")
            self.error(str(e))


@Route("/3/questions/stats/question/(?P<question_id>[-\w]+)")
class QuestionStatsByQuestionHandler(BaseQuestionsHandler):
    """
    :param user_id: The user for whom the stats are returned.

    Response::

            {
                "question": {
                    "quesiton_id": 40,
                    "text": "How many cigarettes a day do you smoke?",
                    "node_id": 241559
                },
                "stat": "#google format"
            }
    """
    
    @authenticated
    @catch_exceptions
    def get(self, user_id, question_id):
        question_id = int(question_id)
        user_stats = self._question_srv.get_stats_by_question(user_id, question_id)
        self.success(user_stats)


routes = Route.get_routes()
