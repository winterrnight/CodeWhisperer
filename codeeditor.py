import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Play, Copy, RotateCcw } from "lucide-react";

const LANGUAGE_EXAMPLES = {
  python: `# Example Python code with an error
def greet_user(name):
    print("Hello " + name)
    return name.upper()

# This will cause an error
result = greet_user()  # Missing required argument
print(result)`,
  
  javascript: `// Example JavaScript code with an error
function calculateArea(radius) {
    return 3.14 * radius * radius;
}

// This will cause an error
let area = calculateArea();  // Missing required argument
console.log("Area is: " + area);`,

  java: `// Example Java code with an error
public class Main {
    public static void main(String[] args) {
        String name;
        System.out.println("Hello " + name);  // Variable not initialized
    }
}`,

  cpp: `// Example C++ code with an error
#include <iostream>
using namespace std;

int main() {
    int numbers[5] = {1, 2, 3, 4, 5};
    cout << numbers[10] << endl;  // Array index out of bounds
    return 0;
}`,

  html_css: `<!-- Example HTML/CSS with an error -->
<!DOCTYPE html>
<html>
<head>
    <style>
        .container {
            color: blue;
            background-color: #fff
            /* Missing semicolon above */
        }
    </style>
</head>
<body>
    <div class="container">
        <p>Hello World!</p>
    </div>
</body>
</html>`
};

export default function CodeEditor({ 
  code, 
  language, 
  onCodeChange, 
  onLanguageChange,
  onAnalyze 
}) {
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleLanguageChange = (newLanguage) => {
    onLanguageChange(newLanguage);
    onCodeChange(LANGUAGE_EXAMPLES[newLanguage] || '');
  };

  const handleAnalyze = async () => {
    setIsAnalyzing(true);
    await onAnalyze();
    setIsAnalyzing(false);
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(code);
  };

  const resetCode = () => {
    onCodeChange(LANGUAGE_EXAMPLES[language] || '');
  };

  return (
    <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
      <CardHeader className="pb-4">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <CardTitle className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
              <Play className="w-4 h-4 text-white" />
            </div>
            Code Playground
          </CardTitle>
          
          <div className="flex items-center gap-3">
            <Select value={language} onValueChange={handleLanguageChange}>
              <SelectTrigger className="w-40">
                <SelectValue placeholder="Language" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="python">
                  <div className="flex items-center gap-2">
                    <Badge className="bg-yellow-100 text-yellow-800">Python</Badge>
                  </div>
                </SelectItem>
                <SelectItem value="javascript">
                  <div className="flex items-center gap-2">
                    <Badge className="bg-orange-100 text-orange-800">JavaScript</Badge>
                  </div>
                </SelectItem>
                <SelectItem value="java">
                  <div className="flex items-center gap-2">
                    <Badge className="bg-red-100 text-red-800">Java</Badge>
                  </div>
                </SelectItem>
                <SelectItem value="cpp">
                  <div className="flex items-center gap-2">
                    <Badge className="bg-blue-100 text-blue-800">C++</Badge>
                  </div>
                </SelectItem>
                <SelectItem value="html_css">
                  <div className="flex items-center gap-2">
                    <Badge className="bg-green-100 text-green-800">HTML/CSS</Badge>
                  </div>
                </SelectItem>
              </SelectContent>
            </Select>

            <Button
              variant="outline"
              size="sm"
              onClick={copyToClipboard}
              className="flex items-center gap-2"
            >
              <Copy className="w-4 h-4" />
              Copy
            </Button>

            <Button
              variant="outline"
              size="sm"
              onClick={resetCode}
              className="flex items-center gap-2"
            >
              <RotateCcw className="w-4 h-4" />
              Reset
            </Button>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        <Textarea
          value={code}
          onChange={(e) => onCodeChange(e.target.value)}
          placeholder="Paste your code here or use the example above..."
          className="min-h-64 font-mono text-sm bg-gray-50 border-gray-200"
          style={{ fontFamily: 'Consolas, Monaco, "Courier New", monospace' }}
        />
        
        <div className="flex justify-between items-center">
          <p className="text-sm text-gray-500">
            Paste your code and click "Get Help" for voice-powered debugging assistance
          </p>
          
          <Button 
            onClick={handleAnalyze}
            disabled={isAnalyzing || !code.trim()}
            className="bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white px-8"
          >
            {isAnalyzing ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                Analyzing...
              </>
            ) : (
              <>
                <Play className="w-4 h-4 mr-2" />
                Get Help
              </>
            )}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}