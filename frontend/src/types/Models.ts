enum ModelType {
    Chat = "chat",
    Embedding = "embedding",
    Undefined = "undefined"
}

interface Model {
    id: string;
    alias: string | null;
    provider: string;
    type: ModelType;
}

export { ModelType };
export type { Model };