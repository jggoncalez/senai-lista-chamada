<script lang="ts">
  import { onMount } from 'svelte';
  import { Accessibility } from 'accessibility';

  onMount(() => {
    new Accessibility({
      labels: {
        menuTitle: 'Menu de Acessibilidade',
        textToSpeech: 'Leitor de texto',
        invertColors: 'Inverter Cores',
      } as any 
    });
  });
</script>