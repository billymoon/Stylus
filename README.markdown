# Stylus Package for Sublime Text 2/3

Includes build system and syntax highlighting for Stylus language.

## Requirements

In order for build system to work you will need [stylus](http://learnboost.github.io/stylus/) installed via [npm](http://nodejs.org/) and available in your `PATH`.

## Install

The easiest way to install this is with [Package Control](http://wbond.net/sublime\_packages/package\_control).

 * Bring up the Command Palette (Command+Shift+p on OS X, Control+Shift+p on Linux/Windows).
 * Select "Package Control: Install Package" (it'll take a few seconds)
 * Select Stylus when the list appears.

Package Control will automatically keep the package up to date with the latest version.

## Issues & Feature Request

Please use [GitHub Issue Tracker](https://github.com/billymoon/Stylus/issues) to report any bugs and make feature requests.

## Development

If you want to help developing this package you will need [grunt](http://gruntjs.com/) installed to be able to recompile language definition from `.yml` source by navigating to a folder contain this package in terminal and typing:

    grunt watch
