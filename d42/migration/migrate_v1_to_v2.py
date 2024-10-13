#!/usr/bin/env python3
import ast
import os
from collections import defaultdict
from typing import Dict, Tuple, Union

__all__ = ("migrate_v1_to_v2",)

mapping = {
    "district42": {
        "schema": ("d42", "schema"),
        "GenericSchema": ("d42.declaration", "GenericSchema"),
        "Props": ("d42.declaration", "Props"),
        "PropsType": ("d42.declaration", "PropsType"),
        "SchemaVisitor": ("d42.declaration", "SchemaVisitor"),
        "SchemaVisitorReturnType": ("d42.declaration", "SchemaVisitorReturnType"),
        "from_native": ("d42.utils", "from_native"),
        "optional": ("d42", "optional"),
        "register_type": ("d42.custom_type", "register_type"),
        "represent": ("d42.representation", "represent"),
        "make_required": ("d42.utils", "make_required"),
    },
    "district42.errors": {
        "DeclarationError": ("d42.declaration", "DeclarationError"),
        "make_invalid_type_error": ("d42.declaration.errors", "make_invalid_type_error"),
        "make_already_declared_error": ("d42.declaration.errors", "make_already_declared_error"),
        "make_incorrect_min_error": ("d42.declaration.errors", "make_incorrect_min_error"),
        "make_incorrect_max_error": ("d42.declaration.errors", "make_incorrect_max_error"),
        "make_incorrect_len_error": ("d42.declaration.errors", "make_incorrect_len_error"),
        "make_incorrect_min_len_error": ("d42.declaration.errors", "make_incorrect_min_len_error"),
        "make_incorrect_max_len_error": ("d42.declaration.errors", "make_incorrect_max_len_error"),
        "make_incorrect_precision_error": ("d42.declaration.errors",
                                           "make_incorrect_precision_error"),
    },
    "district42.representor": {
        "Representor": ("d42.representation", "Representor"),
    },
    "district42.types": {
        "AnySchema": ("d42.declaration.types", "AnySchema"),
        "AnyProps": ("d42.declaration.types", "AnyProps"),
        "BoolSchema": ("d42.declaration.types", "BoolSchema"),
        "BoolProps": ("d42.declaration.types", "BoolProps"),
        "BytesSchema": ("d42.declaration.types", "BytesSchema"),
        "BytesProps": ("d42.declaration.types", "BytesProps"),
        "DateSchema": ("d42.declaration.types", "DateSchema"),
        "DateProps": ("d42.declaration.types", "DateProps"),
        "DateTimeSchema": ("d42.declaration.types", "DateTimeSchema"),
        "DateTimeProps": ("d42.declaration.types", "DateTimeProps"),
        "DictSchema": ("d42.declaration.types", "DictSchema"),
        "DictProps": ("d42.declaration.types", "DictProps"),
        "FloatSchema": ("d42.declaration.types", "FloatSchema"),
        "FloatProps": ("d42.declaration.types", "FloatProps"),
        "IntSchema": ("d42.declaration.types", "IntSchema"),
        "IntProps": ("d42.declaration.types", "IntProps"),
        "ListSchema": ("d42.declaration.types", "ListSchema"),
        "ListProps": ("d42.declaration.types", "ListProps"),
        "NoneSchema": ("d42.declaration.types", "NoneSchema"),
        "NoneProps": ("d42.declaration.types", "NoneProps"),
        "StrSchema": ("d42.declaration.types", "StrSchema"),
        "StrProps": ("d42.declaration.types", "StrProps"),
        "UUID4Schema": ("d42.declaration.types", "UUID4Schema"),
        "UUID4Props": ("d42.declaration.types", "UUID4Props"),
        "GenericTypeAliasSchema": ("d42.declaration.types", "GenericTypeAliasSchema"),
        "TypeAliasSchema": ("d42.declaration.types", "TypeAliasSchema"),
        "TypeAliasProps": ("d42.declaration.types", "TypeAliasProps"),
        "TypeAliasPropsType": ("d42.declaration.types", "TypeAliasPropsType"),
        "GenericSchema": ("d42.declaration", "GenericSchema"),
        "Schema": ("d42.declaration", "Schema"),
        "optional": ("d42", "optional"),
        "make_required": ("d42.utils", "make_required"),
    },
    "district42.utils": {
        "is_ellipsis": ("d42.utils", "is_ellipsis"),
        "EllipsisType": ("d42.utils", "EllipsisType"),
        "TypeOrEllipsis": ("d42.utils", "TypeOrEllipsis"),
        "rollout": ("d42.utils", "rollout"),
    },

    # blahblah
    "blahblah": {
        "fake": ("d42", "fake"),
        "generate": ("d42.generation", "generate"),
        "Generator": ("d42.generation", "Generator"),
        "Random": ("d42.generation", "Random"),
        "RegexGenerator": ("d42.generation", "RegexGenerator"),
    },

    # valera
    "valera": {
        "validate": ("d42", "validate"),
        "validate_or_fail": ("d42", "validate_or_fail"),
        "ValidationException": ("d42", "ValidationException"),
        "eq": ("d42.validation", "eq"),
        "format_result": ("d42.validation", "format_result"),
        "Validator": ("d42.validation", "Validator"),
        "ValidationResult": ("d42.validation", "ValidationResult"),
        "Formatter": ("d42.validation", "Formatter"),
        "AbstractFormatter": ("d42.validation", "AbstractFormatter"),
    },
    "valera.errors": {
        "ValidationError": ("d42.validation.errors", "ValidationError"),
        "TypeValidationError": ("d42.validation.errors", "TypeValidationError"),
        "ValueValidationError": ("d42.validation.errors", "ValueValidationError"),
        "MinValueValidationError": ("d42.validation.errors", "MinValueValidationError"),
        "MaxValueValidationError": ("d42.validation.errors", "MaxValueValidationError"),
        "LengthValidationError": ("d42.validation.errors", "LengthValidationError"),
        "MinLengthValidationError": ("d42.validation.errors", "MinLengthValidationError"),
        "MaxLengthValidationError": ("d42.validation.errors", "MaxLengthValidationError"),
        "AlphabetValidationError": ("d42.validation.errors", "AlphabetValidationError"),
        "SubstrValidationError": ("d42.validation.errors", "SubstrValidationError"),
        "RegexValidationError": ("d42.validation.errors", "RegexValidationError"),
        "MissingElementValidationError": ("d42.validation.errors",
                                          "MissingElementValidationError"),
        "ExtraElementValidationError": ("d42.validation.errors", "ExtraElementValidationError"),
        "MissingKeyValidationError": ("d42.validation.errors", "MissingKeyValidationError"),
        "ExtraKeyValidationError": ("d42.validation.errors", "ExtraKeyValidationError"),
        "SchemaMismatchValidationError": ("d42.validation.errors",
                                          "SchemaMismatchValidationError"),
        "InvalidUUIDVersionValidationError": ("d42.validation.errors",
                                              "InvalidUUIDVersionValidationError"),
    },

    # revolt
    "revolt": {
        "substitute": ("d42", "substitute"),
        "Substitutor": ("d42.substitution", "Substitutor"),
        "SubstitutorValidator": ("d42.substitution", "SubstitutorValidator"),
    },
    "revolt.errors": {
        "SubstitutionError": ("d42.substitution.errors", "SubstitutionError"),
        "make_substitution_error": ("d42.substitution.errors", "make_substitution_error"),
    },
}

MappingType = Dict[str, Dict[str, Tuple[str, str]]]


def rewrite_imports(source_code: str, mapping: MappingType) -> Union[str, None]:
    lines = source_code.splitlines(keepends=True)
    tree = ast.parse(source_code)
    replacements = []

    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            module = node.module
            if node.level > 0:
                continue  # Skip relative imports like 'from .module import ...'

            new_imports = defaultdict(list)
            unmapped_names = []

            for alias in node.names:
                name = alias.name
                asname = alias.asname
                if module in mapping and name in mapping[module]:
                    new_module, new_name = mapping[module][name]
                    import_name = f"{new_name} as {asname}" if asname else new_name
                    new_imports[new_module].append(import_name)
                else:
                    import_name = f"{name} as {asname}" if asname else name
                    unmapped_names.append(import_name)

            # Build replacement lines
            replacement_lines = []
            for new_module, names in new_imports.items():
                names_str = ', '.join(names)
                replacement_lines.append(f'from {new_module} import {names_str}\n')
            if unmapped_names:
                names_str = ', '.join(unmapped_names)
                replacement_lines.append(f'from {module} import {names_str}\n')

            # Get line numbers
            start_line = node.lineno - 1  # Convert to 0-based index
            end_line = getattr(node, 'end_lineno', node.lineno) - 1
            replacements.append((start_line, end_line, replacement_lines))

    if len(replacements) == 0:
        return None

    # Apply replacements in reverse order to maintain line indices
    for start_line, end_line, replacement_lines in reversed(replacements):
        lines[start_line:end_line+1] = replacement_lines

    return ''.join(lines)


def process_file(filepath: str, mapping: MappingType) -> None:
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            source_code = file.read()

        # Rewrite imports in the source code
        modified_code = rewrite_imports(source_code, mapping)

        if modified_code:
            # Write the modified code back to the file
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(modified_code)
            print(f"Processed: {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")


def process_directory(directory: str, mapping: MappingType) -> None:
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        for filename in files:
            if filename.endswith('.py'):
                filepath = os.path.join(root, filename)
                process_file(filepath, mapping)


def migrate_v1_to_v2(directory: str) -> None:
    process_directory(directory, mapping)
