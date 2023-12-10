# Lint extension for Urtext

## Installation

### Urtext (https://github.com/nbeversl/urtext)

Extensions are read automatically from any folder in the library extensions folder or any folder in the `extensions` key in `project_settings`. Put `lint.py` in any included folder.

### Sublime Text (https://github.com/nbeversl/urtext_sublime)

Put `sublime_urtext_lint.py` into the root of your Urtext package folder. You will then need to key bind it in one the `.sublime-keymap` files for your OS.

Example:
`[
 	{ "keys": ["ctrl+shift+k"], "command":"urtext_lint"}
]`

### Other Implementations

`UrtextProjectList.current_project.extensions['LINT'].run([filename])`
