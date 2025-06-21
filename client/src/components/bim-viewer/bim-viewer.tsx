import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { 
  Home, 
  ZoomIn, 
  ZoomOut, 
  RotateCcw, 
  Maximize 
} from "lucide-react";

export function BIMViewer() {
  const viewModes = ["Wireframe", "Shaded", "Rendered"];
  const displayOptions = [
    { id: "labels", label: "Element Labels", checked: true },
    { id: "nodes", label: "Node Numbers", checked: false },
    { id: "deformed", label: "Deformed Shape", checked: false },
  ];

  return (
    <div className="h-full viewport-3d relative">
      {/* 3D BIM Canvas */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="text-center text-white">
          <div className="text-8xl mb-6 opacity-50">🏗️</div>
          <h3 className="text-2xl font-bold mb-4">3D BIM Viewer</h3>
          <p className="text-lg mb-2">Advanced 3D visualization ready</p>
          <p className="text-sm opacity-75">WebGL/Three.js integration point</p>
          <div className="mt-8 space-x-4">
            <Button className="bg-primary hover:bg-primary/90">
              Load Model
            </Button>
            <Button variant="outline" className="bg-gray-700 text-white border-gray-600 hover:bg-gray-600">
              View Settings
            </Button>
          </div>
        </div>
      </div>

      {/* BIM Controls */}
      <div className="absolute top-4 left-4 space-y-4">
        <div className="bg-gray-800 bg-opacity-90 rounded-lg p-3">
          <h4 className="text-white text-sm font-medium mb-2">View Mode</h4>
          <div className="space-y-1">
            {viewModes.map((mode, index) => (
              <Button
                key={index}
                variant="ghost"
                size="sm"
                className="w-full justify-start text-xs text-white hover:bg-gray-700 h-auto py-1"
              >
                {mode}
              </Button>
            ))}
          </div>
        </div>

        <div className="bg-gray-800 bg-opacity-90 rounded-lg p-3">
          <h4 className="text-white text-sm font-medium mb-2">Display</h4>
          <div className="space-y-1">
            {displayOptions.map((option, index) => (
              <div key={index} className="flex items-center space-x-2">
                <Checkbox 
                  id={option.id}
                  checked={option.checked}
                  className="border-white data-[state=checked]:bg-white data-[state=checked]:text-black"
                />
                <Label 
                  htmlFor={option.id}
                  className="text-xs text-white cursor-pointer"
                >
                  {option.label}
                </Label>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Viewport Controls */}
      <div className="absolute top-4 right-4 space-y-2">
        <Button size="sm" variant="outline" className="w-12 h-12 p-0 bg-gray-800 hover:bg-gray-700 text-white border-gray-600">
          <Home className="h-4 w-4" />
        </Button>
        <Button size="sm" variant="outline" className="w-12 h-12 p-0 bg-gray-800 hover:bg-gray-700 text-white border-gray-600">
          <ZoomIn className="h-4 w-4" />
        </Button>
        <Button size="sm" variant="outline" className="w-12 h-12 p-0 bg-gray-800 hover:bg-gray-700 text-white border-gray-600">
          <ZoomOut className="h-4 w-4" />
        </Button>
        <Button size="sm" variant="outline" className="w-12 h-12 p-0 bg-gray-800 hover:bg-gray-700 text-white border-gray-600">
          <RotateCcw className="h-4 w-4" />
        </Button>
        <Button size="sm" variant="outline" className="w-12 h-12 p-0 bg-gray-800 hover:bg-gray-700 text-white border-gray-600">
          <Maximize className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
