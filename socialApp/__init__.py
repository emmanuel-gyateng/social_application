"""Importing celery application and making it available in the application"""
from .celery import app as celery_app 

__all__ = ('celery_app',)

