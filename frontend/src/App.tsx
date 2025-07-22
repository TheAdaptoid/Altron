import React from "react";
import "./styles/App.css";

import UserInputContainer from "./components/UserInputContainer";
import { MessageThread } from "./types/Messages";
import { Model } from "./types/Models";
import MessageThreadContainer from "./components/MessageThreadContainer";

function App() {
    // Track the message thread
    const [messageThread, setMessageThread] = React.useState<MessageThread>(
        new MessageThread([])
    );
    // Track selected model
    const [selectedModel, setSelectedModel] = React.useState<Model | null>(null);

    // Update application state
    React.useEffect(() => {
        console.log("Selected Model: ", selectedModel);
        console.log("Messages: ", messageThread.messages);
    });

    return (
        <div className="App">
            <MessageThreadContainer messageThread={messageThread} />

            <UserInputContainer
                messageThread={messageThread}
                setMessageThread={setMessageThread}
                selectedModel={selectedModel}
                setSelectedModel={setSelectedModel}
            />
        </div>
    );
}

export default App;
