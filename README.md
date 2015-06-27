#slack-mbta

This repository contains a Slack plugin for the MBTA.

###Setup
To set it up, you must do a few things:
- Edit the final line in main.py to bind an IP and port: `app.run(port=8080,ip='127.0.0.1')`
- Create a few slash command integrations:
  - /bus [number] -> GET to https://HOSTNAME:PORT/bus/[number]
  - /alert [route] -> GET to https://HOSTNAME:PORT/alert/[route]
  - /alerts -> GET to https://HOSTNAME:PORT/alerts
- Install the egg (dependencies) by running python setup.py install
- Run the deployment script and answer the questions: `bash deploy`
- Run your app: `/etc/init.d/slack-mbta`

###Debugging
- This logs to `/path/to/slack-mbta/slack-mbta/slack-mbta.log` by default. Specify an alternative by using parameter `-l /path/to/logfile` on startup
- Turn on debugging by using parameter `-d`
- You can also run the app from the route directory if you're having problems, just do `python main.py -d`

###Configuration
- Specify a config file with `-c /path/to/config`. For available configuration parameters READ THE CODE IN `config.py` YOU DUMMY

###Other help
- Email me: daniel.m.fithian@gmail.com
- Read the code and make improvements
- To get other command line arguments, run with parameter `-h`
