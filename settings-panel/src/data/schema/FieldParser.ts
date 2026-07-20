import type { JSONSchema7 } from "json-schema";
import type { FormField } from "./Types";

export const parseSchemaFields = (schema: JSONSchema7, path: string[] = []): FormField[] => {
    if (!schema.properties) {
        return [];
    }

    const required = new Set(schema.required ?? []);

    return Object.entries(schema.properties).map(([key, child]) =>
        parseField(
            child as JSONSchema7,
            key,
            [...path, key],
            required.has(key)
        )
    );
}

export const parseField = (
    schema: JSONSchema7,
    key: string,
    path: string[],
    required: boolean
): FormField => {

    if (schema.enum) {
        return parseEnumField(schema, key, path, required);
    }

    switch (schema.type) {

        case "string":
            return parseStringField(schema, key, path, required);

        case "boolean":
            return parseBooleanField(schema, key, path, required);

        case "integer":
            return parseIntegerField(schema, key, path, required);

        case "number":
            return parseNumberField(schema, key, path, required);

        case "array":
            return parseArrayField(schema, key, path, required);

        case "object":
            return parseObjectField(schema, key, path, required);

        default:
            throw new Error(`Unsupported schema type: ${schema.type}`);
    }
}

export const parseEnumField = (schema: JSONSchema7, key: string, path: string[], required: boolean): FormField => {
    return {
        key,
        path,
        type: "enum",
        required,

        enumValues: schema.enum ?? [],

        description: schema.description,
        defaultValue: schema.default,
    };
}

export const parseStringField = (schema: JSONSchema7, key: string, path: string[], required: boolean): FormField => {
    if (schema.enum) {
        return parseEnumField(schema, key, path, required);
    }

    const field: FormField = {} as FormField;
    field.key = key;
    field.path = path;
    field.required = required;
    if (schema.description) {
        field.description = schema.description;
    }
    if (schema.default != undefined) {
        field.defaultValue = schema.default;
    }
    field.type = "string";

    return field;
}

export const parseBooleanField = (schema: JSONSchema7, key: string, path: string[], required: boolean): FormField => {
    if (schema.enum) {
        return parseEnumField(schema, key, path, required);
    }

    const field: FormField = {} as FormField;
    field.key = key;
    field.path = path;
    field.required = required;
    field.type = "boolean";
    if (schema.description) {
        field.description = schema.description;
    }
    if (schema.default != undefined) {
        field.defaultValue = schema.default;
    }

    return field;
}

export const parseIntegerField = (schema: JSONSchema7, key: string, path: string[], required: boolean): FormField => {
    if (schema.enum) {
        return parseEnumField(schema, key, path, required);
    }
    
    const field: FormField = {} as FormField;

    field.key = key;
    field.path = path;
    field.required = required;
    field.type = "integer";
    if (schema.description) {
        field.description = schema.description;
    }
    if (schema.default != undefined) {
        field.defaultValue = schema.default;
    }
    if (schema.minimum != undefined) {
        field.minimum = schema.minimum;
    }
    if (schema.maximum != undefined) {
        field.maximum = schema.maximum;
    }
    
    return field;
}

export const parseNumberField = (schema: JSONSchema7, key: string, path: string[], required: boolean): FormField => {
    if (schema.enum) {
        return parseEnumField(schema, key, path, required);
    }

    const field: FormField = {} as FormField;
    field.key = key;
    field.path = path;
    field.required = required;
    field.type = "number";
    if (schema.description) {
        field.description = schema.description;
    }
    if (schema.default != undefined) {
        field.defaultValue = schema.default;
    }
    if (schema.minimum != undefined) {
        field.minimum = schema.minimum;
    }
    if (schema.maximum != undefined) {
        field.maximum = schema.maximum;
    }

    return field;
}

export const parseArrayField = (schema: JSONSchema7, key: string, path: string[], required: boolean): FormField => {
    if (schema.enum) {
        return parseEnumField(schema, key, path, required);
    }
    
    if (!schema.items) {
        throw new Error(`Array field ${key} does not have an "items" schema`);
    }

    const items = schema.items;

    let item: FormField | undefined;

    if (items && !Array.isArray(items) && typeof items !== "boolean") {
        item = parseField(
            items,
            "item",
            [...path, "item"],
            false
        );
    }

    const field: FormField = {} as FormField;
    field.key = key;
    field.path = path;
    field.type = "array";
    field.required = required;
    if (schema.description) {
        field.description = schema.description;
    }
    field.arrayItem = item;

    return field;
}

export const parseObjectField = (schema: JSONSchema7, key: string, path: string[], required: boolean): FormField => {
    if (schema.enum) {
        return parseEnumField(schema, key, path, required);
    }

    const field: FormField = {} as FormField;
    field.key = key;
    field.path = path;
    field.type = "object";
    field.required = required;
    field.children = parseSchemaFields(schema, path);
    if (schema.description) {
        field.description = schema.description;
    }
    return field;
}
