import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Plus } from "lucide-react";

interface ElementGridProps {
  elements: Array<{
    id: string;
    type: string;
    section: string;
    length: string;
  }>;
}

export function ElementGrid({ elements }: ElementGridProps) {
  const defaultElements = [
    { id: "B127", type: "Beam", section: "W18x50", length: "6.10m" },
    { id: "B128", type: "Beam", section: "W21x62", length: "8.50m" },
    { id: "C201", type: "Column", section: "W14x90", length: "4.20m" },
  ];

  const displayElements = elements.length > 0 ? elements : defaultElements;

  return (
    <Card className="flex-1">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm">Elements</CardTitle>
          <Button variant="ghost" size="sm" className="text-xs text-primary hover:text-blue-700">
            <Plus className="mr-1 h-3 w-3" />
            Add
          </Button>
        </div>
      </CardHeader>
      <CardContent className="p-0">
        <div className="border rounded-md mx-4 mb-4">
          <div className="bg-muted px-3 py-2 text-xs font-medium text-muted-foreground border-b">
            <div className="grid grid-cols-4 gap-2">
              <span>ID</span>
              <span>Type</span>
              <span>Section</span>
              <span>Length</span>
            </div>
          </div>
          <div className="max-h-48 overflow-y-auto">
            {displayElements.map((element, index) => (
              <div 
                key={element.id}
                className="px-3 py-2 text-xs border-b border-border hover:bg-muted cursor-pointer"
              >
                <div className="grid grid-cols-4 gap-2">
                  <span className="font-medium">{element.id}</span>
                  <span>{element.type}</span>
                  <span>{element.section}</span>
                  <span>{element.length}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
