import React, { useState, useEffect } from "react";
import { User, DebuggingSession, UserProgress, Tutorial } from "@/entities/all";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { 
  TrendingUp, 
  Award, 
  Target, 
  Calendar,
  Code,
  BookOpen,
  Brain,
  Mic,
  Clock,
  Star
} from "lucide-react";
import { format, parseISO, startOfWeek, eachDayOfInterval, endOfWeek } from "date-fns";

export default function ProgressPage() {
  const [userProfile, setUserProfile] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [progress, setProgress] = useState([]);
  const [tutorials, setTutorials] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadProgressData();
  }, []);

  const loadProgressData = async () => {
    setIsLoading(true);
    try {
      const user = await User.me();
      setUserProfile(user);

      const userSessions = await DebuggingSession.filter(
        { created_by: user.email },
        '-created_date',
        50
      );
      setSessions(userSessions);

      const userProgress = await UserProgress.filter(
        { created_by: user.email },
        '-updated_date'
      );
      setProgress(userProgress);

      const allTutorials = await Tutorial.list('order_index');
      setTutorials(allTutorials);
    } catch (error) {
      console.error('Error loading progress data:', error);
    }
    setIsLoading(false);
  };

  const getWeeklyActivity = () => {
    const now = new Date();
    const weekStart = startOfWeek(now);
    const weekEnd = endOfWeek(now);
    const weekDays = eachDayOfInterval({ start: weekStart, end: weekEnd });
    
    return weekDays.map(day => {
      const dayStr = format(day, 'yyyy-MM-dd');
      const sessionsCount = sessions.filter(session => 
        format(parseISO(session.created_date), 'yyyy-MM-dd') === dayStr
      ).length;
      
      return {
        day: format(day, 'EEE'),
        date: dayStr,
        sessions: sessionsCount
      };
    });
  };

  const getLanguageStats = () => {
    const languageCounts = {};
    sessions.forEach(session => {
      languageCounts[session.programming_language] = (languageCounts[session.programming_language] || 0) + 1;
    });
    
    return Object.entries(languageCounts)
      .map(([language, count]) => ({ language, count }))
      .sort((a, b) => b.count - a.count);
  };

  const getCompletionStats = () => {
    const completed = progress.filter(p => p.completion_status === 'completed').length;
    const inProgress = progress.filter(p => p.completion_status === 'in_progress').length;
    const total = tutorials.length;
    
    return {
      completed,
      inProgress,
      notStarted: total - completed - inProgress,
      total,
      completionRate: total > 0 ? Math.round((completed / total) * 100) : 0
    };
  };

  const getTotalTimeSpent = () => {
    const sessionTime = sessions.reduce((total, session) => total + (session.session_duration || 0), 0);
    const tutorialTime = progress.reduce((total, prog) => total + (prog.time_spent || 0), 0);
    return sessionTime + tutorialTime;
  };

  const getAchievements = () => {
    const achievements = [];
    const sessionCount = sessions.length;
    const completedTutorials = progress.filter(p => p.completion_status === 'completed').length;
    const streak = userProfile?.learning_streak || 0;
    const voiceSessions = sessions.filter(s => s.voice_used).length;
    
    if (sessionCount >= 1) achievements.push({ title: 'First Steps', desc: 'Completed your first debugging session', icon: '🚀' });
    if (sessionCount >= 10) achievements.push({ title: 'Debugger', desc: 'Completed 10 debugging sessions', icon: '🔍' });
    if (sessionCount >= 25) achievements.push({ title: 'Bug Hunter', desc: 'Completed 25 debugging sessions', icon: '🎯' });
    if (completedTutorials >= 1) achievements.push({ title: 'Scholar', desc: 'Completed your first tutorial', icon: '📚' });
    if (completedTutorials >= 5) achievements.push({ title: 'Knowledge Seeker', desc: 'Completed 5 tutorials', icon: '🧠' });
    if (streak >= 3) achievements.push({ title: 'Consistent Learner', desc: '3-day learning streak', icon: '🔥' });
    if (streak >= 7) achievements.push({ title: 'Week Warrior', desc: '7-day learning streak', icon: '⚡' });
    if (voiceSessions >= 5) achievements.push({ title: 'Voice Master', desc: 'Used voice features 5 times', icon: '🎤' });
    
    return achievements;
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

  const weeklyActivity = getWeeklyActivity();
  const languageStats = getLanguageStats();
  const completionStats = getCompletionStats();
  const totalTimeSpent = getTotalTimeSpent();
  const achievements = getAchievements();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 p-6 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
            Learning Progress
          </h1>
          <p className="text-lg text-gray-600">
            Track your coding journey and celebrate your achievements
          </p>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-blue-100 text-sm font-medium">Total Sessions</p>
                  <p className="text-3xl font-bold">{sessions.length}</p>
                  <p className="text-blue-100 text-sm">Debugging sessions</p>
                </div>
                <Code className="w-10 h-10 text-blue-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-green-500 to-emerald-600 text-white border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-green-100 text-sm font-medium">Tutorials Completed</p>
                  <p className="text-3xl font-bold">{completionStats.completed}</p>
                  <p className="text-green-100 text-sm">Out of {completionStats.total}</p>
                </div>
                <BookOpen className="w-10 h-10 text-green-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-purple-500 to-pink-600 text-white border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-purple-100 text-sm font-medium">Learning Streak</p>
                  <p className="text-3xl font-bold">{userProfile?.learning_streak || 0}</p>
                  <p className="text-purple-100 text-sm">Days in a row</p>
                </div>
                <TrendingUp className="w-10 h-10 text-purple-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-orange-500 to-red-600 text-white border-0">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-orange-100 text-sm font-medium">Time Spent</p>
                  <p className="text-3xl font-bold">{Math.round(totalTimeSpent)}</p>
                  <p className="text-orange-100 text-sm">Minutes learning</p>
                </div>
                <Clock className="w-10 h-10 text-orange-200" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Weekly Activity & Tutorial Progress */}
        <div className="grid lg:grid-cols-2 gap-6 mb-8">
          <Card className="shadow-lg border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="w-5 h-5 text-blue-500" />
                Weekly Activity
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-7 gap-2">
                {weeklyActivity.map((day, index) => (
                  <div key={index} className="text-center">
                    <div className="text-sm text-gray-500 mb-2">{day.day}</div>
                    <div 
                      className={`w-full h-12 rounded-lg flex items-center justify-center text-sm font-medium ${
                        day.sessions > 0 
                          ? 'bg-blue-500 text-white' 
                          : 'bg-gray-100 text-gray-400'
                      }`}
                    >
                      {day.sessions || 0}
                    </div>
                  </div>
                ))}
              </div>
              <p className="text-sm text-gray-500 mt-4 text-center">
                Daily debugging sessions this week
              </p>
            </CardContent>
          </Card>

          <Card className="shadow-lg border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="w-5 h-5 text-purple-500" />
                Tutorial Progress
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Completion Rate</span>
                <span className="font-semibold text-purple-600">{completionStats.completionRate}%</span>
              </div>
              <Progress value={completionStats.completionRate} className="h-3" />
              
              <div className="grid grid-cols-3 gap-4 mt-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">{completionStats.completed}</div>
                  <div className="text-sm text-gray-500">Completed</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">{completionStats.inProgress}</div>
                  <div className="text-sm text-gray-500">In Progress</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-400">{completionStats.notStarted}</div>
                  <div className="text-sm text-gray-500">Not Started</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Language Usage & Achievements */}
        <div className="grid lg:grid-cols-2 gap-6">
          <Card className="shadow-lg border-0">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Brain className="w-5 h-5 text-green-500" />
                Programming Languages
              </CardTitle>
            </CardHeader>
            <CardContent>
              {languageStats.length > 0 ? (
                <div className="space-y-4">
                  {languageStats.map((stat) => (
                    <div key={stat.language} className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <Badge className="bg-blue-100 text-blue-800">
                          {stat.language.toUpperCase()}
                        </Badge>
                      </div>
                      <div className="flex items-center gap-3">
                        <div className="w-24 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                            style={{ width: `${(stat.count / sessions.length) * 100}%` }}
                          />
                        </div>
                        <span className="text-sm font-medium text-gray-600 w-8">
                          {stat.count}
                        </span>
                      </div>
                    </div>
 