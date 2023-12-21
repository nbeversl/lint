class UrtextLint:

	name = ["LINT"]

	def __init__(self, project):
		super().__init__(project)
		self._get_settings()

	def _get_settings(self):		
		self.settings = None
		if '_lint' in self.project.settings:
			if self.project.settings['_lint'] and self.project.settings['_lint'].is_node:
				self.settings = self.project.settings['_lint'].metadata

	def on_file_modified(self, filename):
		self._get_settings()
		if self.settings:
			lint_on_file_modified = self.settings.get_first_value(
				'run_when_file_modified')
			if lint_on_file_modified != None:
				if lint_on_file_modified.true():
					self.run(filename)

	def run(self, filename):
		self.project.execute(
			self._run,
			filename)

	def _run(self, filename):
		self._get_settings()		
		contents = self.project.run_editor_method(
			'get_buffer', 
			filename)
		if not contents:
			return
		contents = '\n'.join(l for l in contents.split('\n'))
		if contents:
			buffer = self.project._parse_file(
				filename,
				buffer_contents=contents)
			if not buffer:
				return

			self._get_settings() # in case buffer is a project_settings node

			mapped_ranges = {}
			for node in buffer.nodes:
				whitespace = 0
				for r in node.ranges:
					if node.nested > 0 and not node.is_meta:
						if r == node.ranges[0]:
							if node.compact:
								r[0] = r[0] - 2 
							else:
								r[0] = r[0] - 1
							first_line = contents[r[0]+1:r[1]].split('\n')[0]
							whitespace = (len(first_line) - len(first_line.lstrip())) + 1
						if r == node.ranges[-1]:
							if not node.compact:
								r[1] = r[1] + 1
					mapped_ranges[r[0]] = {
						'range' : r,
						'whitespace' : whitespace,
						'nested' : node.nested,
						'start' : r == node.ranges[0] and (node.nested > 0),
						'is_meta' : node.is_meta,
						'end' : r == node.ranges[-1] and (node.nested > 0)
					}

			spaces_between_nodes = 1
			if self.settings:
				spaces_setting = self.settings.get_first_value('space_between_nodes')
				if spaces_setting:
					spaces_between_nodes = int(spaces_setting.num())

			new_contents = []
			range_start_positions = sorted(list(mapped_ranges.keys()))
			for position in range_start_positions:
				r = mapped_ranges[position]
				if not r['is_meta']: # TODO implement meta nodes
					range_contents = contents[r['range'][0]:r['range'][1]]
					range_lines = [l.strip() for l in range_contents.split('\n')]
					if range_lines:
						tabs = '\t' * r['nested']
						whitespace = ' ' * r['whitespace']
						whitespace_start_index = 0
						if r['start']: # first range
							range_lines[0] = ('\n' * (spaces_between_nodes + 1)) + '\t' * r['nested'] + range_lines[0]
							whitespace_start_index = 1
						if len(range_lines) > 1:
							for index, line in enumerate(range_lines):
								if index >= whitespace_start_index:
									if not range_lines[index].strip():
										range_lines[index] = range_lines[index].strip()
									elif range_lines[index].strip() in ['{','}']:
										range_lines[index] = tabs + range_lines[index]
									else:
										range_lines[index] = tabs + whitespace + range_lines[index].strip()
						for line in reversed(range_lines):
							if line.strip():
								break
							range_lines.pop()
					new_contents.append('\n'.join(range_lines))
				else:
					new_contents.append(
						contents[
						r['range'][0]-2
						:
						r['range'][1]+1])
			new_contents = ''.join(new_contents)
			buffer._set_contents(new_contents)

urtext_extensions = [UrtextLint]