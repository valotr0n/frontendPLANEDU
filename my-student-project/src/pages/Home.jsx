// src/pages/Home.jsx
import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-blue-50">
      <h1 className="text-4xl font-bold mb-8 text-blue-900">PlanEDU</h1>
      <Link to="/faculties">
        <button className="bg-blue-900 text-white px-6 py-3 rounded hover:bg-blue-800 transition-colors">
          Войти 
        </button>
      </Link>
    </div>
  );
}
