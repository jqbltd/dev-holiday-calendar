# Dev Holiday Calendar

A script that will copy the dev's holidays from the main JQB calendar to a dev only calendar.

## Setup

Go to https://console.developers.google.com/apis/credentials with a Google account and click on `Create Credentials`. Select `OAuth client ID` And pick the application type as `Desktop app`. Download the newly created credentials file and place it in the project directory, named as `credentials.json`.

Use `example.config.json` as a template to create a `config.json` file in the project directory. The calendar IDs can be found on the Google Calendar's settings. `holiday` is the main JQB calednar and `dev` is the dev only calendar. Look at the main holiday calendar to see how names are displayed.

Install the pip requirements.

When first running `update_calendar.py` you will have to authorise the app. It will create a `token.pickle` file.
