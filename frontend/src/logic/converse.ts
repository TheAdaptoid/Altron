interface Message {
    id: string;
    content: string;
    role: "user" | "assistant";
}

class MessageThread {
    constructor(
        public id: string,
        public messages: Message[],
        public createdAt: Date,
        public updatedAt: Date
    ) {}

    addMessage(message: Message) {
        this.messages.push(message);
        this.updatedAt = new Date();
    }

    getLastMessage(): Message | null {
        return this.messages.length > 0
            ? this.messages[this.messages.length - 1]
            : null;
    }
}

export { MessageThread };
export type { Message };
