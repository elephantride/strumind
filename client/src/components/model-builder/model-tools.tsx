import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { 
  Plus, 
  Minus, 
  Square, 
  Anchor, 
  Weight, 
  Edit3
} from "lucide-react";

export function ModelTools() {
  const tools = [
    { icon: Plus, label: 'Node', color: 'text-primary' },
    { icon: Minus, label: 'Beam', color: 'text-primary' },
    { icon: Square, label: 'Plate', color: 'text-primary' },
    { icon: Anchor, label: 'Support', color: 'text-primary' },
    { icon: Weight, label: 'Load', color: 'text-primary' },
    { icon: Edit3, label: 'Modify', color: 'text-primary' },
  ];

  return (
    <Card>
      <CardHeader className="pb-3">
        <CardTitle className="text-sm">Model Tools</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-3 gap-2">
          {tools.map((tool, index) => {
            const Icon = tool.icon;
            return (
              <Button
                key={index}
                variant="outline"
                className="p-3 h-auto flex flex-col items-center justify-center"
              >
                <Icon className={`block text-lg mb-1 h-5 w-5 ${tool.color}`} />
                <span className="text-xs">{tool.label}</span>
              </Button>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
