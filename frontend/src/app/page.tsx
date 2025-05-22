'use client';  // Mark this as a client component for client-side interactivity

import { useState } from 'react';
import { MessageBubble } from '@/components/MessageBubble';
import { ChatInput } from '@/components/ChatInput';

/**
 * Interface for chat message objects
 * @property id - Unique identifier for the message
 * @property text - Content of the message
 * @property isUser - Flag to indicate if the message is from the user
 */
interface Message {
  id: number;
  text: string;
  isUser: boolean;
}

/**
 * Home - Main chat application component
 * 
 * This component manages the chat state and renders the chat interface.
 * It handles message sending and receiving, and maintains the message history.
 */
export default function Home() {
  // State for storing chat messages
  const [messages, setMessages] = useState<Message[]>([]);
  // State for the current input message
  const [inputMessage, setInputMessage] = useState('');

  /**
   * Handles sending a new message
   * - Adds the user's message to the chat
   * - Clears the input field
   * - Triggers a mock AI response (to be replaced with actual API call)
   */
  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    // Add user message to chat
    const newMessage: Message = {
      id: Date.now(),
      text: inputMessage,
      isUser: true,
    };
    
    setMessages(prev => [...prev, newMessage]);
    setInputMessage('');

    // TODO: Add API call to backend here
    // For now, simulate an AI response after 1 second
    setTimeout(() => {
      const aiResponse: Message = {
        id: Date.now() + 1,
        text: "This is a mock AI response. Connect your backend API to get real responses.",
        isUser: false,
      };
      setMessages(prev => [...prev, aiResponse]);
    }, 1000);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 dark:bg-gray-900">
      {/* Header section */}
      <div className="bg-white dark:bg-gray-800 shadow px-6 py-4">
        <h1 className="text-xl font-semibold text-gray-800 dark:text-white">AI Chat</h1>
      </div>

      {/* Messages section - scrollable area for chat history */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((message) => (
          <MessageBubble
            key={message.id}
            text={message.text}
            isUser={message.isUser}
          />
        ))}
      </div>

      {/* Input section - fixed at bottom */}
      <ChatInput
        value={inputMessage}
        onChange={setInputMessage}
        onSend={handleSendMessage}
      />
    </div>
  );
}
