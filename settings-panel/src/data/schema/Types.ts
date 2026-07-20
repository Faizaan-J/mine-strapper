export interface ParsedSchema {
    pages: FormPage[];
}

export interface FormPage {
    id: string;
    title: string;
    path: string[];
    description?: string;
    fields: FormField[];
}

export interface FormField {
    key: string;
    path: string[];

    type:
        | "string"
        | "integer"
        | "number"
        | "boolean"
        | "enum"
        | "array"
        | "object";

    required: boolean;

    description?: string;
    placeholder?: string;
    defaultValue?: unknown;

    enumValues?: any[];

    minimum?: number;
    maximum?: number;

    children?: FormField[];

    arrayItem?: FormField;

    visibleWhen?: {
        path: string[];
        equals: unknown;
    };
}
