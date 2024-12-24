import json
import re

def extract_libraries(c_file):
    """
    Extracts libraries from a C source file.
    """
    libraries = []
    with open(c_file, 'r') as file:
        content = file.read()
        # Regex to find libraries included with #include
        matches = re.findall(r'#include\s*["<](.*?)[">]', content)
        for match in matches:
            libraries.append(match)
    return libraries

def generate_sbom(libraries):
    """
    Generate a CycloneDX SBOM (Software Bill of Materials) in JSON format
    """
    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.4",
        "version": 1,
        "metadata": {
            "timestamp": "2024-12-24T00:00:00Z"
        },
        "components": []
    }

    for library in libraries:
        sbom['components'].append({
            "type": "library",
            "name": library,
            "version": "unknown",  # You can change this if you know the version
            "purl": f"pkg:generic/{library}@unknown"
        })
    
    return sbom

def write_sbom_to_file(sbom, filename):
    """
    Writes the generated SBOM to a JSON file.
    """
    with open(filename, 'w') as f:
        json.dump(sbom, f, indent=2)

if __name__ == "__main__":
    c_file = 'legacy_code.c'  # Replace with your C file path
    sbom_filename = 'sbom.json'  # Output SBOM file name
    
    libraries = extract_libraries(c_file)
    sbom = generate_sbom(libraries)
    
    write_sbom_to_file(sbom, sbom_filename)
    print(f"SBOM generated and saved to {sbom_filename}")

