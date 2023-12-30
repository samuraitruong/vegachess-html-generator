from flag import get_fed_icon
from jinja2 import Environment, FileSystemLoader
import json;
import os
import shutil

def apply_template(name, data, output):
    """
    Apply a Jinja2 template to data and write the result to an output file.

    Parameters:
    - name (str): File name of the template.
    - data (dict): Dictionary containing data to be used for templating.
    - output (str): Output file name to write the templated content.
    """

    # Render the template with the provided data.
    rendered_content = get_template_str(name, data)
    # Write the rendered content to the output file.
    with open(output, 'w') as file:
        file.write(rendered_content)

    with open(output.replace('html', 'json'), 'w') as file:
        file.write(json.dumps(data, indent=2))

def get_template_str(filename, data):
    # Set up Jinja2 environment with the current directory as the loader path.
    # You can modify this path based on where your template is located.
    file_loader = FileSystemLoader('.')
    env = Environment(loader=file_loader)

    # Load the template using the provided name.
    template = env.get_template(filename)

    # Render the template with the provided data.
    rendered_content = template.render(data)

    return rendered_content

def output_standings_page(data, out_dir):
    source = 'templates/standings.html'
    cloned_data = update_data_with_flag(data, ['Fed'])
    apply_template(source, cloned_data, f"{out_dir}/standings.html")

def update_data_with_flag(data, fed_fields):
    cloned_data = {**data}

    for r in cloned_data['rows']:
        for f in fed_fields:
            r[f] = f'<img src="{get_fed_icon(r[f])}" width="27"/>'

    return cloned_data

def output_players_page(data, out_dir):
    source = 'templates/players.html'
    cloned_data = update_data_with_flag(data, ['Fed'])
    apply_template(source, cloned_data, f"{out_dir}/index.html")
    data['rows'].sort(key=lambda x: x['Name'])
    apply_template(source, cloned_data, f"{out_dir}/playersname.html")
    data['rows'].sort(key=lambda x: x['FRtg'],reverse = True)
    apply_template(source, cloned_data, f"{out_dir}/playersrating.html")


def output_pairings_page(data, out_dir):
    source = 'templates/pairings.html'
    cloned_data = update_data_with_flag(data, ['White Fed', 'Black Fed'])
    apply_template(source, cloned_data, f"{out_dir}/pairs{data['round']}.html")

def output_playercard_page(data, out_dir):
    source = 'templates/playercard.html'
    apply_template(source, data, f"{out_dir}/playercard.html")


def copy_css_and_js(destination_folder):
    # Check if the destination folder exists; if not, create it
   
    source_folder = 'templates'
    # Iterate through all files in the source folder
    for filename in os.listdir(source_folder):
        # Check if the file is either a .css or .js file
        if filename.endswith('.css') or filename.endswith('.js'):
            # Construct the full file path for source and destination
            source_file_path = os.path.join(source_folder, filename)
            destination_file_path = os.path.join(destination_folder, filename)

            # Copy the file from source to destination
            shutil.copy2(source_file_path, destination_file_path)
            print(f"Copied {filename} from {source_folder} to {destination_folder}")

