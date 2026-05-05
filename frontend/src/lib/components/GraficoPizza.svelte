<script >
    import { Chart, ArcElement, Tooltip, Legend } from 'chart.js';
    import { Pie } from 'svelte-chartjs';
	Chart.register(ArcElement, Tooltip, Legend);
    let {presentes , ausentes} = $props();
	
    let data = $derived({
		labels: ["Presentes", "Ausentes"], // eixo X
		datasets: [
			{
				data: [presentes,ausentes], // valores
				backgroundColor: ['#16a34a', '#dc2626'], // verde e vermelho
                borderWidth: 0,    // cor das barras
			}
		]
	});

    let options = {
        responsive: true,
        plugins: {
            legend: { 
                /** @type {'bottom'} */
                position: 'bottom'  // legenda embaixo do gráfico
            },
                tooltip: {
                enabled: true      // popup ao passar o mouse
            }
        }
    };
</script>

<Pie {data} {options} />