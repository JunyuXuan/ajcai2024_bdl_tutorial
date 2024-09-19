import os
import json
import codecs
from shutil import copyfile

# from colorthief import ColorThief

# Parse the string at the top of the data file and parse the formatting rules.
# Starts from line 3.
def get_formatting_rules(s):
	lines = s.split("\n")
	formatting_rules = []
	print(lines)
	for line in lines[2:]:
		print(line)
		line = line.split("# ")[1].strip()
		field = line.split(" ")[0]
		optional = "(optional)" in line
		formatting_rules.append({ "field": field, "optional": optional})
	return formatting_rules

# Determine whether the given line adheres to the given formatting rule.
def line_adheres_to_field_rule(line, field):
	if field == "project_title":
		return not line.startswith("http")
	if field == "uwa_profile":
		return line.startswith("https://research-repository.uwa.edu.au")
	if field == "linkedin_profile":
		return line.startswith("https://www.linkedin.com")
	if field == "website":
		return not line.startswith("https://research-repository.uwa.edu.au") and \
			   not line.startswith("https://www.linkedin.com") and \
			       line.startswith("http")
	if field == "image_filename":
		return line.endswith('.jpg') or line.endswith('.png')
	return True

# Parse an item in the data file, checking whether it adheres to the formatting rules of that file (specified at the top).
# should_group_images specifies whether images and image descriptions should be grouped into a list.
def parse_item(item, formatting_rules, should_group_images):
	required_num_lines = sum([1 for x in formatting_rules if not x['optional']])
	lines = item.split('\n')
	if len(lines) < required_num_lines:
		raise Exception("Error with item:\n%s\n\nItem must have at least 2 lines.")
	parsed_item = {}

	rule_index = 0
	line_index = 0

	while line_index < len(lines):

		line = lines[line_index]		

		current_rule = formatting_rules[rule_index]

		field    = current_rule["field"]
		optional = current_rule["optional"]

		#print(line, field, line_index, rule_index, line_adheres_to_field_rule(line, field))

		# If optional, check whether this line matches the rule
		if not optional or (optional and line_adheres_to_field_rule(line, field)):

			if field == "image_filename":
				#line = os.path.join(*line.split('/'))
				if not os.path.exists(os.path.join('page_data', 'images', os.path.join(*line.split('/')))):
					raise Exception("Image filename does not exist: %s" % line)

			if field == "image_filename" and should_group_images:
				if "images" not in parsed_item.keys():
					parsed_item["images"] = []
				parsed_item["images"].append({"image_filename": line})
			elif field == "image_description" and should_group_images:
				if "images" not in parsed_item.keys():
					raise Exception("Image description must follow an image filename")
				parsed_item["images"][-1]["image_description"] = line
			else:
				parsed_item[field] = line
			line_index += 1		
			rule_index += 1	



		else:
				rule_index += 1
		# else:

		# 	if field == "image_filename":
		# 			line = os.path.join(*line.split('/'))
		# 			if not os.path.exists(os.path.join('page_data', 'images', line)):
		# 				raise Exception("Image filename does not exist: %s" % line)

		# 	parsed_item[field] = line
		# 	line_index += 1
		# 	rule_index += 1

	return parsed_item


# Parse a data file, reading its formatting rules (at the top), and then converting it to JSON.
def parse_file(filename):
	groups = []
	file_json = []
	current_group = None
	should_group_images = True if filename.endswith("news.txt") else False 

	print("Parsing file %s" % filename)

	# Maintain a list of image filenames so they can be copied over into the public folder after parsing
	image_filenames = []

	with codecs.open(filename, 'r', 'utf-8') as f:

		_f = f.read().replace('\r', '')
		parts = _f.split('\n\n')
		formatting_rules = get_formatting_rules(parts[0])

		# Items may either be grouped, or not grouped.
		# This is specified by including [Group] lines in the file, which determine the group of
		# subsequent items.
		group_items = {}
		grouped = False
		for part in parts[1:]:
			if part.startswith('[') and part.endswith(']') and "\n" not in part:
				grouped = True	
		
		# If no [Group] line is present, create a group called "(Ungrouped)" and put the items in there.
		if not grouped:
			group_name = "(Ungrouped)"
			group_items["(Ungrouped)"] = []
			groups.append(group_name)

		for part in parts[1:]:	

			if len(part.strip()) == 0:
				continue

			if part.startswith('[') and part.endswith(']') and "\n" not in part:
				group_name = part[1:-1]
				if group_name in groups:
					raise Exception("Group %s appears more than once." % group_name)
				groups.append(group_name)
				group_items[group_name] = []
				current_group = group_name
			else:
				if current_group is None and grouped:
					raise Exception("First line must be a group.")

				item = parse_item(part, formatting_rules, should_group_images)
				if "image_filename" in item.keys():
					image_filenames.append(item['image_filename'])
									
					# color_thief = ColorThief(os.path.join('page_data', 'images', item['image_filename']))
					# dominant_colour = color_thief.get_color(quality=1)
					# item['dominant_colour'] = dominant_colour


				group_items[group_name].append(item)

	for group in groups:
		file_json.append({
			"group": group,
			"items": group_items[group],
		})
	return file_json, image_filenames


def save_json(file_json, data_name, filename):
	with codecs.open(filename[:-4] + '.js', 'w', 'utf-8') as f:
		f.write('const %s = ' % data_name)
		json.dump(file_json, f, indent=3)
		f.write('\nexport default %s' % data_name)

def copy_images(image_filenames, folder):
	if len(image_filenames) == 0:
		return
	output_folder = os.path.join('public', 'images', folder)
	if not os.path.exists(output_folder):
		os.mkdir(output_folder)
	for filename in image_filenames:
		src = os.path.join("page_data", "images", filename)
		dest = os.path.join("public", "images", filename)
		copyfile(src, dest)
		print("Copied %s to %s" % (src, dest))

def main():

	input_folder = "page_data"
	output_folder = os.path.join("src", "page_data")

	for filename in os.listdir(input_folder):
		if not filename.endswith('.txt'):
			continue
		file_json, image_filenames = parse_file(os.path.join(input_folder, filename))
		save_json(file_json, filename[:-4], os.path.join(output_folder, filename))
		copy_images(image_filenames, filename.split('.txt')[0])


	pass 

if __name__ == "__main__":	
	main()