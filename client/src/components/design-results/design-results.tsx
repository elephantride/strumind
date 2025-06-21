import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { CheckCircle, AlertTriangle, XCircle, Gauge } from "lucide-react";

export function DesignResults() {
  const [designCode, setDesignCode] = useState("AISC 360-16");

  const designSummary = {
    passed: 142,
    warning: 14,
    failed: 0,
    maxUnity: 0.89,
  };

  const designResults = [
    { element: "B127", section: "W18x50", status: "pass", axialCheck: 0.42, momentCheck: 0.67, unityCheck: 0.89, governing: "H1-1a" },
    { element: "B128", section: "W21x62", status: "warning", axialCheck: 0.58, momentCheck: 0.73, unityCheck: 0.95, governing: "H1-1b" },
    { element: "C201", section: "W14x90", status: "pass", axialCheck: 0.38, momentCheck: 0.25, unityCheck: 0.56, governing: "H1-1a" },
  ];

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "pass":
        return <CheckCircle className="h-4 w-4 text-accent" />;
      case "warning":
        return <AlertTriangle className="h-4 w-4 text-yellow-600" />;
      case "fail":
        return <XCircle className="h-4 w-4 text-destructive" />;
      default:
        return null;
    }
  };

  const handleRegenerate = () => {
    console.log("Regenerating design...");
  };

  return (
    <div className="p-4">
      <h2 className="text-lg font-semibold text-foreground mb-4">Design Code Checks</h2>
      
      {/* Design Summary */}
      <div className="grid grid-cols-4 gap-4 mb-6">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-accent">{designSummary.passed}</div>
                <div className="text-xs text-muted-foreground">Elements Passed</div>
              </div>
              <CheckCircle className="h-8 w-8 text-accent" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-yellow-600">{designSummary.warning}</div>
                <div className="text-xs text-muted-foreground">Elements Warning</div>
              </div>
              <AlertTriangle className="h-8 w-8 text-yellow-600" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-destructive">{designSummary.failed}</div>
                <div className="text-xs text-muted-foreground">Elements Failed</div>
              </div>
              <XCircle className="h-8 w-8 text-destructive" />
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div>
                <div className="text-2xl font-bold text-foreground">{designSummary.maxUnity}</div>
                <div className="text-xs text-muted-foreground">Max Unity Check</div>
              </div>
              <Gauge className="h-8 w-8 text-muted-foreground" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Code Check Results */}
      <Card>
        <div className="px-4 py-3 border-b border-border flex items-center justify-between">
          <h3 className="text-sm font-semibold text-foreground">AISC 360-16 Steel Design</h3>
          <div className="flex items-center space-x-2">
            <Select value={designCode} onValueChange={setDesignCode}>
              <SelectTrigger className="w-[140px]">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="AISC 360-16">AISC 360-16</SelectItem>
                <SelectItem value="Eurocode 3">Eurocode 3</SelectItem>
                <SelectItem value="CSA S16">CSA S16</SelectItem>
              </SelectContent>
            </Select>
            <Button 
              size="sm" 
              onClick={handleRegenerate}
            >
              Regenerate
            </Button>
          </div>
        </div>
        
        <div className="overflow-auto max-h-96">
          <table className="w-full text-xs">
            <thead className="bg-muted sticky top-0">
              <tr>
                <th className="px-3 py-2 text-left font-medium text-muted-foreground">Element</th>
                <th className="px-3 py-2 text-left font-medium text-muted-foreground">Section</th>
                <th className="px-3 py-2 text-center font-medium text-muted-foreground">Status</th>
                <th className="px-3 py-2 text-right font-medium text-muted-foreground">Axial Check</th>
                <th className="px-3 py-2 text-right font-medium text-muted-foreground">Moment Check</th>
                <th className="px-3 py-2 text-right font-medium text-muted-foreground">Unity Check</th>
                <th className="px-3 py-2 text-left font-medium text-muted-foreground">Governing</th>
              </tr>
            </thead>
            <tbody>
              {designResults.map((result, index) => (
                <tr key={index} className="border-b border-border hover:bg-muted">
                  <td className="px-3 py-2 font-medium">{result.element}</td>
                  <td className="px-3 py-2">{result.section}</td>
                  <td className="px-3 py-2 text-center">
                    {getStatusIcon(result.status)}
                  </td>
                  <td className="px-3 py-2 text-right">{result.axialCheck}</td>
                  <td className="px-3 py-2 text-right">{result.momentCheck}</td>
                  <td className="px-3 py-2 text-right font-bold">{result.unityCheck}</td>
                  <td className="px-3 py-2">{result.governing}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
