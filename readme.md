# Lint extension for Urtext

## Activation

### Urtext (https://github.com/nbeversl/urtext)

Put `Lint.urtext` into any project.

## Settings

Add a `_lint` key to a `project_settings` node, with a node as the value. 
- `run_when_file_modified` : If true ("true", "yes", "y"), will run lint after saving/modifiying any file. Default: false.
- `lines_between_nodes` : A number. Sets the number of spaces between bracket nodes. Default: 1
- `left_padding` : Number of spaces to left pad

**Example:**

	project_settings _
	_lint::{ 
		run_when_file_modified::yes
		lines_between_nodes::1
	}

## Manual Trigger (Sublime Text) (https://github.com/nbeversl/urtext_sublime)

Put `sublime_urtext_lint.py` into the root of your Urtext package folder. You will then need to key bind it in one the `.sublime-keymap` files for your OS.

Example:
`[
 	{ "keys": ["ctrl+shift+k"], "command":"urtext_lint"}
]`

## Other Implementations

`UrtextProjectList.current_project.run_directive('LINT', self.view.file_name())`


