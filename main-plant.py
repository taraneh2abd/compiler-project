from plantuml import PlantUML
import os

input_file = r'code_examples\Equivalent-usecasediag.puml'
output_folder = 'plantuml-results'
os.makedirs(output_folder, exist_ok=True)

with open(input_file, 'r') as f:
    plantuml_code = f.read()

server = PlantUML(url='http://www.plantuml.com/plantuml/img/') 

output_path = os.path.join(output_folder, 'Equivalent-usecasediag.png')

server.processes_file(input_file, output_path)
