import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

// Register the necessary components for Chart.js
ChartJS.register(ArcElement, Tooltip, Legend);

// Define the type for the props that this component will accept
interface SentimentPieChartProps {
  data: {
    positive: number;
    negative: number;
    neutral: number;
  };
}

const SentimentPieChart = ({ data }: SentimentPieChartProps) => {
  const chartData = {
    labels: ['Positive', 'Negative', 'Neutral'],
    datasets: [
      {
        label: '# of Mentions',
        data: [data.positive, data.negative, data.neutral],
        backgroundColor: [
          'rgba(75, 192, 192, 0.6)', // Green
          'rgba(255, 99, 132, 0.6)',  // Red
          'rgba(201, 203, 207, 0.6)'  // Gray
        ],
        borderColor: [
          'rgba(75, 192, 192, 1)',
          'rgba(255, 99, 132, 1)',
          'rgba(201, 203, 207, 1)'
        ],
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Sentiment Breakdown',
        font: {
          size: 18
        }
      },
    },
  };

  return <Pie data={chartData} options={options} />;
};

export default SentimentPieChart;