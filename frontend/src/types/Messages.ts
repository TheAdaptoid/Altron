/**
 * Represents a single message exchanged between a user and an assistant.
 *
 * @property id - Unique identifier for the message.
 * @property content - The textual content of the message.
 * @property role - The originator of the message, either "user" or "assistant".
 */
interface Message {
    id: string;
    content: string;
    role: "user" | "assistant";
}

/**
 * Represents a message sent by a user.
 * This extends the base Message interface with a specific role.
 * @property role - Always "user" for user messages.
 */
interface UserMessage extends Message {
    role: "user";
}

/**
 * Represents a message sent by an assistant.
 * This extends the base Message interface with a specific role.
 * @property role - Always "assistant" for assistant messages.
 */
interface AssistantMessage extends Message {
    role: "assistant";
}

class MessageThread {
    /**
     * Initializes a new instance of the MessageThread class.
     *
     * @param id - The unique identifier for the message thread.
     * @param messages - The array of messages in the thread.
     * @param createdAt - The timestamp when the thread was created.
     * @param updatedAt - The timestamp when the thread was last updated.
     */
    constructor(
        public id: string,
        public messages: Message[],
        public createdAt: Date = new Date(),
        public updatedAt: Date = new Date()
    ) {}

    /**
     * Adds a new message to the message thread and updates the timestamp.
     *
     * @param message - The message to be added to the thread.
     */
    addMessage(message: Message) {
        this.messages.push(message);
        this.updatedAt = new Date();
    }

    /**
     * Gets the last message from the message thread, or null if the thread is empty.
     *
     * @returns The last message from the thread, or null if the thread is empty.
     */
    getLastMessage(): Message | null {
        return this.messages.length > 0
            ? this.messages[this.messages.length - 1]
            : null;
    }
}

export { MessageThread };
export type { Message, UserMessage, AssistantMessage };
