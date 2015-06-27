#slack-mbta

This repository contains a Slack plugin for the MBTA.

###Setup
To set it up, you must do a few things:
1. Edit the final line in main.py to bind an IP and port: `app.run(port=8080,ip='127.0.0.1')`
2. Create a few slash command integrations:
    1. /bus [number] -> GET to https://<hostname>:<port>/bus/[number]
    2. /alert [route] -> GET to https://<hostname>:<port>/alert/[route]
    3. /alerts -> GET to https://<hostname>:<port>/alerts
3. Install the egg (dependencies) by running python setup.py install
4. Run the deployment script and answer the questions: `bash deploy`
5. Run your app: `/etc/init.d/slack-mbta`

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
