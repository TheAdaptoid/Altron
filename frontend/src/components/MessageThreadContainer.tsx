import { Message, MessageThread } from "../types/Messages";
import React from "react";
import { getDiv } from "../utils/Dom";
import "../styles/MessageThreadContainer.css";

async function renderMessage(message: Message, threadContainer: HTMLDivElement) {
    if (!message) {
        return;
    }

    // Create a container for the message
    const messageContainer: HTMLDivElement = document.createElement("div");

    // Add the message content to the container
    messageContainer.textContent = message.content;

    // Add classes to the container
    messageContainer.classList.add("MessageContainer");
    if (message.role === "user") {
        messageContainer.classList.add("UserMessageContainer");
    } else if (message.role === "assistant") {
        messageContainer.classList.add("AssistantMessageContainer");
    }

    // Add the message container to the message thread container
    threadContainer.appendChild(messageContainer);
}

async function renderMessageThread(messageThread: MessageThread) {
    // Get the count of current child elements of the message thread container
    const messageThreadContainer: HTMLDivElement = getDiv("MessageThreadContainer");
    const appendStartIndex: number = messageThreadContainer.childElementCount;

    // Render messages not already rendered
    for (let i = appendStartIndex; i < messageThread.messages.length; i++) {
        await renderMessage(messageThread.messages[i], messageThreadContainer);
    }
}

function MessageThreadContainer({ messageThread }: { messageThread: MessageThread }) {
    React.useEffect(() => {
        if (messageThread.messages.length > 0) {
            renderMessageThread(messageThread);
        }
    }, [messageThread]);

    return <div id="MessageThreadContainer" className="MessageThreadContainer"></div>;
}

export default MessageThreadContainer;
