import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { ViewMode } from "@/types";
import { 
  Ungroup, 
  Calculator, 
  CheckCircle, 
  Box,
  Ruler,
  Settings,
  HelpCircle,
  Save
} from "lucide-react";

interface TopToolbarProps {
  currentView: ViewMode;
  onViewChange: (view: ViewMode) => void;
}

export function TopToolbar({ currentView, onViewChange }: TopToolbarProps) {
  const navItems = [
    { id: 'model' as ViewMode, label: 'Model', icon: Box },
    { id: 'analysis' as ViewMode, label: 'Analysis', icon: Calculator },
    { id: 'design' as ViewMode, label: 'Design', icon: CheckCircle },
    { id: 'bim' as ViewMode, label: '3D View', icon: Ungroup },
  ];

  return (
    <header className="bg-surface border-b border-border h-14 flex items-center justify-between px-4 shadow-sm">
      <div className="flex items-center space-x-6">
        <div className="flex items-center space-x-3">
          <Ungroup className="text-primary text-xl" />
          <h1 className="text-xl font-bold text-foreground">StruMind</h1>
        </div>
        
        <nav className="flex items-center space-x-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <Button
                key={item.id}
                variant={currentView === item.id ? "default" : "ghost"}
                size="sm"
                onClick={() => onViewChange(item.id)}
                className="px-3 py-1.5 text-sm font-medium"
              >
                <Icon className="mr-2 h-4 w-4" />
                {item.label}
              </Button>
            );
          })}
        </nav>
      </div>

      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2">
          <Button variant="ghost" size="sm" title="Units: SI">
            <Ruler className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm" title="Settings">
            <Settings className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm" title="Help">
            <HelpCircle className="h-4 w-4" />
          </Button>
        </div>
        
        <Separator orientation="vertical" className="h-6" />
        
        <div className="flex items-center space-x-3">
          <span className="text-sm text-muted-foreground">Project: Bridge Analysis</span>
          <Button size="sm" className="px-3 py-1.5">
            <Save className="mr-2 h-4 w-4" />
            Save
          </Button>
        </div>
      </div>
    </header>
  );
}
