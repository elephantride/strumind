import { Button } from "@/components/ui/button";
import { 
  Home, 
  ZoomIn, 
  ZoomOut, 
  RotateCcw 
} from "lucide-react";

interface Viewport3DProps {
  stats: {
    nodeCount: number;
    elementCount: number;
    selectedElement?: string;
  };
}

export function Viewport3D({ stats }: Viewport3DProps) {
  return (
    <div className="flex-1 viewport-3d relative">
      {/* 3D Canvas Area */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="text-center text-white">
          <div className="text-6xl mb-4 opacity-50">🏗️</div>
          <p className="text-lg mb-2">3D Model Viewport</p>
          <p className="text-sm opacity-75">WebGL/Three.js integration ready</p>
        </div>
      </div>

      {/* Viewport Controls */}
      <div className="absolute top-4 right-4 space-y-2">
        <Button size="sm" variant="outline" className="w-10 h-10 p-0 bg-gray-800 hover:bg-gray-700 text-white border-gray-600">
          <Home className="h-4 w-4" />
        </Button>
        <Button size="sm" variant="outline" className="w-10 h-10 p-0 bg-gray-800 hover:bg-gray-700 text-white border-gray-600">
          <ZoomIn className="h-4 w-4" />
        </Button>
        <Button size="sm" variant="outline" className="w-10 h-10 p-0 bg-gray-800 hover:bg-gray-700 text-white border-gray-600">
          <ZoomOut className="h-4 w-4" />
        </Button>
        <Button size="sm" variant="outline" className="w-10 h-10 p-0 bg-gray-800 hover:bg-gray-700 text-white border-gray-600">
          <RotateCcw className="h-4 w-4" />
        </Button>
      </div>

      {/* View Cube */}
      <div className="absolute top-4 left-4 w-16 h-16 bg-gray-800 rounded-lg flex items-center justify-center">
        <div className="text-white text-xs font-medium">3D</div>
      </div>

      {/* Status Bar */}
      <div className="absolute bottom-0 left-0 right-0 bg-gray-800 bg-opacity-90 text-white text-xs px-4 py-2 flex justify-between">
        <span>Nodes: {stats.nodeCount} | Elements: {stats.elementCount} | Selected: {stats.selectedElement || 'None'}</span>
        <span>Units: SI (m, kN, MPa)</span>
      </div>
    </div>
  );
}
