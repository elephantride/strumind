import { Viewport3D } from "./viewport-3d";
import { ModelTools } from "./model-tools";
import { ElementGrid } from "./element-grid";

export function ModelBuilder() {
  const projectStats = {
    nodeCount: 156,
    elementCount: 142,
    selectedElement: "Beam B127",
  };

  const elements = []; // Empty array - will show default elements

  return (
    <div className="flex-1 flex">
      <Viewport3D stats={projectStats} />
      
      {/* Tools Panel */}
      <div className="w-80 bg-surface border-l border-border flex flex-col">
        <div className="p-4 border-b border-border">
          <ModelTools />
        </div>
        
        <div className="flex-1 p-4">
          <ElementGrid elements={elements} />
        </div>
      </div>
    </div>
  );
}
