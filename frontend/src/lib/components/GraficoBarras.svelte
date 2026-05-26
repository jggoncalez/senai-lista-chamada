<script>
    import { BarElement, CategoryScale, LinearScale, Chart,Tooltip, Legend, plugins } from 'chart.js';
    import { Bar} from 'svelte-chartjs';
    Chart.register(BarElement, CategoryScale, LinearScale,Tooltip, Legend);

    let {Alunos, Labels} = $props()
    let data = $derived({
        labels: Alunos,
        datasets: [{
            label: 'Presença por Aluno',
            data: Labels,
            backgroundColor: '#dc262620',
        }]
    })

    let options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                /** @type {'bottom'}*/
                position: 'bottom'
            },
            tooltip: {
                enabled : true
            }
        }
    }
</script>

<div class="w-full" style="height: 400px;">
    <Bar {data} {options} />
</div>