// src/pages/Faculties.jsx
import { Link } from 'react-router-dom';
import Header from '../compnents/Header';

const faculties = [
  { id: 'vmo', name: 'ВМО' },
  { id: 'vpr', name: 'ВПР' },
  { id: 'vkb', name: 'ВКБ' },
  { id: 'vias', name: 'ВИАС' },
  { id: 'vis', name: 'ВИАС' },
];

export default function Faculties() {
  return (
    <div className="min-h-screen bg-blue-50">
      <Header />
      <main className="container mx-auto mt-8 p-4">
        <h1 className="text-3xl font-bold mb-6 text-blue-900">Выберите факультет</h1>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {faculties.map((faculty) => (
            <Link
              key={faculty.id}
              to={`/roadmap/${faculty.id}`}
              className="bg-white p-6 rounded-lg shadow-md text-center text-blue-900 font-semibold hover:bg-blue-100 transition-colors"
            >
              {faculty.name}
            </Link>
          ))}
        </div>
      </main>
    </div>
  );
}
