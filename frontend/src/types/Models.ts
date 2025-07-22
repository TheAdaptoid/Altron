/**
 * This file contains types related to the models used in the chat system.
 * Models are artificial intelligence that generate text based on input.
 */

/**
 * An enumeration of the types of models that can be used in the chat system.
 * The {@link ModelType.Chat} type is for chat models.
 * The {@link ModelType.Embedding} type is for embedding models.
 * The {@link ModelType.Undefined} type is for undefined models.
 */
enum ModelType {
    Chat = "chat",
    Embedding = "embedding",
    Undefined = "undefined",
}

/**
 * Represents a model used in the chat system.
 *
 * @property id - Unique identifier for the model.
 * @property alias - The alias for the model, if any.
 * @property provider - The name of the provider for the model.
 * @property type - The type of the model, either {@link ModelType.Chat}, {@link ModelType.Embedding}, or {@link ModelType.Undefined}.
 */
interface Model {
    id: string;
    alias: string | null;
    provider: string;
    type: ModelType;
}

export { ModelType };
export type { Model };
