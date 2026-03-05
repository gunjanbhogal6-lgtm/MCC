import React, { useState, useEffect, useRef } from 'react';
import { createRoot } from 'react-dom/client';
import { motion, AnimatePresence } from 'framer-motion';
import { Bot, X, Send, Sparkles } from 'lucide-react';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const knowledgeBase = {
    ucaas: "UCaaS (Unified Communications as a Service) is a cloud-delivered model offering enterprise messaging, online meetings, telephony, and video conferencing in one unified platform. It's designed to boost team productivity globally!",
    caas: "CaaS (Communications as a Service) provides cloud-based voice and messaging without the overhead of physical infrastructure.",
    cpaas: "CPaaS (Communications Platform as a Service) allows developers to integrate voice, video, and messaging APIs directly into their apps. It forms the backbone of custom communication workflows.",
    pricing: "Our pricing is flexible and scalable. You only pay for the active usage and DIDs you need, saving up to 60% compared to legacy systems.",
    default: "I'm the My Call Connect AI Assistant! I specialize in UCaaS, CPaaS, and cloud telephony. What can I help you discover today?"
  };

  const getResponse = (text) => {
    const lower = text.toLowerCase();
    if (lower.includes("ucaas")) return knowledgeBase.ucaas;
    if (lower.includes("caas") && !lower.includes("cpaas")) return knowledgeBase.caas;
    if (lower.includes("cpaas")) return knowledgeBase.cpaas;
    if (lower.includes("price") || lower.includes("cost") || lower.includes("pricing")) return knowledgeBase.pricing;
    if (lower.includes("hello") || lower.includes("hi") || lower.includes("hey")) return "Hello! Welcome to My Call Connect. How can I help you scale your communications today?";
    return knowledgeBase.default;
  };

  useEffect(() => {
    if (isOpen && messages.length === 0) {
      setIsTyping(true);
      setTimeout(() => {
        setMessages([
          { text: "Hi there! 👋 I'm your My Call Connect AI Assistant.", sender: "bot" },
          { text: "Ask me anything about UCaaS, CaaS, or our global telecom solutions!", sender: "bot" }
        ]);
        setIsTyping(false);
      }, 1200);
    }
  }, [isOpen]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const handleSend = () => {
    if (!inputValue.trim()) return;
    const userMsg = inputValue.trim();
    setMessages(prev => [...prev, { text: userMsg, sender: "user" }]);
    setInputValue("");
    setIsTyping(true);

    setTimeout(() => {
      setMessages(prev => [...prev, { text: getResponse(userMsg), sender: "bot" }]);
      setIsTyping(false);
    }, 1500 + Math.random() * 1000);
  };

  return (
    <div className="fixed bottom-6 right-6 z-[9999] font-sans" style={{ perspective: '1000px' }}>

      <AnimatePresence>
        {!isOpen && (
          <motion.button
            initial={{ scale: 0, rotateY: -180 }}
            animate={{
              scale: 1,
              rotateY: 0,
              y: [0, -10, 0] // floating effect
            }}
            exit={{ scale: 0, rotateY: 180, opacity: 0 }}
            transition={{
              duration: 0.6,
              type: "spring", stiffness: 260, damping: 20,
              y: { duration: 2, repeat: Infinity, ease: "easeInOut" }
            }}
            onClick={() => setIsOpen(true)}
            className="absolute bottom-0 right-0 w-16 h-16 rounded-full bg-gradient-to-tr from-cyan-400 to-blue-600 flex items-center justify-center text-white shadow-[0_0_30px_rgba(6,182,212,0.6)] z-20 hover:scale-110 cursor-pointer"
            style={{ transformStyle: 'preserve-3d' }}
          >
            {/* 3D Inner Core */}
            <motion.div
              animate={{ rotateZ: 360, rotateX: 360 }}
              transition={{ duration: 10, repeat: Infinity, ease: "linear" }}
              className="absolute inset-2 border-2 border-cyan-200/30 rounded-full"
              style={{ transform: 'translateZ(20px)' }}
            />
            {/* Icon */}
            <motion.div style={{ transform: 'translateZ(30px)' }}>
              <Bot size={28} />
            </motion.div>

            {/* Orbiting particles */}
            <div className="absolute top-0 right-0 flex h-4 w-4" style={{ transform: 'translateZ(-10px)' }}>
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-200 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-4 w-4 bg-cyan-300"></span>
            </div>
          </motion.button>
        )}
      </AnimatePresence>

      {/* Chat Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 0.5, rotateX: 45, y: 100, transformOrigin: 'bottom right' }}
            animate={{ opacity: 1, scale: 1, rotateX: 0, y: 0 }}
            exit={{ opacity: 0, scale: 0.5, rotateX: -45, y: 100 }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="absolute bottom-0 right-0 bg-gray-900 border border-cyan-500/30 rounded-2xl shadow-[0_20px_50px_-15px_rgba(6,182,212,0.6)] flex flex-col overflow-hidden z-30 h-[500px] w-[360px]"
            style={{ transformStyle: 'preserve-3d' }}
          >
            {/* Header */}
            <div className="bg-gradient-to-r from-gray-800 to-gray-900 p-4 flex justify-between items-center border-b border-cyan-500/20 shadow-xl relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-cyan-400 to-blue-500"></div>

              <div className="flex items-center gap-3 relative z-10">
                <div className="relative">
                  <motion.div
                    animate={{ rotateY: 360 }}
                    transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
                    className="w-12 h-12 rounded-full bg-cyan-900/50 flex items-center justify-center border border-cyan-400/50 relative overflow-hidden group shadow-[0_0_15px_rgba(6,182,212,0.5)]"
                    style={{ transformStyle: 'preserve-3d' }}
                  >
                    <div className="absolute inset-0 bg-cyan-400 opacity-20 animate-pulse"></div>
                    <Bot size={24} className="text-cyan-400" style={{ transform: 'translateZ(10px)' }} />
                  </motion.div>
                  <div className="absolute bottom-0 right-0 w-3.5 h-3.5 bg-green-500 border-2 border-gray-900 rounded-full shadow-[0_0_5px_rgba(34,197,94,0.5)]"></div>
                </div>
                <div>
                  <h3 className="text-white font-bold text-md tracking-wide flex items-center gap-2">Nexus AI <Sparkles size={14} className="text-cyan-300" /></h3>
                  <p className="text-cyan-400 text-xs font-semibold uppercase tracking-widest flex items-center gap-1">
                    <span className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-pulse"></span> Online
                  </p>
                </div>
              </div>
              <button
                onClick={() => setIsOpen(false)}
                className="w-8 h-8 rounded-full bg-gray-800 flex items-center justify-center text-gray-400 hover:text-white hover:bg-gray-700 transition-colors relative z-10 group"
              >
                <X size={18} className="group-hover:rotate-90 transition-transform duration-300" />
              </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-900/80 backdrop-blur-md custom-scrollbar flex flex-col relative w-full">
              <div className="relative z-10 space-y-4 w-full flex-1">
                <AnimatePresence>
                  {messages.map((msg, idx) => (
                    <motion.div
                      initial={{ opacity: 0, y: 20, scale: 0.9, rotateX: 20 }}
                      animate={{ opacity: 1, y: 0, scale: 1, rotateX: 0 }}
                      key={idx}
                      className={`flex w-full ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-[85%] p-3.5 text-sm leading-relaxed shadow-lg ${msg.sender === 'user'
                            ? 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white rounded-2xl rounded-tr-sm'
                            : 'bg-gray-800 text-gray-200 border border-gray-700 rounded-2xl rounded-tl-sm'
                          }`}
                      >
                        {msg.text}
                      </div>
                    </motion.div>
                  ))}

                  {isTyping && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      className="flex justify-start w-full"
                    >
                      <div className="bg-gray-800 border border-gray-700/80 rounded-2xl rounded-tl-sm p-4 flex gap-1.5 items-center shadow-md">
                        <motion.div animate={{ y: [0, -5, 0] }} transition={{ duration: 0.6, repeat: Infinity, delay: 0 }} className="w-2.5 h-2.5 rounded-full bg-cyan-400/80"></motion.div>
                        <motion.div animate={{ y: [0, -5, 0] }} transition={{ duration: 0.6, repeat: Infinity, delay: 0.2 }} className="w-2.5 h-2.5 rounded-full bg-cyan-400/80"></motion.div>
                        <motion.div animate={{ y: [0, -5, 0] }} transition={{ duration: 0.6, repeat: Infinity, delay: 0.4 }} className="w-2.5 h-2.5 rounded-full bg-cyan-400/80"></motion.div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
                <div ref={messagesEndRef} />
              </div>
            </div>

            {/* Input Area */}
            <div className="p-4 bg-gray-900 border-t border-gray-800 relative z-10 shadow-[0_-10px_30px_rgba(0,0,0,0.5)]">
              <div className="relative flex items-center">
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                  placeholder="Ask about UCaaS..."
                  className="w-full bg-gray-800 border-2 border-transparent text-white text-sm rounded-full py-3 pl-5 pr-12 focus:outline-none focus:border-cyan-500/50 focus:bg-gray-800/80 transition-all placeholder-gray-500 shadow-inner"
                />
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={handleSend}
                  disabled={!inputValue.trim()}
                  className={`absolute right-1.5 w-9 h-9 rounded-full flex items-center justify-center transition-all ${inputValue.trim()
                      ? 'bg-gradient-to-r from-cyan-500 to-blue-500 text-white shadow-[0_0_10px_rgba(6,182,212,0.6)]'
                      : 'bg-gray-700 text-gray-500 opacity-50 cursor-not-allowed'
                    }`}
                >
                  <Send size={16} className={inputValue.trim() ? "translate-x-0.5" : ""} />
                </motion.button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <style dangerouslySetInnerHTML={{
        __html: `
        .custom-scrollbar::-webkit-scrollbar {
          width: 5px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent; 
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(6, 182, 212, 0.3); 
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(6, 182, 212, 0.6); 
        }
      `}} />
    </div>
  );
};

const rootNode = document.getElementById('chatbot-root');
if (rootNode) {
  const root = createRoot(rootNode);
  root.render(<Chatbot />);
}
