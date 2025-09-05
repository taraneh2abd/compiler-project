from plantuml import PlantUML

server = PlantUML(url='http://www.plantuml.com/plantuml/img/')

puml_content = """
@startuml
skinparam fontcolor blue
skinparam backgroundcolor lightyellow
skinparam classFontSize 14
skinparam classBorderColor black

class A {
  +A()
}
@enduml
"""

# write PUML content to a temporary file
with open("temp_diagram.puml", "w") as f:
    f.write(puml_content)

# generate PNG
server.processes_file(filename="temp_diagram.puml", outfile="yas_theme2.png")

print("Diagram generated: yas_theme2.png")
