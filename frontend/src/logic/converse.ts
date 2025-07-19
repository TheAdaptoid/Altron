import { Message, MessageThread } from "../types/Messages";

async function submitUserMessage(userMessage: Message, messageThread: MessageThread) {
    // Log the input value to the console
    console.log("User input submitted:", userMessage.content);

    // Add the user message to the message thread
    messageThread.addMessage(userMessage);

    // Send the message thread to the server or handle it as needed
    // For now, we will just log the updated message thread
    console.log("Updated message thread:", messageThread);
}

export { submitUserMessage };
