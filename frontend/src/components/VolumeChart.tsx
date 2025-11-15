import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

interface VolumeChartProps {
  mentions: { published_at: string }[];
}

const VolumeChart = ({ mentions }: VolumeChartProps) => {
  // Group mentions by day
  const countsByDay = mentions.reduce((acc, mention) => {
    const date = new Date(mention.published_at).toLocaleDateString();
    acc[date] = (acc[date] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const chartData = {
    labels: Object.keys(countsByDay).reverse(),
    datasets: [
      {
        label: 'Mentions per Day',
        data: Object.values(countsByDay).reverse(),
        fill: true,
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { display: false },
      title: {
        display: true,
        text: 'Mention Volume Over Time',
        font: { size: 18 },
      },
    },
  };

  return <Line data={chartData} options={options} />;
};

export default VolumeChart;