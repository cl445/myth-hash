# Myth Hash

`Myth Hash` is aPython package designed to create human-readable hashes that are not only functional but also cognitively engaging. A key feature of this tool is its multilingual support, enabling the generation of hashes in multiple languages. The concept behind these human-readable hashes is to enhance communication and recognition by creating hashes that form vivid, memorable mental images. The goal is to make the hash as human-compatible as possible, ensuring it effectively serves its purpose in an intuitive and user-friendly manner.
## Features

- **Character Name Generation:** Generates a unique fantasy name based on an input string.
- **Supported Languages:** Currently supports English (`en`) and German (`de`).
- **CLI Support:** Easily generate names via the command line.
- **Library Usage:** Integrate `Myth Hash` into your Python projects.
- **Customizable Data:** Modify the included JSON files to customize the generated names.

## Installation

You can install `Myth Hash` using pip:

```bash
pip install myth-hash
```

## Usage

### Command Line Interface (CLI)

After installing the package, you can use the myth-hash command to generate fantasy names.

Basic Example:
    
```bash
myth-hash "The moon whispered secrets, but only the cats understood." 
```
Example Output:
```bash
exotic-thoughtful-Griffin
```

### Using as a Library

You can also use Myth Hash within your Python code:

Example:
```python
import myth_hash

# Generate a character name using the hash_name function
name_parts = myth_hash.hash_name("The moon whispered secrets, but only the cats understood.", "en")
print(name_parts)  # Output: ('exotic', 'thoughtful', 'Griffin')

# Access individual parts of the name
physical_attr, personality_attr, mystical_creature = name_parts
print(f"Physical Attribute: {physical_attr}")
print(f"Personality Trait: {personality_attr}")
print(f"Mystical Creature: {mystical_creature}")
```

## Contributing

Contributions are welcome! Please fork the repository, create a new branch for your feature or bug fix, and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.