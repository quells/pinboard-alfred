Pinboard in Alfred 2
====================

A Python script to display Pinboard bookmarks in the Alfred window. You will need Alfred 2 and a regular Pinboard account to use this.

# Download

[Pinboard workflow](https://github.com/quells/pinboard-alfred2/blob/master/Pinboard.alfredworkflow?raw=true)

# Installation

To install the [Pinboard workflow](https://github.com/quells/pinboard-alfred2/blob/master/Pinboard.alfredworkflow?raw=true), double click on ```Pinboard.alfredworkflow``` or drag the workflow to the workflow window in Alfred.

Find your API token on the [Pinboard settings page](https://pinboard.in/settings/password).

Next, edit the script filter by double clicking on it. Edit the line ```print list("TOKEN", 3600, "{query}")``` to fill in your API token and caching preference. The default value of 3600 means that the script will only try to cache your bookmarks if it has not done so in the last hour (3600 seconds). A value of 0 means that the script will never write to disk.

# How to use

Simply type ```pinb``` (or whatever you configure) into Alfred. If your bookmarks are cached, they should appear in Alfred almost immediately. If not, downloading from the Pinboard server could take some time.

Hitting ```enter``` while a bookmark is selected will open the URL associated with that bookmark in Safari. Holding ```alt``` while doing this will open the URL in Google Chrome.

To filter the results, add your query after a space. For example, ```pinb apple``` will only display results with ```apple``` in the title, description, or tags of the bookmark. This is case insensitive and is compatible with regular expression syntax, if you’re into that. The first result will open the Pinboard search page with the results of the query.

# Disclaimers

This script and associated Alfred workflow is released under the [MIT license](https://github.com/quells/pinboard-alfred2/blob/master/LICENSE).

The Pinboard name and logo are owned by Nine Fives Software. Kai Wells does not own or claim to own anything related to Pinboard.

# Version History

## 1.0 - November 21, 2013

- Initial release