import os.path
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TOKEN_PICKLE_PATH = os.path.join(DIR_PATH, 'token.pickle')
CREDENTIALS_PATH = os.path.join(DIR_PATH, 'credentials.json')


if __name__ == '__main__':
    flow = InstalledAppFlow.from_client_secrets_file(
        CREDENTIALS_PATH,
        ['https://www.googleapis.com/auth/calendar.events']
    )
    credentials = flow.run_console()

    with open(TOKEN_PICKLE_PATH, 'wb') as f:
        pickle.dump(credentials, f)
