import { FormField, FormPage, ParsedSchema } from "./Types";
import { parseSchema } from "./Parser";

const SCHEMA_URL = "https://faizaan-j.github.io/mine-strapper/schemas/Config.schema.json";

let cached: ParsedSchema | null = null;

const loadSchema = async () => {
    if (cached) {
        return cached;
    }
    
    const response = await fetch(SCHEMA_URL);
    if (!response.ok) {
        throw new Error(`Failed to load schema from ${SCHEMA_URL}: ${response.statusText}`);
    }

    const json = await response.json();
    cached = await parseSchema(json);
    return cached;
}

interface UseSchema {
    schema: ParsedSchema | null;
}

const useSchema = async () => {
    const hookTable = {} as UseSchema;

    try {
        const schema = await loadSchema();
        hookTable.schema = schema;
    } catch (error) {
        console.error("Error loading schema:", error);
        throw error;
    }

    return hookTable;
}

export { useSchema };