import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { 
  MousePointer2,
  Circle,
  Minus,
  Square,
  Triangle,
  Anchor,
  Weight,
  Move3D,
  Copy,
  RotateCcw,
  Scissors,
  Ruler,
  Grid3X3,
  Zap,
  Settings2,
  ChevronDown,
  Target
} from "lucide-react";

export function ModelTools() {
  const [activeTool, setActiveTool] = useState('select');
  const [snapMode, setSnapMode] = useState('grid');

  const drawingTools = [
    { id: 'select', icon: MousePointer2, label: 'Select', shortcut: 'S', group: 'selection' },
    { id: 'node', icon: Circle, label: 'Node', shortcut: 'N', group: 'geometry' },
    { id: 'beam', icon: Minus, label: 'Beam', shortcut: 'B', group: 'geometry' },
    { id: 'column', icon: Square, label: 'Column', shortcut: 'C', group: 'geometry' },
    { id: 'brace', icon: Triangle, label: 'Brace', shortcut: 'X', group: 'geometry' },
    { id: 'plate', icon: Square, label: 'Plate', shortcut: 'P', group: 'geometry' },
  ];

  const constraintTools = [
    { id: 'fixed', icon: Anchor, label: 'Fixed', shortcut: 'F', type: 'support' },
    { id: 'pinned', icon: Circle, label: 'Pinned', shortcut: 'H', type: 'support' },
    { id: 'roller', icon: Target, label: 'Roller', shortcut: 'R', type: 'support' },
    { id: 'point_load', icon: Weight, label: 'Point Load', shortcut: 'L', type: 'load' },
    { id: 'distributed', icon: Zap, label: 'Distributed', shortcut: 'D', type: 'load' },
    { id: 'moment', icon: RotateCcw, label: 'Moment', shortcut: 'M', type: 'load' },
  ];

  const modifyTools = [
    { id: 'move', icon: Move3D, label: 'Move', shortcut: 'M' },
    { id: 'copy', icon: Copy, label: 'Copy', shortcut: 'Ctrl+C' },
    { id: 'rotate', icon: RotateCcw, label: 'Rotate', shortcut: 'R' },
    { id: 'trim', icon: Scissors, label: 'Trim', shortcut: 'T' },
    { id: 'measure', icon: Ruler, label: 'Measure', shortcut: 'Ctrl+M' },
  ];

  const snapOptions = [
    { id: 'grid', label: 'Grid', icon: Grid3X3 },
    { id: 'node', label: 'Node', icon: Circle },
    { id: 'midpoint', label: 'Midpoint', icon: Target },
    { id: 'intersection', label: 'Intersection', icon: Zap },
  ];

  return (
    <div className="professional-panel">
      <div className="bg-panel-header border-b border-border p-3">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-semibold text-foreground">Drawing Tools</h3>
          <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
            <Settings2 className="h-3 w-3" />
          </Button>
        </div>

        {/* Snap Settings */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs text-muted-foreground">Snap Mode</span>
            <Select value={snapMode} onValueChange={setSnapMode}>
              <SelectTrigger className="h-6 w-20 text-xs">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {snapOptions.map((option) => (
                  <SelectItem key={option.id} value={option.id}>
                    <div className="flex items-center">
                      <option.icon className="h-3 w-3 mr-1" />
                      {option.label}
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          
          <div className="flex items-center space-x-1">
            {snapOptions.map((option) => {
              const Icon = option.icon;
              return (
                <Button
                  key={option.id}
                  variant={snapMode === option.id ? "default" : "ghost"}
                  size="sm"
                  className="h-6 w-6 p-0"
                  onClick={() => setSnapMode(option.id)}
                  title={option.label}
                >
                  <Icon className="h-3 w-3" />
                </Button>
              );
            })}
          </div>
        </div>
      </div>

      <Tabs defaultValue="draw" className="flex-1">
        <TabsList className="grid w-full grid-cols-3 h-8 bg-panel-header rounded-none border-b border-border">
          <TabsTrigger value="draw" className="text-xs">Draw</TabsTrigger>
          <TabsTrigger value="loads" className="text-xs">Loads</TabsTrigger>
          <TabsTrigger value="modify" className="text-xs">Modify</TabsTrigger>
        </TabsList>

        <TabsContent value="draw" className="m-0 p-3">
          <div className="space-y-3">
            <div>
              <div className="text-xs font-medium text-muted-foreground mb-2">Selection</div>
              <div className="grid grid-cols-2 gap-2">
                {drawingTools.filter(tool => tool.group === 'selection').map((tool) => {
                  const Icon = tool.icon;
                  return (
                    <Button
                      key={tool.id}
                      variant={activeTool === tool.id ? "default" : "outline"}
                      size="sm"
                      className="h-10 flex flex-col items-center justify-center p-2"
                      onClick={() => setActiveTool(tool.id)}
                    >
                      <Icon className="h-4 w-4 mb-1" />
                      <span className="text-xs">{tool.label}</span>
                    </Button>
                  );
                })}
              </div>
            </div>

            <Separator />

            <div>
              <div className="text-xs font-medium text-muted-foreground mb-2">Structural Elements</div>
              <div className="grid grid-cols-2 gap-2">
                {drawingTools.filter(tool => tool.group === 'geometry').map((tool) => {
                  const Icon = tool.icon;
                  return (
                    <Button
                      key={tool.id}
                      variant={activeTool === tool.id ? "default" : "outline"}
                      size="sm"
                      className="h-10 flex flex-col items-center justify-center p-2"
                      onClick={() => setActiveTool(tool.id)}
                    >
                      <Icon className="h-4 w-4 mb-1" />
                      <span className="text-xs">{tool.label}</span>
                      <Badge variant="outline" className="text-xs mt-1 h-4 px-1">
                        {tool.shortcut}
                      </Badge>
                    </Button>
                  );
                })}
              </div>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="loads" className="m-0 p-3">
          <div className="space-y-3">
            <div>
              <div className="text-xs font-medium text-muted-foreground mb-2">Boundary Conditions</div>
              <div className="grid grid-cols-2 gap-2">
                {constraintTools.filter(tool => tool.type === 'support').map((tool) => {
                  const Icon = tool.icon;
                  return (
                    <Button
                      key={tool.id}
                      variant={activeTool === tool.id ? "default" : "outline"}
                      size="sm"
                      className="h-10 flex flex-col items-center justify-center p-2"
                      onClick={() => setActiveTool(tool.id)}
                    >
                      <Icon className="h-4 w-4 mb-1" />
                      <span className="text-xs">{tool.label}</span>
                    </Button>
                  );
                })}
              </div>
            </div>

            <Separator />

            <div>
              <div className="text-xs font-medium text-muted-foreground mb-2">Applied Loads</div>
              <div className="grid grid-cols-2 gap-2">
                {constraintTools.filter(tool => tool.type === 'load').map((tool) => {
                  const Icon = tool.icon;
                  return (
                    <Button
                      key={tool.id}
                      variant={activeTool === tool.id ? "default" : "outline"}
                      size="sm"
                      className="h-10 flex flex-col items-center justify-center p-2"
                      onClick={() => setActiveTool(tool.id)}
                    >
                      <Icon className="h-4 w-4 mb-1" />
                      <span className="text-xs">{tool.label}</span>
                    </Button>
                  );
                })}
              </div>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="modify" className="m-0 p-3">
          <div className="grid grid-cols-2 gap-2">
            {modifyTools.map((tool) => {
              const Icon = tool.icon;
              return (
                <Button
                  key={tool.id}
                  variant={activeTool === tool.id ? "default" : "outline"}
                  size="sm"
                  className="h-10 flex flex-col items-center justify-center p-2"
                  onClick={() => setActiveTool(tool.id)}
                >
                  <Icon className="h-4 w-4 mb-1" />
                  <span className="text-xs">{tool.label}</span>
                  <Badge variant="outline" className="text-xs mt-1 h-4 px-1">
                    {tool.shortcut}
                  </Badge>
                </Button>
              );
            })}
          </div>
        </TabsContent>
      </Tabs>

      {/* Active Tool Info */}
      {activeTool !== 'select' && (
        <div className="border-t border-border p-3 bg-panel-header">
          <div className="text-xs">
            <div className="font-medium text-foreground mb-1">
              Active: {drawingTools.concat(constraintTools, modifyTools).find(t => t.id === activeTool)?.label}
            </div>
            <div className="text-muted-foreground">
              Click to place or ESC to cancel
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
