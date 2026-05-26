<script>
  import { Chart, LineElement, PointElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js';
  import { Line } from 'svelte-chartjs';

  Chart.register(LineElement, PointElement, CategoryScale, LinearScale, Tooltip, Legend);

  let { labels, presenca } = $props();

  let data = $derived({
    labels: labels,
    datasets: [{
      label: '% Presença',
      data: presenca,
      borderColor: '#dc2626',
      backgroundColor: '#dc262620',
      tension: 0.4,
      fill: false,
    }]
  });

  let options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        /** @type {'bottom'} */
        position: 'bottom'
      },
      tooltip: { enabled: true }
    }
  };
</script>


<div class="w-full" style="height: 700px;">
  <Line {data} {options} />
</div>