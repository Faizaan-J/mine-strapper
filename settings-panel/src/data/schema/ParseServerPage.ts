import type { FormPage } from "./Types";
import type { JSONSchema7 } from "json-schema";
import { parseSchemaFields } from "./FieldParser";

const parseServerPage = (schema: JSONSchema7): FormPage => {
    if (schema.type !== "object") {
        throw new Error("Schema is not an object");
    }

    const serverSchema = schema.properties?.server;

    if (!serverSchema || typeof serverSchema === "boolean") {
        throw new Error("Server properties not found in schema");
    }

    return {
        title: serverSchema.title ?? "Server",
        description: serverSchema.description,
        path: ["server"],
        fields: parseSchemaFields(serverSchema, ["server"]),
        id: "server",
    };
};

export { parseServerPage };