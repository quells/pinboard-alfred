Pinboard in Alfred
==================

A Python script to display Pinboard bookmarks in the Alfred window. You will need Alfred 5 and a regular Pinboard account to use this.

v1 of this workflow is still available for older versions of Alfred, but requires Python 2 and is no longer actively supported.

# Download

[Pinboard workflow](https://github.com/quells/pinboard-alfred/blob/master/Pinboard%20v2.alfredworkflow?raw=true)

# Installation

Find your API token on the [Pinboard settings page](https://pinboard.in/settings/password).

Download the [workflow](https://github.com/quells/pinboard-alfred/blob/master/Pinboard%20v2.alfredworkflow?raw=true) and double click on ```Pinboard v2.alfredworkflow``` or drag the workflow to the workflow window in Alfred.

Information about the workflow will be displayed. Paste your Pinboard API token into the field on the left.

# How to use

Type `pinb` into Alfred. If your bookmarks are cached, they should appear in Alfred almost immediately. If not, downloading from the Pinboard server could take some time.

To filter the results, add your query after a space. For example, `pinb apple` will only display results with "apple" in the title, description, tags, or URL of the bookmark. This is case insensitive.

Hitting `enter` while a bookmark is selected will open the URL for that bookmark in your default Web Browser.

# Disclaimers

This script and associated Alfred workflow is released under the [MIT license](https://github.com/quells/pinboard-alfred/blob/master/LICENSE).

This workflow is not endorsed by the Pinboard service or Nine Fives Software. The Pinboard name and logo are owned by Nine Fives Software. Kai Wells does not own or claim to own anything related to Pinboard.

# Version History

## 2.0.0 - August 13, 2022

- Updated for Alfred 5 workflows
- Rewrote script for Python 3
- Local cache is stored in a sqlite database instead of a text file
- Uses JSON for Alfred formatting instead of XML

## 1.0 - November 21, 2013

- Initial release
