// src/App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Faculties from './pages/Faculties';
import Roadmap from './pages/Roadmap';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/faculties" element={<Faculties />} />
        <Route path="/roadmap/:facultyId" element={<Roadmap />} />
        {/* Добавьте дополнительные маршруты здесь, например, для чата */}
      </Routes>
    </Router>
  );
}

export default App;
