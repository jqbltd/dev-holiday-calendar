# Dev Holiday Calendar

A script that will get copy the dev's holidays from the main JQB calendar to a dev only calendar.

## Setup

Go to: https://developers.google.com/calendar/quickstart/python and click on `Enable the Google Calendar API` to get a desktop app `credentials.json` file.

Use the `example.config.json` as a template to make a `config.json` file. The Calendar IDs can be found on the calendar's settings. `holiday` is the main JQB calednar and `dev` is the dev only calendar. Look at the main holiday calendar to see how names are displayed.

Both the `credentials.json` and `config.json` files should be in the project directory.

Install the pip requirements.

When first running `update_calendar.py` you will have to authorise the app. It will create a `token.pickle` file.