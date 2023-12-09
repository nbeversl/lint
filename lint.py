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
			all_ranges = []
			for node in buffer.nodes:
				mapped_ranges.setdefault(node.nested, [])
				ranges = node.ranges
				for r in ranges:
					if node.nested > 0:
						if r == ranges[0]: # first range
							if node.compact:
								r[0] = r[0] - 2 
							else:
								r[0] = r[0] - 1
						if r == ranges[-1]: # last range
							if not node.compact:
								r[1] = r[1] + 1
					mapped_ranges[node.nested].append(r)
					all_ranges.append(r)
			new_contents = []
			all_ranges = sorted(
				all_ranges,
				key = lambda r : r[0])
			for r in all_ranges:
				for nested in mapped_ranges:
					if r in mapped_ranges[nested]:
						break
				range_contents = contents[r[0]:r[1]]
				range_lines = [l.strip() for l in range_contents.split('\n') if l.strip()]
				new_contents.extend(['\t' * nested + l for l in range_lines] )
			new_contents = '\n'.join(new_contents)
			buffer._set_contents(new_contents)

urtext_extensions = [UrtextLint]