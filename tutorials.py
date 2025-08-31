import React, { useState, useEffect } from "react";
import { Tutorial, UserProgress, User } from "@/entities/all";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { 
  BookOpen, 
  Clock, 
  Search, 
  Filter,
  Play,
  CheckCircle,
  ArrowRight,
  Star,
  Code
} from "lucide-react";
import { Link } from "react-router-dom";
import { createPageUrl } from "@/utils";

export default function Tutorials() {
  const [tutorials, setTutorials] = useState([]);
  const [userProgress, setUserProgress] = useState([]);
  const [userProfile, setUserProfile] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('all');
  const [selectedLevel, setSelectedLevel] = useState('all');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadTutorialsAndProgress();
  }, []);

  const loadTutorialsAndProgress = async () => {
    setIsLoading(true);
    try {
      const user = await User.me();
      setUserProfile(user);

      const allTutorials = await Tutorial.list('order_index');
      setTutorials(allTutorials);

      const progress = await UserProgress.filter(
        { created_by: user.email },
        '-updated_date'
      );
      setUserProgress(progress);
    } catch (error) {
      console.error('Error loading tutorials:', error);
    }
    setIsLoading(false);
  };

  const getProgressForTutorial = (tutorialId) => {
    return userProgress.find(p => p.tutorial_id === tutorialId);
  };

  const getCompletionPercentage = () => {
    if (tutorials.length === 0) return 0;
    const completedCount = userProgress.filter(p => p.completion_status === 'completed').length;
    return Math.round((completedCount / tutorials.length) * 100);
  };

  const filteredTutorials = tutorials.filter(tutorial => {
    const matchesSearch = tutorial.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         tutorial.description?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesLanguage = selectedLanguage === 'all' || tutorial.programming_language === selectedLanguage;
    const matchesLevel = selectedLevel === 'all' || tutorial.difficulty_level === selectedLevel;
    
    return matchesSearch && matchesLanguage && matchesLevel;
  });

  const getDifficultyColor = (level) => {
    switch (level) {
      case 'beginner': return 'bg-green-100 text-green-800';
      case 'intermediate': return 'bg-yellow-100 text-yellow-800';
      case 'advanced': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getLanguageColor = (language) => {
    switch (language) {
      case 'python': return 'bg-blue-100 text-blue-800';
      case 'javascript': return 'bg-orange-100 text-orange-800';
      case 'java': return 'bg-red-100 text-red-800';
      case 'cpp': return 'bg-purple-100 text-purple-800';
      case 'html_css': return 'bg-pink-100 text-pink-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (isLoading) {
    return (
      <div className="p-6 md:p-8">
        <div className="max-w-7xl mx-auto space-y-6">
          {Array(6).fill(0).map((_, i) => (
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
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
            Interactive Tutorials
          </h1>
          <p className="text-lg text-gray-600">
            Learn programming step by step with voice-guided tutorials
          </p>
        </div>

        {/* Progress Overview */}
        <Card className="mb-8 shadow-lg border-0 bg-gradient-to-r from-indigo-500 to-purple-600 text-white">
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <h3 className="text-xl font-bold mb-2">Your Learning Progress</h3>
                <p className="text-indigo-100">
                  {userProgress.filter(p => p.completion_status === 'completed').length} of {tutorials.length} tutorials completed
                </p>
              </div>
              <div className="w-full md:w-64">
                <div className="flex justify-between text-sm mb-2">
                  <span>Overall Progress</span>
                  <span>{getCompletionPercentage()}%</span>
                </div>
                <div className="bg-white/20 rounded-full h-3">
                  <div 
                    className="bg-white rounded-full h-3 transition-all duration-500"
                    style={{ width: `${getCompletionPercentage()}%` }}
                  />
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Filters */}
        <Card className="mb-8 shadow-lg border-0">
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row gap-4 items-start md:items-center">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <Input
                  placeholder="Search tutorials..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              
              <div className="flex items-center gap-3">
                <Filter className="w-4 h-4 text-gray-500" />
                
                <Select value={selectedLanguage} onValueChange={setSelectedLanguage}>
                  <SelectTrigger className="w-40">
                    <SelectValue placeholder="Language" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Languages</SelectItem>
                    <SelectItem value="python">Python</SelectItem>
                    <SelectItem value="javascript">JavaScript</SelectItem>
                    <SelectItem value="java">Java</SelectItem>
                    <SelectItem value="cpp">C++</SelectItem>
                    <SelectItem value="html_css">HTML/CSS</SelectItem>
                  </SelectContent>
                </Select>

                <Select value={selectedLevel} onValueChange={setSelectedLevel}>
                  <SelectTrigger className="w-32">
                    <SelectValue placeholder="Level" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Levels</SelectItem>
                    <SelectItem value="beginner">Beginner</SelectItem>
                    <SelectItem value="intermediate">Intermediate</SelectItem>
                    <SelectItem value="advanced">Advanced</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Tutorial Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredTutorials.map((tutorial) => {
            const progress = getProgressForTutorial(tutorial.id);
            const isCompleted = progress?.completion_status === 'completed';
            const isInProgress = progress?.completion_status === 'in_progress';
            
            return (
              <Card key={tutorial.id} className="shadow-lg border-0 hover:shadow-xl transition-all duration-300 group">
                <CardHeader className="pb-4">
                  <div className="flex justify-between items-start gap-3">
                    <div className="flex-1">
                      <CardTitle className="text-lg font-bold mb-2 group-hover:text-blue-600 transition-colors">
                        {tutorial.title}
                      </CardTitle>
                      <p className="text-sm text-gray-600 line-clamp-2">
                        {tutorial.description}
                      </p>
                    </div>
                    {isCompleted && (
                      <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                        <CheckCircle className="w-5 h-5 text-green-600" />
                      </div>
                    )}
                  </div>
                  
                  <div className="flex flex-wrap gap-2 mt-3">
                    <Badge className={getLanguageColor(tutorial.programming_language)}>
                      {tutorial.programming_language?.toUpperCase()}
                    </Badge>
                    <Badge className={getDifficultyColor(tutorial.difficulty_level)}>
                      {tutorial.difficulty_level}
                    </Badge>
                    {tutorial.estimated_duration && (
                      <Badge variant="outline" className="flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {tutorial.estimated_duration}m
                      </Badge>
                    )}
                  </div>
                </CardHeader>

                <CardContent className="pt-0">
                  {/* Progress bar for in-progress tutorials */}
                  {isInProgress && progress?.mastery_score && (
                    <div className="mb-4">
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-gray-600">Progress</span>
                        <span className="text-blue-600 font-medium">{progress.mastery_score}%</span>
                      </div>
                      <Progress value={progress.mastery_score} className="h-2" />
                    </div>
                  )}

                  {/* Concepts covered */}
                  {tutorial.concepts_covered && tutorial.concepts_covered.length > 0 && (
                    <div className="mb-4">
                      <h4 className="text-sm font-medium text-gray-700 mb-2">What you'll learn:</h4>
                      <div className="flex flex-wrap gap-1">
                        {tutorial.concepts_covered.slice(0, 3).map((concept, index) => (
                          <Badge key={index} variant="outline" className="text-xs">
                            {concept}
                          </Badge>
                        ))}
                        {tutorial.concepts_covered.length > 3 && (
                          <Badge variant="outline" className="text-xs">
                            +{tutorial.concepts_covered.length - 3} more
                          </Badge>
                        )}
                      </div>
                    </div>
                  )}

                  <div className="flex justify-between items-center">
                    <div className="flex items-center gap-2">
                      {isCompleted ? (
                        <div className="flex items-center gap-2 text-green-600">
                          <Star className="w-4 h-4" />
                          <span className="text-sm font-medium">Completed</span>
                        </div>
                      ) : (
                        <div className="flex items-center gap-2 text-gray-500">
                          <Code className="w-4 h-4" />
                          <span className="text-sm">Ready to learn</span>
                        </div>
                      )}
                    </div>
                    
                    <Button 
                      size="sm" 
                      className="bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white"
                    >
                      {isCompleted ? 'Review' : isInProgress ? 'Continue' : 'Start'}
                      <ArrowRight className="w-4 h-4 ml-1" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {filteredTutorials.length === 0 && (
          <Card className="text-center py-12">
            <CardContent>
              <BookOpen className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-600 mb-2">No tutorials found</h3>
              <p className="text-gray-500">
                Try adjusting your search filters or check back later for new content.
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}