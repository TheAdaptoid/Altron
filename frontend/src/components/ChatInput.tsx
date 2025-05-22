/**
 * Props interface for the ChatInput component
 * @property value - The current value of the input field
 * @property onChange - Callback function that receives the new input value
 * @property onSend - Callback function triggered when the send button is clicked or Enter is pressed
 */
interface ChatInputProps {
  value: string;
  onChange: (value: string) => void;
  onSend: () => void;
}

/**
 * ChatInput - A reusable component for chat message input
 * 
 * This component renders an input field with a send button. It handles both
 * text input and message sending through callbacks to the parent component.
 * 
 * Features:
 * - Controlled input field
 * - Send button
 * - Enter key support for sending messages
 * - Dark mode compatible
 */
export function ChatInput({ value, onChange, onSend }: ChatInputProps) {
  return (
    <div className="bg-white dark:bg-gray-800 p-4 shadow-lg">
      <div className="flex space-x-4">
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}  // Call onChange with the new value
          onKeyPress={(e) => e.key === 'Enter' && onSend()}  // Send message on Enter key
          placeholder="Type your message..."
          className="flex-1 px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 
                   focus:outline-none focus:ring-2 focus:ring-blue-500 
                   bg-white dark:bg-gray-700 text-gray-800 dark:text-white"
        />
        <button
          onClick={onSend}
          className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 
                   transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Send
        </button>
      </div>
    </div>
  );
}
