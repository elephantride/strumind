import { apiRequest } from '@/lib/queryClient';

// Base API URL
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Project API
export const projectApi = {
  getProjects: async () => {
    const response = await apiRequest('GET', `${API_BASE_URL}/projects`);
    return response.json();
  },
  getProject: async (id: string) => {
    const response = await apiRequest('GET', `${API_BASE_URL}/projects/${id}`);
    return response.json();
  },
  createProject: async (data: any) => {
    const response = await apiRequest('POST', `${API_BASE_URL}/projects`, data);
    return response.json();
  },
  updateProject: async (id: string, data: any) => {
    const response = await apiRequest('PUT', `${API_BASE_URL}/projects/${id}`, data);
    return response.json();
  },
  deleteProject: async (id: string) => {
    const response = await apiRequest('DELETE', `${API_BASE_URL}/projects/${id}`);
    return response.json();
  }
};

// Node API
export const nodeApi = {
  getNodes: async (projectId?: string) => {
    const url = projectId 
      ? `${API_BASE_URL}/nodes?project_id=${projectId}` 
      : `${API_BASE_URL}/nodes`;
    const response = await apiRequest('GET', url);
    return response.json();
  },
  getNode: async (id: string) => {
    const response = await apiRequest('GET', `${API_BASE_URL}/nodes/${id}`);
    return response.json();
  },
  createNode: async (data: any) => {
    const response = await apiRequest('POST', `${API_BASE_URL}/nodes`, data);
    return response.json();
  },
  updateNode: async (id: string, data: any) => {
    const response = await apiRequest('PUT', `${API_BASE_URL}/nodes/${id}`, data);
    return response.json();
  },
  deleteNode: async (id: string) => {
    const response = await apiRequest('DELETE', `${API_BASE_URL}/nodes/${id}`);
    return response.json();
  }
};

// Element API
export const elementApi = {
  getElements: async (projectId?: string) => {
    const url = projectId 
      ? `${API_BASE_URL}/elements?project_id=${projectId}` 
      : `${API_BASE_URL}/elements`;
    const response = await apiRequest('GET', url);
    return response.json();
  },
  getElement: async (id: string) => {
    const response = await apiRequest('GET', `${API_BASE_URL}/elements/${id}`);
    return response.json();
  },
  createElement: async (data: any) => {
    const response = await apiRequest('POST', `${API_BASE_URL}/elements`, data);
    return response.json();
  },
  updateElement: async (id: string, data: any) => {
    const response = await apiRequest('PUT', `${API_BASE_URL}/elements/${id}`, data);
    return response.json();
  },
  deleteElement: async (id: string) => {
    const response = await apiRequest('DELETE', `${API_BASE_URL}/elements/${id}`);
    return response.json();
  }
};

// Material API
export const materialApi = {
  getMaterials: async (projectId?: string) => {
    const url = projectId 
      ? `${API_BASE_URL}/materials?project_id=${projectId}` 
      : `${API_BASE_URL}/materials`;
    const response = await apiRequest('GET', url);
    return response.json();
  },
  getMaterial: async (id: string) => {
    const response = await apiRequest('GET', `${API_BASE_URL}/materials/${id}`);
    return response.json();
  },
  createMaterial: async (data: any) => {
    const response = await apiRequest('POST', `${API_BASE_URL}/materials`, data);
    return response.json();
  },
  updateMaterial: async (id: string, data: any) => {
    const response = await apiRequest('PUT', `${API_BASE_URL}/materials/${id}`, data);
    return response.json();
  },
  deleteMaterial: async (id: string) => {
    const response = await apiRequest('DELETE', `${API_BASE_URL}/materials/${id}`);
    return response.json();
  }
};

// Section API
export const sectionApi = {
  getSections: async (projectId?: string) => {
    const url = projectId 
      ? `${API_BASE_URL}/sections?project_id=${projectId}` 
      : `${API_BASE_URL}/sections`;
    const response = await apiRequest('GET', url);
    return response.json();
  },
  getSection: async (id: string) => {
    const response = await apiRequest('GET', `${API_BASE_URL}/sections/${id}`);
    return response.json();
  },
  createSection: async (data: any) => {
    const response = await apiRequest('POST', `${API_BASE_URL}/sections`, data);
    return response.json();
  },
  updateSection: async (id: string, data: any) => {
    const response = await apiRequest('PUT', `${API_BASE_URL}/sections/${id}`, data);
    return response.json();
  },
  deleteSection: async (id: string) => {
    const response = await apiRequest('DELETE', `${API_BASE_URL}/sections/${id}`);
    return response.json();
  }
};

// Load API
export const loadApi = {
  getLoadCases: async (projectId?: string) => {
    const url = projectId 
      ? `${API_BASE_URL}/loads/cases?project_id=${projectId}` 
      : `${API_BASE_URL}/loads/cases`;
    const response = await apiRequest('GET', url);
    return response.json();
  },
  getLoadCase: async (id: string) => {
    const response = await apiRequest('GET', `${API_BASE_URL}/loads/cases/${id}`);
    return response.json();
  },
  createLoadCase: async (data: any) => {
    const response = await apiRequest('POST', `${API_BASE_URL}/loads/cases`, data);
    return response.json();
  },
  getLoadCombinations: async (projectId?: string) => {
    const url = projectId 
      ? `${API_BASE_URL}/loads/combinations?project_id=${projectId}` 
      : `${API_BASE_URL}/loads/combinations`;
    const response = await apiRequest('GET', url);
    return response.json();
  },
  createLoad: async (data: any) => {
    const response = await apiRequest('POST', `${API_BASE_URL}/loads`, data);
    return response.json();
  }
};

// Analysis API
export const analysisApi = {
  getAnalyses: async (projectId?: string) => {
    const url = projectId 
      ? `${API_BASE_URL}/analysis?project_id=${projectId}` 
      : `${API_BASE_URL}/analysis`;
    const response = await apiRequest('GET', url);
    return response.json();
  },
  getAnalysis: async (id: string) => {
    const response = await apiRequest('GET', `${API_BASE_URL}/analysis/${id}`);
    return response.json();
  },
  createAnalysis: async (data: any) => {
    const response = await apiRequest('POST', `${API_BASE_URL}/analysis`, data);
    return response.json();
  },
  runAnalysis: async (analysisId: string) => {
    const response = await apiRequest('POST', `${API_BASE_URL}/analysis/run`, { analysis_id: analysisId });
    return response.json();
  },
  getNodeResults: async (analysisId: string, nodeId?: string) => {
    const url = nodeId 
      ? `${API_BASE_URL}/analysis/${analysisId}/node-results?node_id=${nodeId}` 
      : `${API_BASE_URL}/analysis/${analysisId}/node-results`;
    const response = await apiRequest('GET', url);
    return response.json();
  },
  getElementResults: async (analysisId: string, elementId?: string) => {
    const url = elementId 
      ? `${API_BASE_URL}/analysis/${analysisId}/element-results?element_id=${elementId}` 
      : `${API_BASE_URL}/analysis/${analysisId}/element-results`;
    const response = await apiRequest('GET', url);
    return response.json();
  },
  getModalResults: async (analysisId: string) => {
    const response = await apiRequest('GET', `${API_BASE_URL}/analysis/${analysisId}/modal-results`);
    return response.json();
  }
};

// Design API
export const designApi = {
  getDesigns: async (projectId?: string) => {
    const url = projectId 
      ? `${API_BASE_URL}/design?project_id=${projectId}` 
      : `${API_BASE_URL}/design`;
    const response = await apiRequest('GET', url);
    return response.json();
  },
  getDesign: async (id: string) => {
    const response = await apiRequest('GET', `${API_BASE_URL}/design/${id}`);
    return response.json();
  },
  createDesign: async (data: any) => {
    const response = await apiRequest('POST', `${API_BASE_URL}/design`, data);
    return response.json();
  },
  runDesign: async (designId: string) => {
    const response = await apiRequest('POST', `${API_BASE_URL}/design/run`, { design_id: designId });
    return response.json();
  },
  getElementDesignResults: async (designId: string, elementId?: string) => {
    const url = elementId 
      ? `${API_BASE_URL}/design/${designId}/element-results?element_id=${elementId}` 
      : `${API_BASE_URL}/design/${designId}/element-results`;
    const response = await apiRequest('GET', url);
    return response.json();
  }
};

// BIM API
export const bimApi = {
  getBimModels: async (projectId?: string) => {
    const url = projectId 
      ? `${API_BASE_URL}/bim/models?project_id=${projectId}` 
      : `${API_BASE_URL}/bim/models`;
    const response = await apiRequest('GET', url);
    return response.json();
  },
  createBimModel: async (data: any) => {
    const response = await apiRequest('POST', `${API_BASE_URL}/bim/models`, data);
    return response.json();
  },
  generateGeometry: async (projectId: string, modelId: string, elementIds?: string[]) => {
    const data = {
      project_id: projectId,
      model_id: modelId,
      element_ids: elementIds
    };
    const response = await apiRequest('POST', `${API_BASE_URL}/bim/generate-geometry`, data);
    return response.json();
  },
  getViewerData: async (projectId: string, modelId?: string) => {
    const url = modelId 
      ? `${API_BASE_URL}/bim/viewer-data/${projectId}?model_id=${modelId}` 
      : `${API_BASE_URL}/bim/viewer-data/${projectId}`;
    const response = await apiRequest('GET', url);
    return response.json();
  }
};

// Detailing API
export const detailingApi = {
  getDetailings: async (projectId?: string) => {
    const url = projectId 
      ? `${API_BASE_URL}/detailing?project_id=${projectId}` 
      : `${API_BASE_URL}/detailing`;
    const response = await apiRequest('GET', url);
    return response.json();
  },
  createDetailing: async (data: any) => {
    const response = await apiRequest('POST', `${API_BASE_URL}/detailing`, data);
    return response.json();
  },
  runDetailing: async (detailingId: string) => {
    const response = await apiRequest('POST', `${API_BASE_URL}/detailing/run`, { detailing_id: detailingId });
    return response.json();
  },
  getElementDetailings: async (detailingId: string, elementId?: string) => {
    const url = elementId 
      ? `${API_BASE_URL}/detailing/${detailingId}/element-detailings?element_id=${elementId}` 
      : `${API_BASE_URL}/detailing/${detailingId}/element-detailings`;
    const response = await apiRequest('GET', url);
    return response.json();
  },
  getConnectionDetails: async (detailingId: string, elementId?: string) => {
    const url = elementId 
      ? `${API_BASE_URL}/detailing/${detailingId}/connection-details?element_id=${elementId}` 
      : `${API_BASE_URL}/detailing/${detailingId}/connection-details`;
    const response = await apiRequest('GET', url);
    return response.json();
  },
  generateConnections: async (detailingId: string, elementIds: string[], connectionOptions?: any) => {
    const data = {
      detailing_id: detailingId,
      element_ids: elementIds,
      connection_options: connectionOptions
    };
    const response = await apiRequest('POST', `${API_BASE_URL}/detailing/generate-connections`, data);
    return response.json();
  }
};