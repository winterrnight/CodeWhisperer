
import React, { useState, useRef, useEffect } from "react";
import { User, DebuggingSession } from "@/entities/all";
import { InvokeLLM } from "@/integrations/Core";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { AlertCircle, ArrowLeft } from "lucide-react";
import { Link } from "react-router-dom";
import { createPageUrl } from "@/utils";

import VoiceControls from "../components/voice/VoiceControls";
import CodeEditor from "../components/debugger/CodeEditor";
import ErrorExplanation from "../components/debugger/ErrorExplanation";

export default function Debugger() {
  const [userProfile, setUserProfile] = useState(null);
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [explanation, setExplanation] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState(null);
  const voiceControlsRef = useRef(null);

  useEffect(() => {
    loadUserProfile();
    // Set initial code example
    setCode(`# Example Python code with an error
def greet_user(name):
    print("Hello " + name)
    return name.upper()

# This will cause an error
result = greet_user()  # Missing required argument
print(result)`);
  }, []);

  const loadUserProfile = async () => {
    try {
      const user = await User.me();
      setUserProfile(user);
      setLanguage(user.preferred_language || 'python');
    } catch (error) {
      console.error('Error loading user profile:', error);
    }
  };

  const handleVoiceInput = (transcript) => {
    // Simple voice commands
    const lowerTranscript = transcript.toLowerCase();
    
    if (lowerTranscript.includes('analyze') || lowerTranscript.includes('help')) {
      handleAnalyzeCode();
    } else if (lowerTranscript.includes('clear')) {
      setCode('');
      setExplanation(null);
    } else if (lowerTranscript.includes('explain again') && explanation) {
      speakExplanation();
    } else {
      // Treat as code input
      setCode(prev => prev + '\n' + transcript);
    }
  };

  const speakExplanation = () => {
    if (explanation && voiceControlsRef.current) {
      const textToSpeak = `I found a ${explanation.error_type}. Here is what's wrong: ${explanation.simple_explanation}. And here is how to fix it: ${explanation.solution}`;
      voiceControlsRef.current.speak(textToSpeak);
    }
  };

  const handleAnalyzeCode = async () => {
    if (!code.trim()) {
      setError('Please enter some code to analyze');
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setExplanation(null);

    try {
      const prompt = `
        You are a friendly programming tutor helping a ${userProfile?.programming_level || 'beginner'} programmer.
        
        Analyze this ${language} code and identify any errors or potential issues:
        
        \`\`\`${language}
        ${code}
        \`\`\`
        
        Please provide:
        1. A clear identification of any errors or issues
        2. A beginner-friendly explanation in simple terms
        3. Step-by-step solution with code examples
        4. Key learning points to remember
        
        Focus on being encouraging and educational rather than just providing fixes.
        If the code looks correct, explain what it does and suggest improvements.
      `;

      const response = await InvokeLLM({
        prompt,
        response_json_schema: {
          type: "object",
          properties: {
            error_type: {
              type: "string",
              description: "Type of error or 'No errors found' if code is correct"
            },
            simple_explanation: {
              type: "string",
              description: "Beginner-friendly explanation of the issue"
            },
            solution: {
              type: "string",
              description: "Step-by-step solution with code examples"
            },
            learning_points: {
              type: "array",
              items: {
                type: "string"
              },
              description: "Key concepts to remember"
            }
          }
        }
      });

      setExplanation(response);

      // Save debugging session
      await DebuggingSession.create({
        code_input: code,
        programming_language: language,
        explanation_provided: response.simple_explanation,
        solution_suggested: response.solution,
        voice_used: userProfile?.voice_enabled || false,
        concepts_learned: response.learning_points || []
      });

      // Update user's session count
      if (userProfile) {
        await User.updateMyUserData({
          total_sessions: (userProfile.total_sessions || 0) + 1
        });
      }

      // Auto-speak explanation if voice is enabled - with delay to ensure UI is rendered
      if (userProfile?.voice_enabled && voiceControlsRef.current) {
        setTimeout(() => {
          speakExplanation();
        }, 500);
      }

    } catch (error) {
      console.error('Error analyzing code:', error);
      setError('Failed to analyze code. Please try again.');
    }

    setIsAnalyzing(false);
  };

  const handleRateExplanation = async (rating) => {
    if (!explanation) return;
    
    try {
      // Find the most recent session and update it
      const recentSessions = await DebuggingSession.filter(
        { created_by: userProfile?.email },
        '-created_date',
        1
      );
      
      if (recentSessions.length > 0) {
        await DebuggingSession.update(recentSessions[0].id, {
          user_satisfaction: rating
        });
      }
    } catch (error) {
      console.error('Error rating explanation:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
          <div className="flex items-center gap-4">
            <Link to={createPageUrl("Dashboard")}>
              <Button variant="outline" size="icon">
                <ArrowLeft className="w-4 h-4" />
              </Button>
            </Link>
            <div>
              <h1 className="text-2xl md:text-3xl font-bold text-gray-900">
                Voice-Powered Code Debugger
              </h1>
              <p className="text-gray-600 mt-1">
                Paste your code, get instant AI-powered explanations with voice support
              </p>
            </div>
          </div>

          {userProfile?.voice_enabled && (
            <VoiceControls
              ref={voiceControlsRef}
              onSpeechResult={handleVoiceInput}
              voiceEnabled={userProfile.voice_enabled}
              speechRate={userProfile.speech_rate || 1.0}
            />
          )}
        </div>

        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <div className="space-y-6">
          {/* Code Editor */}
          <CodeEditor
            code={code}
            language={language}
            onCodeChange={setCode}
            onLanguageChange={setLanguage}
            onAnalyze={handleAnalyzeCode}
          />

          {/* Error Explanation */}
          <ErrorExplanation
            explanation={explanation}
            onRate={handleRateExplanation}
            onSpeak={speakExplanation}
            isLoading={isAnalyzing}
          />
        </div>
      </div>
    </div>
  );
}
