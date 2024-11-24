import { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import Header from '../compnents/Header';
import mermaid from 'mermaid';

export default function Roadmap() {
  const { facultyId } = useParams();

  useEffect(() => {
    mermaid.initialize({
      startOnLoad: true,
      theme: 'neutral',
      flowchart: {
        nodeSpacing: 50,
        rankSpacing: 50,
        curve: 'basis',
        useMaxWidth: false,
      },
      themeVariables: {
        fontFamily: 'system-ui, -apple-system, sans-serif',
        fontSize: '16px',
        nodeBorder: '#2563eb',
        mainBkg: '#ffffff',
        nodeTextColor: '#000000',
      }
    });
  }, []);

  const getMermaidDiagram = () => {
    return `
    flowchart TB
    classDef default fill:#fff,stroke:#2563eb,stroke-width:2px,color:#000;
    classDef section fill:#f8fafc,stroke:#2563eb,stroke-width:2px,color:#000;
    classDef recommended fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#000;
    classDef optional fill:#fff,stroke:#94a3b8,stroke-width:2px,color:#000,stroke-dasharray: 5 5;

    %% Основная математика
    A[Основная математика]

    %% Первый уровень
    A --> B[Алгебра]
    A --> C[Геометрия]
    A --> D[Математический анализ]

    %% Алгебра
    subgraph Алгебра
    B --> B1[Линейная алгебра]
    B --> B2[Абстрактная алгебра]
    
    B1 --> B1_1[Матрицы и определители]
    B1 --> B1_2[Системы линейных уравнений]
    B1_1 --> B1_1_1[Операции над матрицами]
    B1_1 --> B1_1_2[Вычисление определителей]
    B1_2 --> B1_2_1[Метод Гаусса]
    B1_2 --> B1_2_2[Метод Крамера]
    
    B2 --> B2_1[Группы и кольца]
    B2 --> B2_2[Поля и векторные пространства]
    end

    %% Геометрия
    subgraph Геометрия
    C --> C1[Планиметрия]
    C --> C2[Стереометрия]
    C --> C3[Аналитическая геометрия]
    
    C1 --> C1_1[Треугольники]
    C1 --> C1_2[Окружности]
    C1_1 --> C1_1_1[Признаки равенства]
    C1_1 --> C1_1_2[Признаки подобия]
    
    C2 --> C2_1[Многогранники]
    C2 --> C2_2[Тела вращения]
    
    C3 --> C3_1[Векторы]
    C3 --> C3_2[Координатный метод]
    end

    %% Математический анализ
    subgraph Мат_анализ[Математический анализ]
    D --> D1[Дифференциальное исчисление]
    D --> D2[Интегральное исчисление]
    
    D1 --> D1_1[Пределы]
    D1 --> D1_2[Производные]
    D1_1 --> D1_1_1[Предел последовательности]
    D1_1 --> D1_1_2[Предел функции]
    D1_2 --> D1_2_1[Правила дифференцирования]
    D1_2 --> D1_2_2[Приложения производной]
    
    D2 --> D2_1[Неопределенные интегралы]
    D2 --> D2_2[Определенные интегралы]
    end

    %% Дополнительные разделы
    A --> E[Дискретная математика]
    A --> F[Теория вероятностей]
    A --> G[Математическая статистика]

    subgraph Доп_разделы[Дополнительные разделы]
    E --> E1[Комбинаторика]
    E --> E2[Теория графов]
    
    F --> F1[Случайные события]
    F --> F2[Случайные величины]
    
    G --> G1[Описательная статистика]
    G --> G2[Статистические гипотезы]
    end

    %% Стили
    class A,B,C,D section;
    class E,F,G recommended;
    class B2,C3,D2 optional;
    `;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          План обучения: {facultyId.toUpperCase()}
        </h1>
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="mermaid w-full" style={{ minWidth: '800px' }}>
            {getMermaidDiagram()}
          </div>
        </div>
      </div>
    </div>
  );
}