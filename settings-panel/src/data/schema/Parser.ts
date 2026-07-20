import { ParsedSchema } from "./Types"

import $RefParser from "@apidevtools/json-schema-ref-parser";
import { JSONSchema7 } from "json-schema";

import { parseServerPage } from "./ParseServerPage";
import { parseBuiltInFeatures } from "./ParseBuiltInFeatures";

const parseSchema = async (schema: object): Promise<ParsedSchema> => {
    const resolved = await $RefParser.dereference(schema);
    
    const parsed = {
        pages: [
            parseServerPage(resolved as JSONSchema7),
            ...parseBuiltInFeatures(resolved as JSONSchema7)
        ]
    }
    console.log("PARSED: ", parsed);
    return parsed;
}

export { parseSchema };
