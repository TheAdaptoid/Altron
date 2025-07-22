class Message {
    /**
     * Represents a single message exchanged between a user and an assistant.
     *
     * @property id - Unique identifier for the message.
     * @property content - The textual content of the message.
     * @property role - The originator of the message, either "user" or "assistant".
     */
    constructor(
        // id: string,
        public content: string,
        public role: "user" | "assistant"
    ) {}
}

class UserMessage extends Message {
    /**
     * Represents a message sent by a user.
     * This extends the base Message interface with a specific role.
     * @property role - Always "user" for user messages.
     */
    constructor(content: string) {
        super(content, "user");
    }
}

class AssistantMessage extends Message {
    /**
     * Represents a message sent by an assistant.
     * This extends the base Message interface with a specific role.
     * @property role - Always "assistant" for assistant messages.
     */
    constructor(content: string) {
        super(content, "assistant");
    }
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
        // public id: string,
        public messages: Message[],
        public createdAt: Date = new Date(),
        public updatedAt: Date = new Date()
    ) {}
}

export { MessageThread, Message, UserMessage, AssistantMessage };
