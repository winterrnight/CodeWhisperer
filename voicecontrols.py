import React, { useState, useRef, useEffect, useCallback, forwardRef, useImperativeHandle } from 'react';
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Mic, MicOff, Volume2, VolumeX } from "lucide-react";
import { Badge } from "@/components/ui/badge";

const VoiceControls = forwardRef(({ 
  onSpeechResult, 
  voiceEnabled, 
  speechRate = 1.0 
}, ref) => {
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(false);
  const recognitionRef = useRef(null);

  const speak = useCallback((text) => {
    if (!voiceEnabled || !('speechSynthesis' in window)) return;

    // Stop any ongoing speech
    window.speechSynthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = speechRate;
    utterance.pitch = 1;
    utterance.volume = 0.8;
    
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);
    
    window.speechSynthesis.speak(utterance);
  }, [voiceEnabled, speechRate]);

  const stopSpeaking = useCallback(() => {
    window.speechSynthesis.cancel();
    setIsSpeaking(false);
  }, []);

  // Expose speak function to parent component
  useImperativeHandle(ref, () => ({
    speak,
    stopSpeaking
  }), [speak, stopSpeaking]);

  useEffect(() => {
    // Check for speech recognition support
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    setSpeechSupported(!!SpeechRecognition);

    if (SpeechRecognition) {
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'en-US';

      recognitionRef.current.onstart = () => {
        setIsListening(true);
      };

      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        onSpeechResult && onSpeechResult(transcript);
        setIsListening(false);
      };

      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
    }
  }, [onSpeechResult]);

  const startListening = () => {
    if (recognitionRef.current && !isListening) {
      recognitionRef.current.start();
    }
  };

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    }
  };

  if (!speechSupported && !('speechSynthesis' in window)) {
    return (
      <Card className="border-amber-200 bg-amber-50">
        <CardContent className="p-4">
          <p className="text-sm text-amber-700">
            Voice features are not supported in this browser. Please try Chrome, Edge, or Safari for the best experience.
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="flex items-center gap-3">
      <Button
        variant={isListening ? "default" : "outline"}
        size="sm"
        onClick={isListening ? stopListening : startListening}
        disabled={!voiceEnabled || !speechSupported}
        className={`flex items-center gap-2 ${
          isListening ? 'bg-red-500 hover:bg-red-600 text-white animate-pulse' : ''
        }`}
      >
        {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
        {isListening ? 'Stop Listening' : 'Start Voice'}
      </Button>

      <Button
        variant={isSpeaking ? "default" : "outline"}
        size="sm"
        onClick={isSpeaking ? stopSpeaking : undefined}
        disabled={!voiceEnabled || !isSpeaking}
        className={isSpeaking ? 'bg-blue-500 hover:bg-blue-600 text-white' : ''}
      >
        {isSpeaking ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
        {isSpeaking ? 'Stop Speaking' : 'Text-to-Speech'}
      </Button>

      {isListening && (
        <Badge variant="secondary" className="animate-pulse">
          Listening...
        </Badge>
      )}
      
      {isSpeaking && (
        <Badge variant="secondary" className="animate-pulse">
          Speaking...
        </Badge>
      )}
    </div>
  );
});

export default VoiceControls;