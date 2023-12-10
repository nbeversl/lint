class UrtextLint:

	name = ["LINT"]

	def run(self, filename):
		contents = self.project.run_editor_method('get_buffer')
		if contents:
			buffer = self.project.urtext_buffer(
				self.project,
				filename,
				contents)
			buffer.lex_and_parse()
			mapped_ranges = {}
			for node in buffer.nodes:
				for r in node.ranges:
					if node.nested > 0:
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
						'start' : r == node.ranges[0] and node.nested > 0
					}
			new_contents = []
			range_start_positions = sorted(list(mapped_ranges.keys()))
			for position in range_start_positions:
				r = mapped_ranges[position]
				range_contents = contents[r['range'][0]:r['range'][1]]
				range_lines = [l.strip() for l in range_contents.split('\n') if l.strip()]
				if range_lines:
					whitespace = '\t' * r['nested']
					whitespace += ' ' * r['whitespace']
					whitespace_index = 0
					if r['start']:
						range_lines[0] = '\t' * r['nested'] + range_lines[0]
						whitespace_index = 1
					if len(range_lines) > 1:
						range_lines[whitespace_index:] = [whitespace + l for l in range_lines[whitespace_index:]]
					new_contents.extend(range_lines)
				# print([whitespace + l for l in range_lines])
			new_contents = '\n'.join(new_contents)
			buffer._set_contents(new_contents)

urtext_extensions = [UrtextLint]