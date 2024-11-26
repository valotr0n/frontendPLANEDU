import { useState, useRef, useEffect } from 'react';
import Header from '../compnents/Header';
export default function Chat() {
 const [messages, setMessages] = useState([]);
 const [inputMessage, setInputMessage] = useState('');
 const [isLoading, setIsLoading] = useState(false);
 const messagesEndRef = useRef(null);
  const scrollToBottom = () => {
   messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
 };
  useEffect(() => {
   scrollToBottom();
 }, [messages]);
  const handleSubmit = async (e) => {
   e.preventDefault();
   if (!inputMessage.trim()) return;
    const userMessage = { role: 'user', content: inputMessage };
   setMessages(prev => [...prev, userMessage]);
   setInputMessage('');
   setIsLoading(true);
    try {
     const response = await fetch('YOUR_API_ENDPOINT', {
       method: 'POST',
       headers: {
         'Content-Type': 'application/json',
       },
       body: JSON.stringify({ message: inputMessage }),
     });
      const data = await response.json();
     setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
   } catch (error) {
     console.error('Error:', error);
     setMessages(prev => [...prev, { 
       role: 'assistant', 
       content: 'Извините, произошла ошибка. Попробуйте позже.' 
     }]);
   } finally {
     setIsLoading(false);
   }
 };
  return (
   <div className="min-h-screen bg-gray-50">
     <Header />
     <div className="max-w-3xl mx-auto px-4 py-8">
       <div className="bg-white rounded-lg shadow-lg h-[600px] flex flex-col">
         <div className="flex-1 overflow-y-auto p-4 space-y-4">
           {messages.map((message, index) => (
             <div
               key={index}
               className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
             >
               <div
                 className={`max-w-[80%] rounded-lg p-3 ${
                   message.role === 'user'
                     ? 'bg-blue-600 text-white'
                     : 'bg-gray-100 text-gray-800'
                 }`}
               >
                 {message.content}
               </div>
             </div>
           ))}
           {isLoading && (
             <div className="flex justify-start">
               <div className="bg-gray-100 rounded-lg p-3 text-gray-800">
                 Печатает...
               </div>
             </div>
           )}
           <div ref={messagesEndRef} />
         </div>
         <form onSubmit={handleSubmit} className="border-t p-4">
           <div className="flex gap-2">
             <input
               type="text"
               value={inputMessage}
               onChange={(e) => setInputMessage(e.target.value)}
               placeholder="Введите сообщение..."
               className="flex-1 rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:border-blue-500"
             />
             <button
               type="submit"
               disabled={isLoading}
               className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
             >
               Отправить
             </button>
           </div>
         </form>
       </div>
     </div>
   </div>
 );
}