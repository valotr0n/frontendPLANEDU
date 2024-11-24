import { useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import Header from '../compnents/Header';
import { roadmapData } from '../data/roadmapData';

export default function Roadmap() {
  const { facultyId } = useParams();
  const [expandedItems, setExpandedItems] = useState([]);

  const toggleItem = (id) => {
    setExpandedItems((prev) => 
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  const renderRoadmapItem = (item) => (
    <div key={item.id} className="mb-4">
      <div 
        className="flex items-center justify-between bg-white p-4 rounded-lg shadow cursor-pointer hover:bg-blue-100"
        onClick={() => toggleItem(item.id)}
      >
        <span>{item.name}</span>
        {item.children && (
          <span>{expandedItems.includes(item.id) ? '▼' : '▶'}</span>
        )}
      </div>
      {item.children && expandedItems.includes(item.id) && (
        <div className="ml-8 mt-2 space-y-2">
          {item.children.map((child) => (
            <Link to={`/chat/${facultyId}/${child.id}`} key={child.id}>
              <div className="bg-white p-3 rounded-lg shadow hover:bg-blue-100">
                {child.name}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-100">
      <Header />
      <main className="container mx-auto mt-8 p-4">
        <h1 className="text-3xl font-bold mb-6 text-blue-900">Учебный план: {facultyId.toUpperCase()}</h1>
        <div className="space-y-4">
          {roadmapData[facultyId]?.map(renderRoadmapItem)}
        </div>
      </main>
    </div>
  );
}