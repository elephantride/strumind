import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { ViewportControls, SelectedElement, ProjectStats } from "@/types";
import { 
  FolderOpen,
  Folder,
  ChevronRight,
  ChevronDown,
  Box,
  Circle,
  Square,
  Triangle,
  Weight,
  Anchor,
  TrendingUp,
  FileText,
  Settings,
  Eye,
  EyeOff,
  Lock,
  Unlock,
  Layers,
  Grid3X3,
  Ruler,
  Calculator,
  Maximize,
  Filter,
  Search,
  MoreHorizontal
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
  const [expandedNodes, setExpandedNodes] = useState<Set<string>>(new Set(['model', 'materials', 'sections']));
  const [activeTab, setActiveTab] = useState('explorer');

  const updateViewportControl = (key: keyof ViewportControls, value: boolean) => {
    onViewportControlsChange({ ...viewportControls, [key]: value });
  };

  const updateSelectedElement = (key: keyof SelectedElement, value: string | number) => {
    onSelectedElementChange({ ...selectedElement, [key]: value });
  };

  const toggleNode = (nodeId: string) => {
    const newExpanded = new Set(expandedNodes);
    if (newExpanded.has(nodeId)) {
      newExpanded.delete(nodeId);
    } else {
      newExpanded.add(nodeId);
    }
    setExpandedNodes(newExpanded);
  };

  const projectTree = [
    {
      id: 'model',
      label: 'Structural Model',
      icon: Box,
      children: [
        { id: 'nodes', label: `Nodes (${projectStats.nodeCount})`, icon: Circle, count: projectStats.nodeCount },
        { id: 'elements', label: `Elements (${projectStats.elementCount})`, icon: Square, count: projectStats.elementCount },
        { id: 'supports', label: 'Boundary Conditions (8)', icon: Anchor, count: 8 },
        { id: 'loads', label: 'Load Cases (4)', icon: Weight, count: 4 }
      ]
    },
    {
      id: 'materials',
      label: 'Materials',
      icon: Layers,
      children: [
        { id: 'steel', label: 'A992 Steel', icon: Box },
        { id: 'concrete', label: 'Concrete fc=4000', icon: Box },
        { id: 'timber', label: 'Douglas Fir', icon: Box }
      ]
    },
    {
      id: 'sections',
      label: 'Section Properties',
      icon: Square,
      children: [
        { id: 'w-shapes', label: 'W-Shapes (12)', icon: Square, count: 12 },
        { id: 'hss', label: 'HSS Sections (5)', icon: Square, count: 5 },
        { id: 'custom', label: 'Custom Sections (2)', icon: Square, count: 2 }
      ]
    },
    {
      id: 'analysis',
      label: 'Analysis Results',
      icon: TrendingUp,
      children: [
        { id: 'displacements', label: 'Displacements', icon: TrendingUp },
        { id: 'forces', label: 'Element Forces', icon: TrendingUp },
        { id: 'stresses', label: 'Stresses', icon: TrendingUp },
        { id: 'reactions', label: 'Reactions', icon: TrendingUp }
      ]
    }
  ];

  const layers = [
    { id: 'structural', name: 'Structural Elements', visible: true, locked: false, color: '#3b82f6' },
    { id: 'loads', name: 'Load Cases', visible: viewportControls.showLoads, locked: false, color: '#ef4444' },
    { id: 'supports', name: 'Supports', visible: viewportControls.showSupports, locked: false, color: '#10b981' },
    { id: 'dimensions', name: 'Dimensions', visible: false, locked: false, color: '#8b5cf6' },
    { id: 'grid', name: 'Grid Lines', visible: true, locked: true, color: '#6b7280' }
  ];

  return (
    <div className="w-80 professional-panel flex flex-col">
      {/* Header */}
      <div className="h-10 bg-panel-header border-b border-border flex items-center px-3">
        <div className="flex items-center space-x-2">
          <Search className="h-3 w-3 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search model..."
            className="flex-1 text-xs bg-transparent border-none outline-none text-foreground placeholder-muted-foreground"
          />
        </div>
        <Button variant="ghost" size="sm" className="h-6 w-6 p-0 ml-2">
          <Filter className="h-3 w-3" />
        </Button>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
        <TabsList className="grid w-full grid-cols-3 h-8 bg-panel-header rounded-none border-b border-border">
          <TabsTrigger value="explorer" className="text-xs py-1">Explorer</TabsTrigger>
          <TabsTrigger value="layers" className="text-xs py-1">Layers</TabsTrigger>
          <TabsTrigger value="properties" className="text-xs py-1">Properties</TabsTrigger>
        </TabsList>

        <TabsContent value="explorer" className="flex-1 m-0 p-0">
          <ScrollArea className="flex-1">
            <div className="p-2">
              {projectTree.map((section) => {
                const SectionIcon = section.icon;
                const isExpanded = expandedNodes.has(section.id);
                
                return (
                  <div key={section.id} className="mb-1">
                    <Button
                      variant="ghost"
                      size="sm"
                      className="w-full justify-start h-7 px-2 text-xs font-medium hover:bg-muted"
                      onClick={() => toggleNode(section.id)}
                    >
                      {isExpanded ? (
                        <ChevronDown className="h-3 w-3 mr-1" />
                      ) : (
                        <ChevronRight className="h-3 w-3 mr-1" />
                      )}
                      <SectionIcon className="h-3 w-3 mr-2" />
                      {section.label}
                    </Button>
                    
                    {isExpanded && section.children && (
                      <div className="ml-4 mt-1">
                        {section.children.map((child) => {
                          const ChildIcon = child.icon;
                          return (
                            <Button
                              key={child.id}
                              variant="ghost"
                              size="sm"
                              className="w-full justify-start h-6 px-2 text-xs text-muted-foreground hover:text-foreground hover:bg-muted"
                            >
                              <ChildIcon className="h-3 w-3 mr-2" />
                              {child.label}
                              {child.count && (
                                <span className="ml-auto text-xs">{child.count}</span>
                              )}
                            </Button>
                          );
                        })}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </ScrollArea>
        </TabsContent>

        <TabsContent value="layers" className="flex-1 m-0 p-0">
          <div className="p-2">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-medium text-foreground">Layer Control</span>
              <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
                <MoreHorizontal className="h-3 w-3" />
              </Button>
            </div>
            
            <div className="space-y-1">
              {layers.map((layer) => (
                <div
                  key={layer.id}
                  className="flex items-center justify-between p-2 rounded hover:bg-muted group"
                >
                  <div className="flex items-center space-x-2">
                    <div
                      className="w-3 h-3 rounded"
                      style={{ backgroundColor: layer.color }}
                    />
                    <span className="text-xs text-foreground">{layer.name}</span>
                  </div>
                  <div className="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <Button
                      variant="ghost"
                      size="sm"
                      className="h-5 w-5 p-0"
                      onClick={() => {
                        if (layer.id === 'loads') updateViewportControl('showLoads', !layer.visible);
                        if (layer.id === 'supports') updateViewportControl('showSupports', !layer.visible);
                      }}
                    >
                      {layer.visible ? (
                        <Eye className="h-3 w-3" />
                      ) : (
                        <EyeOff className="h-3 w-3" />
                      )}
                    </Button>
                    <Button variant="ghost" size="sm" className="h-5 w-5 p-0">
                      {layer.locked ? (
                        <Lock className="h-3 w-3" />
                      ) : (
                        <Unlock className="h-3 w-3" />
                      )}
                    </Button>
                  </div>
                </div>
              ))}
            </div>

            <Separator className="my-3" />

            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label className="text-xs font-medium text-foreground">Display Options</Label>
              </div>
              <div className="space-y-2">
                <div className="flex items-center space-x-2">
                  <Checkbox 
                    id="showNodes"
                    checked={viewportControls.showNodes}
                    onCheckedChange={(checked) => updateViewportControl('showNodes', !!checked)}
                  />
                  <Label htmlFor="showNodes" className="text-xs text-foreground">Node Numbers</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox 
                    id="showElements"
                    checked={viewportControls.showElements}
                    onCheckedChange={(checked) => updateViewportControl('showElements', !!checked)}
                  />
                  <Label htmlFor="showElements" className="text-xs text-foreground">Element Labels</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox id="wireframe" />
                  <Label htmlFor="wireframe" className="text-xs text-foreground">Wireframe Mode</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <Checkbox id="shadows" defaultChecked />
                  <Label htmlFor="shadows" className="text-xs text-foreground">Shadows</Label>
                </div>
              </div>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="properties" className="flex-1 m-0 p-0">
          <ScrollArea className="flex-1">
            <div className="p-3">
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-medium text-foreground">Element Properties</span>
                <Badge className="text-xs bg-primary/20 text-primary border-primary/30">
                  {selectedElement.elementType}
                </Badge>
              </div>

              <div className="space-y-3">
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <Label className="text-xs text-muted-foreground">Element ID</Label>
                    <Input 
                      value={selectedElement.id} 
                      readOnly 
                      className="mt-1 h-7 text-xs engineering-input bg-muted"
                    />
                  </div>
                  <div>
                    <Label className="text-xs text-muted-foreground">Type</Label>
                    <Input 
                      value={selectedElement.elementType} 
                      readOnly 
                      className="mt-1 h-7 text-xs bg-muted"
                    />
                  </div>
                </div>

                <div>
                  <Label className="text-xs text-muted-foreground">Cross Section</Label>
                  <Select 
                    value={selectedElement.sectionType}
                    onValueChange={(value) => updateSelectedElement('sectionType', value)}
                  >
                    <SelectTrigger className="mt-1 h-7 text-xs">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="W18x50">W18x50</SelectItem>
                      <SelectItem value="W21x62">W21x62</SelectItem>
                      <SelectItem value="W24x76">W24x76</SelectItem>
                      <SelectItem value="W14x90">W14x90</SelectItem>
                      <SelectItem value="HSS8x8x1/2">HSS8x8x1/2</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label className="text-xs text-muted-foreground">Material</Label>
                  <Select 
                    value={selectedElement.materialType}
                    onValueChange={(value) => updateSelectedElement('materialType', value)}
                  >
                    <SelectTrigger className="mt-1 h-7 text-xs">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="A992 Steel">A992 Steel (Fy=50ksi)</SelectItem>
                      <SelectItem value="A36 Steel">A36 Steel (Fy=36ksi)</SelectItem>
                      <SelectItem value="A572 Gr50">A572 Gr50 (Fy=50ksi)</SelectItem>
                      <SelectItem value="Concrete fc=4000">Concrete fc=4000 psi</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <Label className="text-xs text-muted-foreground">Length (m)</Label>
                    <Input 
                      type="number" 
                      value={selectedElement.length}
                      onChange={(e) => updateSelectedElement('length', parseFloat(e.target.value))}
                      className="mt-1 h-7 text-xs engineering-input"
                      step="0.01"
                    />
                  </div>
                  <div>
                    <Label className="text-xs text-muted-foreground">Rotation (°)</Label>
                    <Input 
                      type="number" 
                      defaultValue="0"
                      className="mt-1 h-7 text-xs engineering-input"
                      step="1"
                    />
                  </div>
                </div>

                <Separator />

                <div>
                  <Label className="text-xs font-medium text-foreground mb-2 block">Section Properties</Label>
                  <div className="text-xs space-y-1">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Area:</span>
                      <span className="engineering-input">14.7 in²</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Ix:</span>
                      <span className="engineering-input">800 in⁴</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Iy:</span>
                      <span className="engineering-input">40.1 in⁴</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Weight:</span>
                      <span className="engineering-input">50 lb/ft</span>
                    </div>
                  </div>
                </div>

                <Separator />

                <div className="flex space-x-2">
                  <Button size="sm" className="flex-1 h-7 text-xs">
                    <Calculator className="mr-1 h-3 w-3" />
                    Analyze
                  </Button>
                  <Button variant="outline" size="sm" className="flex-1 h-7 text-xs">
                    <FileText className="mr-1 h-3 w-3" />
                    Report
                  </Button>
                </div>
              </div>
            </div>
          </ScrollArea>
        </TabsContent>
      </Tabs>

      {/* Status Bar */}
      <div className="status-bar h-6 px-3 flex items-center justify-between text-xs">
        <span>Selected: {selectedElement.id}</span>
        <span>Scale: 1:100</span>
      </div>
    </div>
  );
}
