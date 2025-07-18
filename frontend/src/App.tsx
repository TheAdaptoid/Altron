import React from "react";
import "./App.css";

import UserInputContainer from "./components/UserInputContainer";
import PlaceHolder from "./components/PlaceHolder";
import { MessageThread } from "./logic/converse";

function App() {
    const messageThread: MessageThread = new MessageThread(
        "thread-1",
        [],
        new Date(),
        new Date()
    );
    

    return (
        <div className="App">
            <header>
                <p>Altron Agentic System</p>
            </header>

            <PlaceHolder />

            <UserInputContainer messageThread={messageThread} />
        </div>
    );
}

export default App;
