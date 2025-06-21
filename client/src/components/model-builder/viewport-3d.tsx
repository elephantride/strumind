import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { 
  Home, 
  ZoomIn, 
  ZoomOut, 
  RotateCcw,
  Move3D,
  RotateCw,
  Maximize,
  Grid3X3,
  Lightbulb,
  Camera,
  Layers,
  Target,
  Crosshair,
  Eye,
  MousePointer2,
  Hand,
  Compass
} from "lucide-react";

interface Viewport3DProps {
  stats: {
    nodeCount: number;
    elementCount: number;
    selectedElement?: string;
  };
}

export function Viewport3D({ stats }: Viewport3DProps) {
  const [activeView, setActiveView] = useState('perspective');
  const [showGrid, setShowGrid] = useState(true);

  const viewModes = [
    { id: 'perspective', label: 'Perspective', shortcut: 'P' },
    { id: 'front', label: 'Front', shortcut: 'F' },
    { id: 'top', label: 'Top', shortcut: 'T' },
    { id: 'right', label: 'Right', shortcut: 'R' },
    { id: 'iso', label: 'Isometric', shortcut: 'I' }
  ];

  return (
    <div className="flex-1 viewport-3d relative grid-overlay">
      {/* 3D Canvas Area with engineering grid */}
      <div className="absolute inset-0">
        {/* Background with subtle engineering grid */}
        <div className="absolute inset-0 opacity-20">
          <svg width="100%" height="100%" className="absolute inset-0">
            <defs>
              <pattern id="engineeringGrid" width="40" height="40" patternUnits="userSpaceOnUse">
                <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.15)" strokeWidth="0.5"/>
                <path d="M 0 0 L 40 40" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="0.3"/>
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#engineeringGrid)" />
          </svg>
        </div>

        {/* Main 3D content placeholder */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="text-center text-white/80">
            <div className="mb-8">
              <div className="w-32 h-32 mx-auto border-2 border-dashed border-white/30 rounded-lg flex items-center justify-center mb-4">
                <div className="text-4xl">⚡</div>
              </div>
              <div className="text-lg font-medium mb-2">3D Structural Model</div>
              <div className="text-sm opacity-75 mb-4">WebGL viewport ready for integration</div>
              <div className="flex justify-center space-x-3">
                <Badge variant="outline" className="text-xs bg-blue-500/20 text-blue-300 border-blue-400/30">
                  Three.js Ready
                </Badge>
                <Badge variant="outline" className="text-xs bg-green-500/20 text-green-300 border-green-400/30">
                  Hardware Accelerated
                </Badge>
              </div>
            </div>
          </div>
        </div>

        {/* Coordinate System Indicator */}
        <div className="absolute bottom-20 left-4">
          <div className="w-16 h-16 relative">
            <svg width="64" height="64" viewBox="0 0 64 64">
              <g transform="translate(32,32)">
                <line x1="0" y1="0" x2="24" y2="0" stroke="#ef4444" strokeWidth="2" markerEnd="url(#arrowX)" />
                <line x1="0" y1="0" x2="0" y2="-24" stroke="#10b981" strokeWidth="2" markerEnd="url(#arrowY)" />
                <line x1="0" y1="0" x2="-12" y2="12" stroke="#3b82f6" strokeWidth="2" markerEnd="url(#arrowZ)" />
                <text x="26" y="4" className="text-xs fill-red-400 font-medium">X</text>
                <text x="2" y="-26" className="text-xs fill-green-400 font-medium">Y</text>
                <text x="-20" y="20" className="text-xs fill-blue-400 font-medium">Z</text>
              </g>
              <defs>
                <marker id="arrowX" markerWidth="8" markerHeight="8" refX="8" refY="3" orient="auto">
                  <polygon points="0 0, 8 3, 0 6" fill="#ef4444" />
                </marker>
                <marker id="arrowY" markerWidth="8" markerHeight="8" refX="8" refY="3" orient="auto">
                  <polygon points="0 0, 8 3, 0 6" fill="#10b981" />
                </marker>
                <marker id="arrowZ" markerWidth="8" markerHeight="8" refX="8" refY="3" orient="auto">
                  <polygon points="0 0, 8 3, 0 6" fill="#3b82f6" />
                </marker>
              </defs>
            </svg>
          </div>
        </div>
      </div>

      {/* View Mode Selector */}
      <div className="absolute top-4 left-4 flex flex-col space-y-2">
        <div className="bg-panel/90 backdrop-blur-sm rounded-lg border border-border p-2">
          <div className="text-xs text-muted-foreground mb-1 font-medium">View</div>
          <div className="grid grid-cols-2 gap-1">
            {viewModes.slice(0, 4).map((view) => (
              <Button
                key={view.id}
                variant={activeView === view.id ? "default" : "ghost"}
                size="sm"
                className="h-6 px-2 text-xs"
                onClick={() => setActiveView(view.id)}
              >
                {view.shortcut}
              </Button>
            ))}
          </div>
        </div>

        <div className="bg-panel/90 backdrop-blur-sm rounded-lg border border-border p-2">
          <div className="text-xs text-muted-foreground mb-1 font-medium">Display</div>
          <div className="space-y-1">
            <Button
              variant={showGrid ? "default" : "ghost"}
              size="sm"
              className="w-full h-6 px-2 text-xs justify-start"
              onClick={() => setShowGrid(!showGrid)}
            >
              <Grid3X3 className="h-3 w-3 mr-1" />
              Grid
            </Button>
            <Button variant="ghost" size="sm" className="w-full h-6 px-2 text-xs justify-start">
              <Lightbulb className="h-3 w-3 mr-1" />
              Lights
            </Button>
          </div>
        </div>
      </div>

      {/* Navigation Controls */}
      <div className="absolute top-4 right-4 flex flex-col space-y-2">
        <div className="bg-panel/90 backdrop-blur-sm rounded-lg border border-border p-2">
          <div className="text-xs text-muted-foreground mb-1 font-medium">Navigate</div>
          <div className="grid grid-cols-2 gap-1">
            <Button variant="ghost" size="sm" className="h-8 w-8 p-0" title="Home View">
              <Home className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm" className="h-8 w-8 p-0" title="Fit All">
              <Maximize className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm" className="h-8 w-8 p-0" title="Zoom In">
              <ZoomIn className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm" className="h-8 w-8 p-0" title="Zoom Out">
              <ZoomOut className="h-4 w-4" />
            </Button>
          </div>
        </div>

        <div className="bg-panel/90 backdrop-blur-sm rounded-lg border border-border p-2">
          <div className="text-xs text-muted-foreground mb-1 font-medium">Tools</div>
          <div className="grid grid-cols-2 gap-1">
            <Button variant="ghost" size="sm" className="h-8 w-8 p-0" title="Select">
              <MousePointer2 className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm" className="h-8 w-8 p-0" title="Pan">
              <Hand className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm" className="h-8 w-8 p-0" title="Rotate">
              <RotateCcw className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm" className="h-8 w-8 p-0" title="Measure">
              <Crosshair className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>

      {/* View Cube - Enhanced */}
      <div className="absolute top-1/2 right-4 transform -translate-y-1/2">
        <div className="w-20 h-20 perspective-1000">
          <div className="relative w-full h-full transform-style-preserve-3d">
            <div className="absolute inset-0 bg-panel/90 backdrop-blur-sm border border-border rounded-lg flex items-center justify-center cursor-pointer hover:bg-muted transition-colors">
              <div className="text-center">
                <Compass className="h-6 w-6 mx-auto mb-1 text-primary" />
                <div className="text-xs font-medium">ISO</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Measurement Overlay */}
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 pointer-events-none">
        <div className="text-xs text-white/60 font-mono">
          <div className="bg-black/50 px-2 py-1 rounded mb-2">6.100 m</div>
          <div className="bg-black/50 px-2 py-1 rounded">∠ 45.0°</div>
        </div>
      </div>

      {/* Enhanced Status Bar */}
      <div className="absolute bottom-0 left-0 right-0 status-bar h-7 px-4 flex items-center justify-between">
        <div className="flex items-center space-x-4 text-xs">
          <span>Nodes: {stats.nodeCount}</span>
          <span>Elements: {stats.elementCount}</span>
          <span>Selected: {stats.selectedElement || 'None'}</span>
          <span className="text-accent">✓ Model Valid</span>
        </div>
        <div className="flex items-center space-x-4 text-xs">
          <span>View: {activeView}</span>
          <span>Scale: 1:100</span>
          <span>Units: kN, m</span>
          <span>FPS: 60</span>
        </div>
      </div>

      {/* Selection Info Overlay */}
      {stats.selectedElement && (
        <div className="absolute top-16 left-4 bg-panel/95 backdrop-blur-sm border border-border rounded-lg p-3 max-w-xs">
          <div className="text-xs">
            <div className="font-medium text-foreground mb-2">Element B127</div>
            <div className="space-y-1 text-muted-foreground">
              <div className="flex justify-between">
                <span>Type:</span>
                <span>W18x50 Beam</span>
              </div>
              <div className="flex justify-between">
                <span>Length:</span>
                <span>6.100 m</span>
              </div>
              <div className="flex justify-between">
                <span>Material:</span>
                <span>A992 Steel</span>
              </div>
              <div className="flex justify-between">
                <span>Status:</span>
                <span className="text-accent">✓ OK</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
