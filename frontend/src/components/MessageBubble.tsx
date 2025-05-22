/**
 * Props interface for the MessageBubble component
 * @property text - The content of the message to display
 * @property isUser - Boolean flag to indicate if the message is from the user (true) or AI (false)
 */
interface MessageBubbleProps {
  text: string;
  isUser: boolean;
}

/**
 * MessageBubble - A reusable component for displaying chat messages
 * 
 * This component renders a single message bubble that can be styled differently
 * based on whether it's a user message or an AI response.
 * 
 * @param text - The message content to display
 * @param isUser - If true, aligns right with blue background; if false, aligns left with white/dark background
 */
export function MessageBubble({ text, isUser }: MessageBubbleProps) {
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[80%] rounded-lg px-4 py-2 ${
          isUser
            ? 'bg-blue-500 text-white'  // User message styling
            : 'bg-white dark:bg-gray-700 text-gray-800 dark:text-white'  // AI message styling
        }`}
      >
        {text}
      </div>
    </div>
  );
}
