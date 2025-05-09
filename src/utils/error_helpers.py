'''Helper functions for the Discord Codeforces Verification Bot.'''
import string
import random
import logging
from typing import Optional
import discord
from datetime import datetime

logger = logging.getLogger(__name__)



def format_error_message(error: Exception) -> str:
    error_type = type(error).__name__
    error_msg = str(error)
    logger.error(f'{error_type}: {error_msg}')
    
    if isinstance(error, discord.errors.Forbidden):
        return 'I don\'t have permission to perform this action'
    elif isinstance(error, discord.errors.HTTPException):
        return 'Discord API error occurred. Please try again later'
    else:
        return 'An unexpected error occurred. Please try again later' 