export interface ViewportControls {
  showNodes: boolean;
  showElements: boolean;
  showLoads: boolean;
  showSupports: boolean;
}

export interface SelectedElement {
  id: string;
  elementType: string;
  sectionType: string;
  materialType: string;
  length: number;
}

export interface AnalysisOptions {
  analysisType: string;
  includeGeometry: boolean;
  includeShear: boolean;
}

export interface BoundaryConditions {
  supportType: string;
  restraints: {
    tx: boolean;
    ty: boolean;
    tz: boolean;
    rx: boolean;
    ry: boolean;
    rz: boolean;
  };
}

export interface ProjectStats {
  nodeCount: number;
  elementCount: number;
  selectedElement?: string;
}

export type ViewMode = 'model' | 'analysis' | 'design' | 'bim';
