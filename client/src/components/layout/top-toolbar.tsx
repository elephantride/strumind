import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { ViewMode } from "@/types";
import { 
  Menu,
  FolderOpen,
  Save,
  Undo2,
  Redo2,
  Copy,
  Clipboard,
  Search,
  Box,
  Calculator,
  CheckCircle,
  Ungroup,
  Grid3X3,
  ZoomIn,
  ZoomOut,
  RotateCcw,
  Settings,
  HelpCircle,
  User,
  ChevronDown,
  Play,
  Square
} from "lucide-react";

interface TopToolbarProps {
  currentView: ViewMode;
  onViewChange: (view: ViewMode) => void;
}

export function TopToolbar({ currentView, onViewChange }: TopToolbarProps) {
  const viewTabs = [
    { id: 'model' as ViewMode, label: 'Modeling', icon: Box, color: 'bg-blue-600' },
    { id: 'analysis' as ViewMode, label: 'Analysis', icon: Calculator, color: 'bg-green-600' },
    { id: 'design' as ViewMode, label: 'Design', icon: CheckCircle, color: 'bg-orange-600' },
    { id: 'bim' as ViewMode, label: 'Visualization', icon: Ungroup, color: 'bg-purple-600' },
  ];

  return (
    <div className="professional-toolbar">
      {/* Menu Bar */}
      <div className="h-8 bg-panel-header border-b border-border flex items-center px-2 text-xs">
        <div className="flex items-center space-x-4">
          <Button variant="ghost" size="sm" className="h-6 px-2 text-xs hover:bg-muted">
            File
          </Button>
          <Button variant="ghost" size="sm" className="h-6 px-2 text-xs hover:bg-muted">
            Edit
          </Button>
          <Button variant="ghost" size="sm" className="h-6 px-2 text-xs hover:bg-muted">
            View
          </Button>
          <Button variant="ghost" size="sm" className="h-6 px-2 text-xs hover:bg-muted">
            Model
          </Button>
          <Button variant="ghost" size="sm" className="h-6 px-2 text-xs hover:bg-muted">
            Analysis
          </Button>
          <Button variant="ghost" size="sm" className="h-6 px-2 text-xs hover:bg-muted">
            Design
          </Button>
          <Button variant="ghost" size="sm" className="h-6 px-2 text-xs hover:bg-muted">
            Tools
          </Button>
          <Button variant="ghost" size="sm" className="h-6 px-2 text-xs hover:bg-muted">
            Help
          </Button>
        </div>
        <div className="ml-auto flex items-center space-x-2">
          <span className="text-muted-foreground">StruMind Professional 2024</span>
          <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
            <User className="h-3 w-3" />
          </Button>
        </div>
      </div>

      {/* Main Toolbar */}
      <div className="h-12 flex items-center px-3 space-x-1">
        {/* Logo and Brand */}
        <div className="flex items-center space-x-3 mr-6">
          <div className="w-8 h-8 bg-primary rounded flex items-center justify-center">
            <Ungroup className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="text-sm font-bold text-foreground">StruMind</div>
            <div className="text-xs text-muted-foreground">Professional</div>
          </div>
        </div>

        {/* File Operations */}
        <div className="flex items-center space-x-1">
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0" title="New Project">
            <FolderOpen className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0" title="Save">
            <Save className="h-4 w-4" />
          </Button>
        </div>

        <Separator orientation="vertical" className="h-6 mx-2" />

        {/* Edit Operations */}
        <div className="flex items-center space-x-1">
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0" title="Undo">
            <Undo2 className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0" title="Redo">
            <Redo2 className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0" title="Copy">
            <Copy className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0" title="Paste">
            <Clipboard className="h-4 w-4" />
          </Button>
        </div>

        <Separator orientation="vertical" className="h-6 mx-2" />

        {/* View Controls */}
        <div className="flex items-center space-x-1">
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0" title="Grid">
            <Grid3X3 className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0" title="Zoom In">
            <ZoomIn className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0" title="Zoom Out">
            <ZoomOut className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0" title="Reset View">
            <RotateCcw className="h-4 w-4" />
          </Button>
        </div>

        <Separator orientation="vertical" className="h-6 mx-2" />

        {/* Analysis Controls */}
        <div className="flex items-center space-x-2">
          <Button size="sm" className="h-8 bg-accent hover:bg-accent/90">
            <Play className="mr-1 h-3 w-3" />
            Run
          </Button>
          <Button variant="outline" size="sm" className="h-8">
            <Square className="mr-1 h-3 w-3" />
            Stop
          </Button>
        </div>

        {/* Spacer */}
        <div className="flex-1" />

        {/* Search */}
        <div className="relative">
          <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 h-3 w-3 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search..."
            className="h-8 w-48 pl-7 pr-3 text-xs bg-input border border-border rounded focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </div>

        {/* Status and Settings */}
        <div className="flex items-center space-x-3 ml-4">
          <Badge variant="outline" className="text-xs">
            Bridge-Model-v2.1
          </Badge>
          <div className="text-xs text-muted-foreground">
            Units: kN, m
          </div>
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
            <Settings className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Module Tabs */}
      <div className="h-10 bg-panel border-b border-border flex items-center px-3">
        <div className="flex items-center space-x-1">
          {viewTabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = currentView === tab.id;
            return (
              <Button
                key={tab.id}
                variant="ghost"
                size="sm"
                onClick={() => onViewChange(tab.id)}
                className={`h-8 px-3 text-xs font-medium rounded-t border-b-2 transition-all ${
                  isActive 
                    ? 'bg-muted border-primary text-foreground' 
                    : 'border-transparent hover:bg-muted/50 text-muted-foreground hover:text-foreground'
                }`}
              >
                <div className={`w-2 h-2 rounded mr-2 ${isActive ? tab.color : 'bg-muted-foreground'}`} />
                <Icon className="mr-1 h-3 w-3" />
                {tab.label}
              </Button>
            );
          })}
        </div>
        
        <div className="ml-auto flex items-center space-x-2 text-xs text-muted-foreground">
          <span>Model Status: ✓ Valid</span>
          <span>•</span>
          <span>Analysis: Ready</span>
          <span>•</span>
          <span>Elements: 142</span>
        </div>
      </div>
    </div>
  );
}
