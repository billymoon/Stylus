# Stylus Package for Sublime Text 2/3

Includes build system and syntax highlighting for [stylus](http://learnboost.github.io/stylus/) CSS preprocessor.

## Notice to existing users

In order to provide better integration with [Emmet](https://sublime.wbond.net/packages/Emmet) and [Hayaku](https://sublime.wbond.net/packages/Hayaku%20-%20tools%20for%20writing%20CSS%20faster) packages that allow dynamic expansion of CSS properties, snippets that were previously a part of this package are now distrubited separately as new package called [Sublime-Snippets](https://github.com/billymoon/Stylus-Snippets) (available via [Package Control](https://sublime.wbond.net/)).

## Requirements

In order for build system to work you will need [stylus](http://learnboost.github.io/stylus/) installed via [npm](http://nodejs.org/) and available in your `PATH`.

## Install

The easiest way to install this is with [Package Control](https://sublime.wbond.net/).

 * Bring up the Command Palette (Command+Shift+p on OS X, Control+Shift+p on Linux/Windows).
 * Select "Package Control: Install Package" (it'll take a few seconds)
 * Select Stylus when the list appears.

Package Control will automatically keep the package up to date with the latest version.

# Settings

Go to `Preferences > Package Settings > Stylus > Settings - User` to change settings.

You can set paths to the stylus binary, and other plugin settings including `compileOnSave` which is off by default, `compress` and output paths.

Full details in the comments in `Preferences > Package Settings > Stylus > Settings - Default`

## Project settings

Go to `Project > Edit Project` to change project settings.

```Javascript
{
    "folders":
    [
        ...
    ],
    "settings":
    {
        "Stylus":
        {
            "compress": false,
            "compileOnSave": true,
            "compileDir": "out"
        }
    }
}
```

## Issues & Feature Requests

Please use [GitHub Issue Tracker](https://github.com/billymoon/Stylus/issues) to report any bugs and make feature requests.

## Maintainers

 * [Billy Moon](https://github.com/billymoon) ([billy@itaccess.org](mailto:billy@itaccess.org))
 * [Dmitriy Kubyshkin](https://github.com/grassator) ([dmitriy@kubyshkin.name](mailto:dmitriy@kubyshkin.name))

## Thanks

 * [Logan Howlett](https://github.com/aponxi) The compileOnSave, Python script and settings file have been forked from [aponxi](https://github.com/aponxi/sublime-better-coffeescript)

## Development

If you want to help developing this package you will need [grunt](http://gruntjs.com/) installed to be able to recompile language definition from `.yml` source by navigating to a folder contain this package in terminal and typing:

    grunt watch

## Licensing

Licensed under permissive [MIT-style license](https://github.com/billymoon/Stylus/blob/master/LICENSE).
