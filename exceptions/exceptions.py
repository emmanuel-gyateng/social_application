"""Exception class"""
from rest_framework.exceptions import APIException


class UserNotFound(APIException):
    """Exception for when a user does not exist"""

    status_code = 404
    default_detail = {"status": "failure", "detail": "User does not exist"}


class ProfileNotFound(APIException):
    """Exception for when a profile does not exist"""

    status_code = 404
    default_detail = {"status": "failure", "detail": "User does not exist"}


class InvalidLink(APIException):
    """Invalid link exception"""

    status_code = 400
    default_detail = {"status": "failure", "detail": "link invalid"}


class PostNotFound(APIException):
    """Exception for when a post does not exist"""

    status_code = 400
    default_detail = {"status": "failure", "detail": "post not found"}


class CommentNotFound(APIException):
    """Exception for when a comment does not exist"""

    status_code = 400
    default_detail = {"status": "failure", "detail": "comment not found"}


class GroupNotFound(APIException):
    """Exception for when a group does not exist"""

    status_code = 400
    default_detail = {"status": "failure", "detail": "group not found"}


class GroupMemberNotFound(APIException):
    """Exception for when a Group Member does not exist"""

    status_code = 400
    default_detail = {"status": "failure", "detail": "group member not found"}
