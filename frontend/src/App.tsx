import React from "react";
import "./styles/App.css";

import UserInputContainer from "./components/UserInputContainer";
import PlaceHolder from "./components/PlaceHolder";
import { MessageThread } from "./types/Messages";

function App() {
    const messageThread: MessageThread = new MessageThread("thread-1", []);

    return (
        <div className="App">
            <header>
                <p>Altron Agentic System</p>
            </header>

            <UserInputContainer messageThread={messageThread} />
        </div>
    );
}

export default App;
