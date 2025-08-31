import React, { useRef, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { 
  AlertTriangle, 
  Lightbulb, 
  Code2, 
  ThumbsUp, 
  ThumbsDown,
  Volume2,
  BookOpen,
  Copy
} from "lucide-react";
import { Separator } from "@/components/ui/separator";
import ReactMarkdown from 'react-markdown';

export default function ErrorExplanation({ 
  explanation, 
  onRate, 
  onSpeak,
  isLoading 
}) {
  const explanationRef = useRef(null);

  useEffect(() => {
    if (explanation && explanationRef.current) {
      explanationRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [explanation]);

  const copyExplanation = () => {
    if (explanation) {
      navigator.clipboard.writeText(
        `Error: ${explanation.error_type}\n\nExplanation: ${explanation.simple_explanation}\n\nSolution: ${explanation.solution}`
      );
    }
  };

  const handleSpeak = () => {
    if (!explanation) return;
    
    // Direct text-to-speech implementation
    if ('speechSynthesis' in window) {
      // Stop any ongoing speech
      window.speechSynthesis.cancel();
      
      const textToSpeak = `I found a ${explanation.error_type}. Here is what's wrong: ${explanation.simple_explanation}. And here is how to fix it: ${explanation.solution}`;
      
      const utterance = new SpeechSynthesisUtterance(textToSpeak);
      utterance.rate = 1.0;
      utterance.pitch = 1;
      utterance.volume = 0.9;
      
      // Add some debugging
      utterance.onstart = () => console.log('Speech started');
      utterance.onend = () => console.log('Speech ended');
      utterance.onerror = (e) => console.error('Speech error:', e);
      
      window.speechSynthesis.speak(utterance);
    } else {
      alert('Text-to-speech is not supported in this browser. Please try Chrome, Edge, or Safari.');
    }
  };

  if (isLoading) {
    return (
      <Card ref={explanationRef} className="shadow-lg border-0 bg-gradient-to-r from-blue-50 to-indigo-50">
        <CardContent className="p-8">
          <div className="flex items-center justify-center space-x-3">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500" />
            <p className="text-blue-700 font-medium">Analyzing your code with AI...</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!explanation) return null;

  return (
    <Card ref={explanationRef} className="shadow-lg border-0 bg-gradient-to-r from-amber-50 to-orange-50 border-l-4 border-l-amber-400">
      <CardHeader className="pb-4">
        <div className="flex justify-between items-start">
          <CardTitle className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-r from-amber-500 to-orange-500 rounded-xl flex items-center justify-center">
              <AlertTriangle className="w-5 h-5 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-gray-900">Code Analysis Results</h3>
              <Badge className="mt-1 bg-amber-100 text-amber-800">
                {explanation.error_type || 'Code Issue Detected'}
              </Badge>
            </div>
          </CardTitle>
          
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleSpeak}
              className="flex items-center gap-2"
            >
              <Volume2 className="w-4 h-4" />
              Listen
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={copyExplanation}
              className="flex items-center gap-2"
            >
              <Copy className="w-4 h-4" />
              Copy
            </Button>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Simple Explanation */}
        <div className="bg-white/70 rounded-xl p-6 border border-amber-200">
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
              <Lightbulb className="w-4 h-4 text-blue-600" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-2">What's Wrong?</h4>
              <div className="text-gray-700 prose prose-sm">
                <ReactMarkdown>{explanation.simple_explanation}</ReactMarkdown>
              </div>
            </div>
          </div>
        </div>

        {/* Solution */}
        <div className="bg-white/70 rounded-xl p-6 border border-green-200">
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
              <Code2 className="w-4 h-4 text-green-600" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-2">How to Fix It</h4>
              <div className="text-gray-700 prose prose-sm">
                <ReactMarkdown>{explanation.solution}</ReactMarkdown>
              </div>
            </div>
          </div>
        </div>

        {/* Learning Points */}
        {explanation.learning_points && explanation.learning_points.length > 0 && (
          <div className="bg-white/70 rounded-xl p-6 border border-purple-200">
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <BookOpen className="w-4 h-4 text-purple-600" />
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 mb-3">Key Learning Points</h4>
                <div className="space-y-2">
                  {explanation.learning_points.map((point, index) => (
                    <div key={index} className="flex items-start gap-2 text-gray-700">
                      <div className="w-2 h-2 bg-purple-400 rounded-full mt-2 flex-shrink-0" />
                      <span>{point}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        <Separator />

        {/* Rating */}
        <div className="flex justify-between items-center">
          <p className="text-sm text-gray-600">Was this explanation helpful?</p>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => onRate && onRate(5)}
              className="flex items-center gap-2 hover:bg-green-50 hover:text-green-700"
            >
              <ThumbsUp className="w-4 h-4" />
              Yes, helpful!
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => onRate && onRate(2)}
              className="flex items-center gap-2 hover:bg-red-50 hover:text-red-700"
            >
              <ThumbsDown className="w-4 h-4" />
              Needs improvement
            </Button>
 