import { JSONSchema7 } from "json-schema";
import { parseSchemaFields } from "./FieldParser";

const prettifyTitle = (key: string) =>
    key
        .split("_")
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(" ");

const parseBuiltInFeatures = (schema: JSONSchema7): any => {
    const features = schema.properties?.features;

    if (!features || typeof features === "boolean") {
        return [];
    }

    if (!features.properties) {
        return [];
    }

    return Object.entries(features.properties).map(([key, value]) => {
        if (typeof value === "boolean") {
            throw new Error(`Feature "${key}" has an invalid schema`);
        }

        const path = ["features", key];

        return {
            id: key,
            title: prettifyTitle(key),
            path,
            description: value.description,
            fields: parseSchemaFields(value, path),
        };
    });
}

export { parseBuiltInFeatures };