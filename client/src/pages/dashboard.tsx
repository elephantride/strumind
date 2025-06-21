import { useState } from "react";
import { TopToolbar } from "@/components/layout/top-toolbar";
import { Sidebar } from "@/components/layout/sidebar";
import { ModelBuilder } from "@/components/model-builder/model-builder";
import { AnalysisPanel } from "@/components/analysis-panel/analysis-panel";
import { DesignResults } from "@/components/design-results/design-results";
import { BIMViewer } from "@/components/bim-viewer/bim-viewer";
import { ViewMode, ViewportControls, SelectedElement, ProjectStats } from "@/types";

export default function Dashboard() {
  const [currentView, setCurrentView] = useState<ViewMode>('model');
  const [viewportControls, setViewportControls] = useState<ViewportControls>({
    showNodes: true,
    showElements: true,
    showLoads: false,
    showSupports: false,
  });
  const [selectedElement, setSelectedElement] = useState<SelectedElement>({
    id: "B127",
    elementType: "Beam",
    sectionType: "W18x50",
    materialType: "A992 Steel",
    length: 6.10,
  });
  const [projectStats] = useState<ProjectStats>({
    nodeCount: 156,
    elementCount: 142,
    selectedElement: "Beam B127",
  });

  return (
    <div className="h-screen flex flex-col bg-background">
      <TopToolbar 
        currentView={currentView} 
        onViewChange={setCurrentView}
      />
      
      <div className="flex flex-1 overflow-hidden">
        <Sidebar
          viewportControls={viewportControls}
          onViewportControlsChange={setViewportControls}
          selectedElement={selectedElement}
          onSelectedElementChange={setSelectedElement}
          projectStats={projectStats}
        />
        
        <main className="flex-1 flex flex-col">
          {currentView === 'model' && <ModelBuilder />}
          {currentView === 'analysis' && <AnalysisPanel />}
          {currentView === 'design' && <DesignResults />}
          {currentView === 'bim' && <BIMViewer />}
        </main>
      </div>
    </div>
  );
}
