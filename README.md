# Language for Creating UML Diagrams

**Authors:**  
- fatemeh abdellahi 
- yasaman haji  
- mahyar niavand  
- shayan moulai

---

## Description of the Language

The goal of our project is to create a simple language for describing basic UML diagrams.  
Our language will be able to describe :
- **AST visualization**  
- **class diagrams**
- **sequence diagrams**
- **use-case diagrams**  
- **State Machine Diagram**  TODO
- **flowchart**  TODO
- **Theme**  TODO

what is point of our compiler?

- Ability to reuse and reference **global objects**, **shared theme** and **functions*** programmatically

- Abstracts diagram generation with logic (functions, variables)
 
- Lets you write diagrams as code with more modularity and **snappshot** in between the codes unlikly to plantuml.

- converting python and cpp code

After entering code, the user will get a generated UML diagram as an image.  

---


## Syntax

### 1. Creating Diagrams

```
diagclass diag_name:
# class diagram declaration

diagseq diag_name:
# sequence diagram declaration

diagusecase diag_name:
# use-case diagram declaration
```
---

### 2. Creating Objects

**Creating a theme that can be assigned to blocks:**
```
theme theme_name:
    fontcolor "red"
    classFontSize "8"
    backgroundcolor "white"
```

**Creating a note:**
```
note theme_name note_name:
    "note content"
    "..."
```

**Creating a package/group:**
```
package theme_name package_name:
    object1
    object2
    ...
```

Access to individual fields of a group is via the `.` operator. Example:
```
package_name.attribute1
```

**Creating connections between objects:**

**Basic connection:**
```
source_block_name -> destiny_block_name
```

**Custom connection** *(square brackets contain possible arrow types)*:
```
source_block_name ([x<, <, <<, \, //, \\, o<, \\o ], [., -, _], [>x, >, >>, \, //, \\, >o, o\\]) destiny_block_name labeled "label_name"
```

**Class relationship connection:**
```
source_class_name [inherit, implement, associate, depend, aggregate, compose] destiny_class_name
```

---

### 2.1 Objects Specific to Class Diagrams

```
class theme_name class_name:
    public "int value"
    function protected "int calc(int x)"
    private "string name"

abstract theme_name class_name:
    public "int value"
    function protected "int calc(int x)"
    function private "string getName()"

interface theme_name interface_name:
    "int calc(string source)"
```

---

### 2.2 Objects Specific to Sequence Diagrams

**Creating/declaring a block:**
```
block theme_name block_name labeled "label_name"
```

**Activating a block:**
```
activate block_name
```

**Destroying a block:**
```
destroy block_name
```

**Connecting blocks:**
Connect blocks the same way as other objects. You can add a delay like this:
```
source_block_name -> ... destiny_block_name
```

---

### 2.3 Objects Specific to Use-Case Diagrams

**Creating an actor:**
```
actor theme_name actor_name labeled "label_name"
```

**Creating use-cases:**
```
usecase theme_name usecase_name:
    "usecase_text"
    "..."
```

---

## 3. Object Container – List

**Creating a list:**
```
list_name [object1, object2.object3, object4, ...]
```

**Indexing a list:**
```
list_name[index]  # 0 <= index < list_size
```

---

## 4. Loops

**Declaring a loop:**
```
for item_name in list_name:
    function_name(item_name)
    item_name -> other_class labeled "label"
```

---

## 5. Functions

**Declaring a function:**
```
def function_name(...):
    # do something
    return (...)
```

---

## 6. Comments in Code

`#` ← this starts a comment in the code. Comment text follows.

---

## 7. Saving the Diagram State

The current state of the diagram is saved by calling the command:
```
exec diag_name [brief, all] [ [list of objects] ] ["filename.png"]
```

The `exec` command has several optional attributes:

- **Type of diagram printout**:  
  - `all` – all information  
  - `brief` – only necessary diagram information
- **List of objects** to be printed.
- **File name** to which the diagram will be saved.

---

## Usage

we used **Antlr4** and **plantuml** to create this language so first install requirements then To get your diagram in .png format run this commands:

```
pip install -r requirements.txt
python main.py [PATH TO .dml FILE]
```

The result png file will be created in the catalog results/

To test our examples use path to our code_examples file e.g. code_examples/classdiag.dml
