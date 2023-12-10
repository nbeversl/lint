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
		self._get_settings()		
		contents = self.project.run_editor_method('get_buffer')
		contents = '\n'.join(l for l in contents.split('\n') if l.strip())
		if contents:
			buffer = self.project._parse_file(
				filename,
				buffer_contents=contents)
			self._get_settings() # in case buffer is project_settings
			if not buffer:
				return
			mapped_ranges = {}
			for node in buffer.nodes:
				for r in node.ranges:
					if node.nested > 0 and not node.is_meta:
						if r == node.ranges[0]: # first range
							if node.compact:
								r[0] = r[0] - 2 
							else:
								r[0] = r[0] - 1
							whitespace = (len(contents[r[0]+1:r[1]]) - len(contents[r[0]+1:r[1]].lstrip())) + 1
						if r == node.ranges[-1]: # last range
							if not node.compact:
								r[1] = r[1] + 1
					else:
						whitespace = 0
					mapped_ranges[r[0]] = {
						'range' : r,
						'whitespace' : whitespace,
						'nested' : node.nested,
						'start' : r == node.ranges[0] and (node.nested > 0),
						'is_meta' : node.is_meta,
						'end' : r == node.ranges[-1] and (node.nested > 0)
					}
			new_contents = []
			range_start_positions = sorted(list(mapped_ranges.keys()))
			for position in range_start_positions:
				r = mapped_ranges[position]
				if not r['is_meta']:
					range_contents = contents[r['range'][0]:r['range'][1]]
					range_lines = [l.strip() for l in range_contents.split('\n')]
					if range_lines:
						whitespace = '\t' * r['nested']
						whitespace += ' ' * r['whitespace']
						whitespace_index = 0
						if r['start'] or r['end']:
							spaces = 1
							if self.settings:
								spaces = self.settings.get_first_value(
									'space_between_nodes')
								if spaces:
									spaces = int(spaces.num())
								else: 
									spaces = 1
							range_lines[0] = '\t' * r['nested'] + range_lines[0]
							whitespace_index = 1
						if len(range_lines) > 1:
							range_lines[whitespace_index:] = [
								whitespace + l for l in range_lines[whitespace_index:]]
					new_contents.append('\n'.join(range_lines))
				else:
					new_contents.append(
						contents[r['range'][0]-2:r['range'][1]+1]
						)
			new_contents = ''.join(new_contents)
			buffer._set_contents(new_contents)

urtext_extensions = [UrtextLint]