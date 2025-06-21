import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Plus, Play } from "lucide-react";
import { AnalysisOptions, BoundaryConditions } from "@/types";

export function AnalysisPanel() {
  const [analysisOptions, setAnalysisOptions] = useState<AnalysisOptions>({
    analysisType: "Linear Static",
    includeGeometry: false,
    includeShear: true,
  });

  const [boundaryConditions, setBoundaryConditions] = useState<BoundaryConditions>({
    supportType: "Fixed",
    restraints: {
      tx: true,
      ty: true,
      tz: true,
      rx: false,
      ry: false,
      rz: false,
    },
  });

  const loadCases = [
    { name: "Dead Load", description: "Self weight + permanent loads", active: true },
    { name: "Live Load", description: "Occupancy loads", active: true },
    { name: "Wind Load X", description: "Wind in X direction", active: false },
  ];

  const analysisResults = [
    { element: "B127", axial: -245.8, shearY: 12.5, shearZ: -8.2, momentY: 156.3, momentZ: -89.7 },
    { element: "B128", axial: -189.4, shearY: 15.8, shearZ: -6.1, momentY: 198.7, momentZ: -124.5 },
  ];

  const handleSolve = () => {
    console.log("Running analysis...");
  };

  return (
    <div className="flex h-full">
      {/* Analysis Controls */}
      <div className="w-96 bg-surface border-r border-border p-4">
        <h2 className="text-lg font-semibold text-foreground mb-4">Analysis Control</h2>
        
        {/* Load Cases */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-semibold text-foreground">Load Cases</h3>
            <Button variant="ghost" size="sm" className="text-xs text-primary hover:text-blue-700">
              <Plus className="mr-1 h-3 w-3" />
              Add Case
            </Button>
          </div>
          
          <div className="space-y-2">
            {loadCases.map((loadCase, index) => (
              <div key={index} className="flex items-center justify-between p-3 border rounded-md">
                <div>
                  <div className="font-medium text-sm">{loadCase.name}</div>
                  <div className="text-xs text-muted-foreground">{loadCase.description}</div>
                </div>
                <Checkbox checked={loadCase.active} />
              </div>
            ))}
          </div>
        </div>

        {/* Boundary Conditions */}
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-foreground mb-3">Boundary Conditions</h3>
          <div className="space-y-3">
            <div>
              <Label className="text-xs font-medium text-muted-foreground">Support Type</Label>
              <Select value={boundaryConditions.supportType}>
                <SelectTrigger className="mt-1">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Fixed">Fixed</SelectItem>
                  <SelectItem value="Pinned">Pinned</SelectItem>
                  <SelectItem value="Roller">Roller</SelectItem>
                  <SelectItem value="Spring">Spring</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="grid grid-cols-3 gap-2">
              <div className="flex items-center space-x-2">
                <Checkbox checked={boundaryConditions.restraints.tx} id="tx" />
                <Label htmlFor="tx" className="text-xs">Tx</Label>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox checked={boundaryConditions.restraints.ty} id="ty" />
                <Label htmlFor="ty" className="text-xs">Ty</Label>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox checked={boundaryConditions.restraints.tz} id="tz" />
                <Label htmlFor="tz" className="text-xs">Tz</Label>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox checked={boundaryConditions.restraints.rx} id="rx" />
                <Label htmlFor="rx" className="text-xs">Rx</Label>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox checked={boundaryConditions.restraints.ry} id="ry" />
                <Label htmlFor="ry" className="text-xs">Ry</Label>
              </div>
              <div className="flex items-center space-x-2">
                <Checkbox checked={boundaryConditions.restraints.rz} id="rz" />
                <Label htmlFor="rz" className="text-xs">Rz</Label>
              </div>
            </div>
          </div>
        </div>

        {/* Analysis Options */}
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-foreground mb-3">Analysis Options</h3>
          <div className="space-y-3">
            <div>
              <Label className="text-xs font-medium text-muted-foreground">Analysis Type</Label>
              <Select value={analysisOptions.analysisType}>
                <SelectTrigger className="mt-1">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Linear Static">Linear Static</SelectItem>
                  <SelectItem value="Modal">Modal</SelectItem>
                  <SelectItem value="Response Spectrum">Response Spectrum</SelectItem>
                  <SelectItem value="Time History">Time History</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="flex items-center space-x-2">
              <Checkbox 
                checked={analysisOptions.includeGeometry} 
                id="geometry"
              />
              <Label htmlFor="geometry" className="text-sm">Include P-Delta effects</Label>
            </div>
            <div className="flex items-center space-x-2">
              <Checkbox 
                checked={analysisOptions.includeShear} 
                id="shear"
              />
              <Label htmlFor="shear" className="text-sm">Include shear deformation</Label>
            </div>
          </div>
        </div>

        {/* Solve Button */}
        <div className="space-y-2">
          <Button 
            onClick={handleSolve}
            className="w-full bg-accent hover:bg-accent/90"
          >
            <Play className="mr-2 h-4 w-4" />
            Run Analysis
          </Button>
          <div className="text-xs text-muted-foreground text-center">
            Last run: Today 2:45 PM
          </div>
        </div>
      </div>

      {/* Analysis Results */}
      <div className="flex-1 p-4">
        <h2 className="text-lg font-semibold text-foreground mb-4">Analysis Results</h2>
        
        {/* Results Summary */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          <Card>
            <CardContent className="p-4">
              <div className="text-2xl font-bold text-foreground">12.5</div>
              <div className="text-xs text-muted-foreground">Max Displacement (mm)</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <div className="text-2xl font-bold text-foreground">245.8</div>
              <div className="text-xs text-muted-foreground">Max Stress (MPa)</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <div className="text-2xl font-bold text-foreground">2.45</div>
              <div className="text-xs text-muted-foreground">1st Mode (Hz)</div>
            </CardContent>
          </Card>
        </div>

        {/* Results Table */}
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Element Forces</CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <div className="overflow-auto max-h-96">
              <table className="w-full text-xs">
                <thead className="bg-muted sticky top-0">
                  <tr>
                    <th className="px-3 py-2 text-left font-medium text-muted-foreground">Element</th>
                    <th className="px-3 py-2 text-right font-medium text-muted-foreground">Axial (kN)</th>
                    <th className="px-3 py-2 text-right font-medium text-muted-foreground">Shear Y (kN)</th>
                    <th className="px-3 py-2 text-right font-medium text-muted-foreground">Shear Z (kN)</th>
                    <th className="px-3 py-2 text-right font-medium text-muted-foreground">Moment Y (kN⋅m)</th>
                    <th className="px-3 py-2 text-right font-medium text-muted-foreground">Moment Z (kN⋅m)</th>
                  </tr>
                </thead>
                <tbody>
                  {analysisResults.map((result, index) => (
                    <tr key={index} className="border-b border-border hover:bg-muted">
                      <td className="px-3 py-2 font-medium">{result.element}</td>
                      <td className="px-3 py-2 text-right">{result.axial}</td>
                      <td className="px-3 py-2 text-right">{result.shearY}</td>
                      <td className="px-3 py-2 text-right">{result.shearZ}</td>
                      <td className="px-3 py-2 text-right">{result.momentY}</td>
                      <td className="px-3 py-2 text-right">{result.momentZ}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
