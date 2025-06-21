import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ViewportControls, SelectedElement, ProjectStats } from "@/types";
import { 
  FolderOpen, 
  Box, 
  Weight, 
  TrendingUp,
  Maximize
} from "lucide-react";

interface SidebarProps {
  viewportControls: ViewportControls;
  onViewportControlsChange: (controls: ViewportControls) => void;
  selectedElement: SelectedElement;
  onSelectedElementChange: (element: SelectedElement) => void;
  projectStats: ProjectStats;
}

export function Sidebar({ 
  viewportControls, 
  onViewportControlsChange, 
  selectedElement, 
  onSelectedElementChange,
  projectStats 
}: SidebarProps) {
  const updateViewportControl = (key: keyof ViewportControls, value: boolean) => {
    onViewportControlsChange({ ...viewportControls, [key]: value });
  };

  const updateSelectedElement = (key: keyof SelectedElement, value: string | number) => {
    onSelectedElementChange({ ...selectedElement, [key]: value });
  };

  return (
    <aside className="w-64 bg-surface border-r border-border flex flex-col">
      {/* Project Explorer */}
      <div className="p-4 border-b border-border">
        <h3 className="text-sm font-semibold text-foreground mb-3">Project Explorer</h3>
        <div className="space-y-1">
          <div className="flex items-center text-sm text-foreground">
            <FolderOpen className="mr-2 h-4 w-4 text-yellow-600" />
            <span>Current Project</span>
          </div>
          <div className="ml-6 space-y-1">
            <div className="flex items-center text-sm text-muted-foreground hover:text-foreground cursor-pointer">
              <Box className="mr-2 h-4 w-4" />
              <span>Model ({projectStats.nodeCount} nodes)</span>
            </div>
            <div className="flex items-center text-sm text-muted-foreground hover:text-foreground cursor-pointer">
              <Weight className="mr-2 h-4 w-4" />
              <span>Load Cases (4)</span>
            </div>
            <div className="flex items-center text-sm text-muted-foreground hover:text-foreground cursor-pointer">
              <TrendingUp className="mr-2 h-4 w-4" />
              <span>Results</span>
            </div>
          </div>
        </div>
      </div>

      {/* Model View Controls */}
      <div className="p-4 border-b border-border">
        <h3 className="text-sm font-semibold text-foreground mb-3">Model View</h3>
        <div className="space-y-3">
          <div className="space-y-2">
            <div className="flex items-center space-x-2">
              <Checkbox 
                id="showNodes"
                checked={viewportControls.showNodes}
                onCheckedChange={(checked) => updateViewportControl('showNodes', !!checked)}
              />
              <Label htmlFor="showNodes" className="text-sm text-foreground">Nodes</Label>
            </div>
            <div className="flex items-center space-x-2">
              <Checkbox 
                id="showElements"
                checked={viewportControls.showElements}
                onCheckedChange={(checked) => updateViewportControl('showElements', !!checked)}
              />
              <Label htmlFor="showElements" className="text-sm text-foreground">Elements</Label>
            </div>
            <div className="flex items-center space-x-2">
              <Checkbox 
                id="showLoads"
                checked={viewportControls.showLoads}
                onCheckedChange={(checked) => updateViewportControl('showLoads', !!checked)}
              />
              <Label htmlFor="showLoads" className="text-sm text-foreground">Loads</Label>
            </div>
            <div className="flex items-center space-x-2">
              <Checkbox 
                id="showSupports"
                checked={viewportControls.showSupports}
                onCheckedChange={(checked) => updateViewportControl('showSupports', !!checked)}
              />
              <Label htmlFor="showSupports" className="text-sm text-foreground">Supports</Label>
            </div>
          </div>
          
          <div className="pt-2">
            <Button variant="outline" className="w-full" size="sm">
              <Maximize className="mr-2 h-4 w-4" />
              Fit to View
            </Button>
          </div>
        </div>
      </div>

      {/* Properties Panel */}
      <div className="flex-1 p-4">
        <h3 className="text-sm font-semibold text-foreground mb-3">Properties</h3>
        <div className="space-y-3">
          <div>
            <Label className="text-xs font-medium text-muted-foreground">Element ID</Label>
            <Input 
              value={selectedElement.id} 
              readOnly 
              className="mt-1 text-sm"
            />
          </div>
          <div>
            <Label className="text-xs font-medium text-muted-foreground">Section</Label>
            <Select 
              value={selectedElement.sectionType}
              onValueChange={(value) => updateSelectedElement('sectionType', value)}
            >
              <SelectTrigger className="mt-1">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="W18x50">W18x50</SelectItem>
                <SelectItem value="W21x62">W21x62</SelectItem>
                <SelectItem value="W24x76">W24x76</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label className="text-xs font-medium text-muted-foreground">Material</Label>
            <Select 
              value={selectedElement.materialType}
              onValueChange={(value) => updateSelectedElement('materialType', value)}
            >
              <SelectTrigger className="mt-1">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="A992 Steel">A992 Steel</SelectItem>
                <SelectItem value="A36 Steel">A36 Steel</SelectItem>
                <SelectItem value="Concrete fc=4000">Concrete fc=4000</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label className="text-xs font-medium text-muted-foreground">Length (m)</Label>
            <Input 
              type="number" 
              value={selectedElement.length}
              onChange={(e) => updateSelectedElement('length', parseFloat(e.target.value))}
              className="mt-1 text-sm"
            />
          </div>
        </div>
      </div>
    </aside>
  );
}
