import React, { useState, useEffect } from "react";
import { User, DebuggingSession, Tutorial, UserProgress } from "@/entities/all";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Link } from "react-router-dom";
import { createPageUrl } from "@/utils";
import {
  Code,
  BookOpen,
  TrendingUp,
  Clock,
  Award,
  Target,
  Brain,
  Zap,
  Play,
  Mic
} from "lucide-react";
import { format } from "date-fns";

export default function Dashboard() {
  const [userProfile, setUserProfile] = useState(null);
  const [recentSessions, setRecentSessions] = useState([]);
  const [userProgress, setUserProgress] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setIsLoading(true);
    try {
      const user = await User.me();
      setUserProfile(user);

      const sessions = await DebuggingSession.filter(
        { created_by: user.email },
        '-created_date',
        5
      );
      setRecentSessions(sessions);

      const progress = await UserProgress.filter(
        { created_by: user.email },
        '-updated_date',
        10
      );
      setUserProgress(progress);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    }
    setIsLoading(false);
  };

  const getStreakStatus = () => {
    const streak = userProfile?.learning_streak || 0;
    if (streak >= 7) return { text: 'On Fire! 🔥', color: 'bg-red-100 text-red-800' };
    if (streak >= 3) return { text: 'Great Momentum!', color: 'bg-green-100 text-green-800' };
    if (streak >= 1) return { text: 'Getting Started', color: 'bg-blue-100 text-blue-800' };
    return { text: 'Ready to Learn', color: 'bg-gray-100 text-gray-800' };
  };

  const getLevelProgress = () => {
    const totalSessions = userProfile?.total_sessions || 0;
    if (totalSessions >= 50) return { level: 'Advanced', progress: 100 };
    if (totalSessions >= 20) return { level: 'Intermediate', progress: (totalSessions / 50) * 100 };
    return { level: 'Beginner', progress: (totalSessions / 20) * 100 };
  };

  if (isLoading) {
    return (
      <div className="p-6 md:p-8">
        <div className="max-w-7xl mx-auto space-y-6">
          {Array(4).fill(0).map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardContent className="h-32 bg-gray-100 rounded" />
            </Card>
          ))}
        </div>
      </div>
    );
  }

  const streakStatus = getStreakStatus();
  const levelProgress = getLevelProgress();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 p-6 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Welcome Header */}
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
            Welcome back! 👋
          </h1>
          <p className="text-lg text-gray-600">
            Ready to continue your coding journey? Let's debug some code together!
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-blue-100 text-sm font-medium">Learning Streak</p>
                  <p className="text-3xl font-bold">{userProfile?.learning_streak || 0}</p>
                  <Badge className={`mt-2 ${streakStatus.color}`}>
                    {streakStatus.text}
                  </Badge>
                </div>
                <Award className="w-10 h-10 text-blue-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-green-500 to-emerald-600 text-white border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-green-100 text-sm font-medium">Total Sessions</p>
                  <p className="text-3xl font-bold">{userProfile?.total_sessions || 0}</p>
                  <p className="text-green-100 text-sm">Debugging sessions</p>
                </div>
                <Code className="w-10 h-10 text-green-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-purple-500 to-pink-600 text-white border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-purple-100 text-sm font-medium">Skill Level</p>
                  <p className="text-2xl font-bold">{levelProgress.level}</p>
                  <div className="mt-2 bg-white/20 rounded-full h-2">
                    <div 
                      className="bg-white rounded-full h-2 transition-all duration-500"
                      style={{ width: `${levelProgress.progress}%` }}
                    />
                  </div>
                </div>
                <Target className="w-10 h-10 text-purple-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-orange-500 to-red-600 text-white border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-orange-100 text-sm font-medium">Preferred Language</p>
                  <p className="text-xl font-bold">
                    {userProfile?.preferred_language?.toUpperCase() || 'PYTHON'}
                  </p>
                  <p className="text-orange-100 text-sm">Primary focus</p>
                </div>
                <Brain className="w-10 h-10 text-orange-200" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="grid lg:grid-cols-3 gap-6 mb-8">
          <Card className="lg:col-span-2 shadow-lg border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Zap className="w-5 h-5 text-blue-500" />
                Quick Start
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid md:grid-cols-2 gap-4">
                <Link to={createPageUrl("Debugger")}>
                  <Button className="w-full h-20 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white">
                    <div className="text-center">
                      <Code className="w-6 h-6 mx-auto mb-2" />
                      <div className="font-semibold">Start Debugging</div>
                      <div className="text-xs opacity-80">Get instant help with errors</div>
                    </div>
                  </Button>
                </Link>

                <Link to={createPageUrl("Tutorials")}>
                  <Button variant="outline" className="w-full h-20 hover:bg-purple-50 hover:text-purple-700">
                    <div className="text-center">
                      <BookOpen className="w-6 h-6 mx-auto mb-2" />
                      <div className="font-semibold">Browse Tutorials</div>
                      <div className="text-xs opacity-60">Learn step by step</div>
                    </div>
                  </Button>
                </Link>
              </div>

              {userProfile?.voice_enabled && (
                <div className="bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-lg p-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                      <Mic className="w-5 h-5 text-green-600" />
                    </div>
                    <div>
                      <p className="font-semibold text-green-800">Voice Features Enabled</p>
                      <p className="text-sm text-green-600">You can speak your questions and hear explanations!</p>
                    </div>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Recent Activity */}
          <Card className="shadow-lg border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Clock className="w-5 h-5 text-purple-500" />
                Recent Activity
              </CardTitle>
            </CardHeader>
            <CardContent>
              {recentSessions.length > 0 ? (
                <div className="space-y-3">
                  {recentSessions.map((session) => (
                    <div key={session.id} className="p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center justify-between mb-1">
                        <Badge className="bg-blue-100 text-blue-800 text-xs">
                          {session.programming_language}
                        </Badge>
                        <span className="text-xs text-gray-500">
                          {format(new Date(session.created_date), 'MMM d')}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 line-clamp-2">
                        {session.explanation_provided?.slice(0, 60) || 'Debugging session completed'}...
                      </p>
                      {session.voice_used && (
                        <div className="flex items-center gap-1 mt-1">
                          <Mic className="w-3 h-3 text-green-500" />
                          <span className="text-xs text-green-600">Voice used</span>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-6">
                  <Code className="w-12 h-12 text-gray-300 mx-auto mb-3" />
                  <p className="text-gray-500">No debugging sessions yet</p>
                  <p className="text-sm text-gray-400">Start your first session!</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Daily Tip */}
        <Card className="shadow-lg border-0 bg-gradient-to-r from-yellow-50 to-amber-50 border-l-4 border-l-yellow-400">
          <CardContent className="p-6">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 bg-yellow-100 rounded-xl flex items-center justify-center flex-shrink-0">
                <Brain className="w-6 h-6 text-yellow-600" />
              </div>
              <div>
                <h3 className="font-bold text-gray-900 mb-2">💡 Daily Learning Tip</h3>
                <p className="text-gray-700 mb-3">
                  When debugging, read error messages carefully - they often tell you exactly what's wrong and where! 
                  Don't just copy-paste solutions; understand why they work.
                </p>
                <Link to={createPageUrl("Tutorials")}>
                  <Button variant="outline" size="sm" className="flex items-center gap-2">
                    <Play className="w-4 h-4" />
                    Learn More
                  </Button>
                </Link>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}