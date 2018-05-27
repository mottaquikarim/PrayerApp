from os import environ


def get_variables():
    return {
        'google_api_key': environ.get('GOOGLE_API_KEY'),
        'host': 'https://5nzkfjtltl.execute-api.us-east-1.amazonaws.com',
        'stage': 'test'
    }
