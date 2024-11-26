import { Link } from 'react-router-dom';

export default function Header() {
  return (
    <header className="bg-blue-900 text-white p-4">
      <nav className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold">
          PlanEdu
        </Link>
        <div className="flex gap-6">
          <Link to="/chat" className="hover:underline">
            Помощник
          </Link>
          <Link to="/" className="hover:underline">
            Выйти
          </Link>
        </div>
      </nav>
    </header>
  );
}
