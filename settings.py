import React, { useState, useEffect } from "react";
import { User } from "@/entities/all";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Slider } from "@/components/ui/slider";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { 
  Settings as SettingsIcon,
  Mic,
  Volume2,
  Code,
  User as UserIcon,
  CheckCircle,
  Info
} from "lucide-react";

export default function Settings() {
  const [userProfile, setUserProfile] = useState(null);
  const [settings, setSettings] = useState({
    voice_enabled: true,
    speech_rate: 1.0,
    preferred_language: 'python',
    programming_level: 'beginner'
  });
  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadUserSettings();
  }, []);

  const loadUserSettings = async () => {
    setIsLoading(true);
    try {
      const user = await User.me();
      setUserProfile(user);
      setSettings({
        voice_enabled: user.voice_enabled ?? true,
        speech_rate: user.speech_rate ?? 1.0,
        preferred_language: user.preferred_language ?? 'python',
        programming_level: user.programming_level ?? 'beginner'
      });
    } catch (error) {
      console.error('Error loading user settings:', error);
    }
    setIsLoading(false);
  };

  const handleSaveSettings = async () => {
    setIsSaving(true);
    setSaveMessage('');
    
    try {
      await User.updateMyUserData(settings);
      setSaveMessage('Settings saved successfully!');
      
      // Update local state
      setUserProfile(prev => ({ ...prev, ...settings }));
      
      // Clear message after 3 seconds
      setTimeout(() => setSaveMessage(''), 3000);
    } catch (error) {
      console.error('Error saving settings:', error);
      setSaveMessage('Failed to save settings. Please try again.');
    }
    
    setIsSaving(false);
  };

  const testSpeech = () => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel(); // Cancel any ongoing speech
      const utterance = new SpeechSynthesisUtterance(
        "Hello! This is a test of your text-to-speech settings. The speech rate is currently set to " + settings.speech_rate + ". How does this sound?"
      );
      utterance.rate = settings.speech_rate;
      utterance.pitch = 1;
      utterance.volume = 0.8;
      window.speechSynthesis.speak(utterance);
    }
  };

  if (isLoading) {
    return (
      <div className="p-6 md:p-8">
        <div className="max-w-4xl mx-auto space-y-6">
          {Array(3).fill(0).map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardContent className="h-32 bg-gray-100 rounded" />
            </Card>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 p-6 md:p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
            Voice & Learning Settings
          </h1>
          <p className="text-lg text-gray-600">
            Customize your learning experience and voice preferences
          </p>
        </div>

        {saveMessage && (
          <Alert className={`mb-6 ${saveMessage.includes('successfully') ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'}`}>
            <CheckCircle className="h-4 w-4" />
            <AlertDescription className={saveMessage.includes('successfully') ? 'text-green-700' : 'text-red-700'}>
              {saveMessage}
            </AlertDescription>
          </Alert>
        )}

        <div className="space-y-6">
          {/* Profile Settings */}
          <Card className="shadow-lg border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <UserIcon className="w-5 h-5 text-blue-500" />
                Profile Settings
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label htmlFor="programming_level">Programming Level</Label>
                  <Select 
                    value={settings.programming_level} 
                    onValueChange={(value) => setSettings(prev => ({ ...prev, programming_level: value }))}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select your level" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="beginner">
                        <div className="flex items-center gap-2">
                          <div className="w-3 h-3 bg-green-400 rounded-full" />
                          Beginner - Just starting out
                        </div>
                      </SelectItem>
                      <SelectItem value="intermediate">
                        <div className="flex items-center gap-2">
                          <div className="w-3 h-3 bg-yellow-400 rounded-full" />
                          Intermediate - Some experience
                        </div>
                      </SelectItem>
                      <SelectItem value="advanced">
                        <div className="flex items-center gap-2">
                          <div className="w-3 h-3 bg-red-400 rounded-full" />
                          Advanced - Experienced developer
                        </div>
                      </SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="preferred_language">Preferred Programming Language</Label>
                  <Select 
                    value={settings.preferred_language} 
                    onValueChange={(value) => setSettings(prev => ({ ...prev, preferred_language: value }))}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select language" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="python">
                        <div className="flex items-center gap-2">
                          <Code className="w-4 h-4" />
                          Python
                        </div>
                      </SelectItem>
                      <SelectItem value="javascript">
                        <div className="flex items-center gap-2">
                          <Code className="w-4 h-4" />
                          JavaScript
                        </div>
                      </SelectItem>
                      <SelectItem value="java">
                        <div className="flex items-center gap-2">
                          <Code className="w-4 h-4" />
                          Java
                        </div>
                      </SelectItem>
                      <SelectItem value="cpp">
                        <div className="flex items-center gap-2">
                          <Code className="w-4 h-4" />
                          C++
                        </div>
                      </SelectItem>
                      <SelectItem value="html_css">
                        <div className="flex items-center gap-2">
                          <Code className="w-4 h-4" />
                          HTML/CSS
                        </div>
                      </SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Voice Settings */}
          <Card className="shadow-lg border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Mic className="w-5 h-5 text-purple-500" />
                Voice Settings
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Voice Enable/Disable */}
              <div className="flex items-center justify-between p-4 bg-purple-50 rounded-lg">
                <div className="flex-1">
                  <Label htmlFor="voice_enabled" className="text-base font-medium">
                    Enable Voice Features
                  </Label>
                  <p className="text-sm text-gray-600 mt-1">
                    Turn on voice recognition and text-to-speech for a hands-free learning experience
                  </p>
                </div>
                <Switch
                  id="voice_enabled"
                  checked={settings.voice_enabled}
                  onCheckedChange={(checked) => setSettings(prev => ({ ...prev, voice_enabled: checked }))}
                />
              </div>

              {/* Speech Rate */}
              {settings.voice_enabled && (
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="speech_rate" className="text-base font-medium">
                      Speech Rate: {settings.speech_rate}x
                    </Label>
                    <p className="text-sm text-gray-600 mb-3">
                      Adjust how fast the AI speaks explanations
                    </p>
                    <Slider
                      id="speech_rate"
                      min={0.5}
                      max={2.0}
                      step={0.1}
                      value={[settings.speech_rate]}
                      onValueChange={([value]) => setSettings(prev => ({ ...prev, speech_rate: value }))}
                      className="w-full"
                    />
                    <div className="flex justify-between text-sm text-gray-500 mt-1">
                      <span>Slower (0.5x)</span>
                      <span>Normal (1.0x)</span>
                      <span>Faster (2.0x)</span>
                    </div>
                  </div>

                  {/* Test Speech */}
                  <div className="flex items-center gap-3">
                    <Button 
                      variant="outline" 
                      onClick={testSpeech}
                      className="flex items-center gap-2"
                    >
                      <Volume2 className="w-4 h-4" />
                      Test Speech
                    </Button>
                    <p className="text-sm text-gray-500">
                      Click to hear how your settings sound
                    </p>
                  </div>
                </div>
              )}

              {!('speechSynthesis' in window || 'SpeechRecognition' in window || 'webkitSpeechRecognition' in window) && (
                <Alert>
                  <Info className="h-4 w-4" />
                  <AlertDescription>
                    Voice features may not be fully supported in this browser. 
                    For the best experience, use Chrome, Edge, or Safari.
                  </AlertDescription>
                </Alert>
              )}
            </CardContent>
          </Card>

          {/* Privacy & Data */}
          <Card className="shadow-lg border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <SettingsIcon className="w-5 h-5 text-gray-500" />
                Privacy & Data
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h4 className="font-semibold text-blue-900 mb-2">Your Learning Data</h4>
                <p className="text-sm text-blue-800">
                  We store your debugging sessions and tutorial progress to provide personalized learning recommendations. 
                  Your code snippets are processed by AI to provide better explanations but are not permanently stored.
                </p>
              </div>
              
 