# Ulauncher-calendar
[Ulauncher](https://ulauncher.io/) Calendar plugin to manage 'cal' command directly from ULauncher.
It also integrates Google Calendar. It is needed to configure the plugin to allow this option. This will ask the user for authorize the plugin to retrieve incoming events in google calendar.
## Preview
![default](https://github.com/Carlosmape/ulauncher-calendar/blob/master/images/screenshot_01.png?raw=true)
![with options](https://github.com/Carlosmape/ulauncher-calendar/blob/master/images/screenshot_02.png?raw=true)
![google calendar integration](https://github.com/Carlosmape/ulauncher-calendar/blob/master/images/screenshot_03.png?raw=true)
## Dependencies
- Ulauncher API ^2.0
- `cal` command

For python dependencies see [requirements.txt](https://github.com/Carlosmape/ulauncher-calendar/blob/master/requirements.txt)

## Google Calendar integration
To allow Google Calendar integration, you need to create a Google Calendar Application in [Google Console](https://console.cloud.google.com/welcome?project=ulauncher-calendar) enable Google Calendar API and generate an OAuth 2.0 credentials. Just as you should make for [Google Calendar Development](https://developers.google.com/calendar/) purposes. 

At the end of the process, store generated credentials.json in ~/.local/share/ulauncher/extensions/com.github.carlosmape.ulauncher-calendar/ folder to allow this plugin to read and use your own credentials

Finally go to extension preferences and able Google Calendar integration option
![config screen](https://github.com/Carlosmape/ulauncher-calendar/blob/master/images/preferences.png?raw=true)

Notice that if Google Calendar integration changes to "No" and then to "Yes" (saving coniguration on each value change) The Google Integration will force to reinitialize. It means, if the credentials.json is valid, Google will ask you to allow this plugin integration as in the following sample image:

![config screen](https://github.com/Carlosmape/ulauncher-calendar/blob/master/images/oauth_1.png?raw=true)
![config screen](https://github.com/Carlosmape/ulauncher-calendar/blob/master/images/oauth_2.png?raw=true)
