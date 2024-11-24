import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

export default function D3Roadmap({ data }) {
  const svgRef = useRef(null);

  useEffect(() => {
    if (!data || !svgRef.current) return;

    // Очищаем предыдущий SVG
    d3.select(svgRef.current).selectAll("*").remove();

    // Настройка размеров
    const width = 1200;
    const height = 800;
    const nodeWidth = 200;
    const nodeHeight = 60;

    // Создаем иерархию данных
    const hierarchy = d3.hierarchy(data);
    
    // Создаем дерево
    const treeLayout = d3.tree()
      .size([height - 100, width - 400]);

    // Применяем layout к данным
    const root = treeLayout(hierarchy);

    // Создаем SVG
    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(50, 50)`);

    // Добавляем связи
    svg.selectAll('path.link')
      .data(root.links())
      .enter()
      .append('path')
      .attr('class', 'link')
      .attr('d', d3.linkHorizontal()
        .x(d => d.y)
        .y(d => d.x))
      .attr('fill', 'none')
      .attr('stroke', '#4B5563')
      .attr('stroke-width', 1.5);

    // Создаем группы для узлов
    const nodes = svg.selectAll('g.node')
      .data(root.descendants())
      .enter()
      .append('g')
      .attr('class', 'node')
      .attr('transform', d => `translate(${d.y},${d.x})`);

    // Добавляем прямоугольники для узлов
    nodes.append('rect')
      .attr('width', nodeWidth)
      .attr('height', nodeHeight)
      .attr('x', -nodeWidth / 2)
      .attr('y', -nodeHeight / 2)
      .attr('rx', 8)
      .attr('ry', 8)
      .attr('fill', 'white')
      .attr('stroke', '#4B5563')
      .attr('stroke-width', 2)
      .on('mouseover', function() {
        d3.select(this)
          .attr('stroke', '#2563EB')
          .attr('transform', 'scale(1.05)');
      })
      .on('mouseout', function() {
        d3.select(this)
          .attr('stroke', '#4B5563')
          .attr('transform', 'scale(1)');
      });

    // Добавляем текст
    nodes.append('text')
      .attr('dy', '0.35em')
      .attr('text-anchor', 'middle')
      .attr('font-size', '14px')
      .attr('font-weight', 'medium')
      .text(d => d.data.name)
      .call(wrap, nodeWidth - 20);

    // Функция для переноса длинного текста
    function wrap(text, width) {
      text.each(function() {
        const text = d3.select(this);
        const words = text.text().split(/\s+/).reverse();
        let word;
        let line = [];
        let lineNumber = 0;
        const lineHeight = 1.1;
        const y = text.attr('y');
        const dy = parseFloat(text.attr('dy'));
        let tspan = text.text(null).append('tspan').attr('x', 0).attr('y', y).attr('dy', dy + 'em');
        
        while (word = words.pop()) {
          line.push(word);
          tspan.text(line.join(' '));
          if (tspan.node().getComputedTextLength() > width) {
            line.pop();
            tspan.text(line.join(' '));
            line = [word];
            tspan = text.append('tspan').attr('x', 0).attr('y', y).attr('dy', ++lineNumber * lineHeight + dy + 'em').text(word);
          }
        }
      });
    }
  }, [data]);

  return (
    <div className="overflow-auto">
      <svg ref={svgRef} className="min-w-full"></svg>
    </div>
  );
}