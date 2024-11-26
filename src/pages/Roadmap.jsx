import { useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import Header from '../compnents/Header';
import mermaid from 'mermaid';
import roadmapData from '../data/roadmapData.json';

export default function Roadmap() {
  const { facultyId } = useParams();
  const mermaidRef = useRef(null);

  const generateMermaidDiagram = (data, facultyId) => {
    const faculty = data[facultyId];
    if (!faculty) return '';

    let diagram = `
    flowchart TD
    %% Styles
    classDef default fill:#fff,stroke:#000,stroke-width:2px,color:#000;
    classDef section fill:#f6f7f8,stroke:#000,stroke-width:2px,color:#000;
    classDef recommended fill:#e7f3ff,stroke:#000,stroke-width:2px,color:#000;
    classDef optional fill:#fff,stroke:#666,stroke-width:2px,color:#666,stroke-dasharray: 5 5;
    `;

    const processNode = (node, parentId = null) => {
      const nodeId = node.id.replace(/[^a-zA-Z0-9]/g, '_');
      
      const formattedName = node.name.replace(/ /g, '<br>');
      diagram += `\n    ${nodeId}["${formattedName}"]`;
      
      if (node.type === 'section') {
        diagram += `\n    class ${nodeId} section`;
      } else if (node.optional) {
        diagram += `\n    class ${nodeId} optional`;
      } else if (node.recommended) {
        diagram += `\n    class ${nodeId} recommended`;
      }
      
      if (parentId) {
        diagram += `\n    ${parentId} --> ${nodeId}`;
      }

      if (node.children) {
        node.children.forEach(child => processNode(child, nodeId));
      }
    };

    processNode(faculty);
    return diagram;
  };

  useEffect(() => {
    mermaid.initialize({
      startOnLoad: true,
      theme: 'base',
      flowchart: {
        nodeSpacing: 30,
        rankSpacing: 100,
        curve: 'basis',
        useMaxWidth: false,
        htmlLabels: true,
        padding: 15,
      },
      securityLevel: 'loose',
      themeVariables: {
        fontFamily: 'system-ui, -apple-system, sans-serif',
        fontSize: '14px',
        primaryColor: '#000',
        primaryTextColor: '#000',
        primaryBorderColor: '#000',
        lineColor: '#000',
        secondaryColor: '#f6f7f8',
        tertiaryColor: '#fff',
      }
    });

    const renderDiagram = async () => {
      if (mermaidRef.current) {
        mermaidRef.current.innerHTML = '';
        try {
          const diagram = generateMermaidDiagram(roadmapData, facultyId);
          const { svg } = await mermaid.render('mermaid-diagram', diagram);
          mermaidRef.current.innerHTML = svg;
        } catch (error) {
          console.error('Ошибка рендеринга диаграммы:', error);
        }
      }
    };

    renderDiagram();
  }, [facultyId]);
  return (
    <div className="min-h-screen bg-white">
      <Header />
      <div className="max-w-[1200px] mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          План обучения: {facultyId.toUpperCase()}
        </h1>
        <div className="bg-white rounded-lg p-6 overflow-auto">
          <div ref={mermaidRef} className="mermaid-diagram min-w-[800px]" />
        </div>
      </div>
    </div>
  );
}