<template>
    <header class="site-header">
        <canvas ref="bgCanvas" class="bg-canvas"></canvas>
        <h1>Test Project</h1>
    </header>
</template>

<script>
export default {
    name: 'SiteHeader',
    mounted() {
    this.initParticles();
  },
  methods: {
    initParticles() {
      const canvas = this.$refs.bgCanvas;
      const ctx = canvas.getContext('2d');
      let particles = [];

      const resize = () => {
          const header = canvas.parentElement;
          const width = header.clientWidth;
          const height = header.clientHeight;

          canvas.style.width = `${width}px`;
          canvas.style.height = `${height}px`;
          canvas.width = width;
          canvas.height = height;
        };
      window.addEventListener('resize', resize);
      resize();

      const createParticles = () => {
        particles = [];
        for (let i = 0; i < 100; i++) {
          particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: Math.random() * 2 + 1,
            dx: (Math.random() - 0.5) * 0.5,
            dy: (Math.random() - 0.5) * 0.5,
            color: `hsl(${Math.random() * 360}, 100%, 70%)`
          });
        }
      };

      const animate = () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => {
          p.x += p.dx;
          p.y += p.dy;

          // wrap around screen edges
          if (p.x < 0) p.x = canvas.width;
          if (p.x > canvas.width) p.x = 0;
          if (p.y < 0) p.y = canvas.height;
          if (p.y > canvas.height) p.y = 0;

          ctx.beginPath();
          ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
          ctx.fillStyle = p.color;
          ctx.fill();
        });

        requestAnimationFrame(animate);
      };

      createParticles();
      animate();
    }
  }
}
</script>

<style scoped>

.site-header {
    background-color: #2d3b8a;
    color: white;
    padding: 10px 20px;
    text-align: center;
    font-family: 'Montserrat';
    height: 100px;
    user-select: none;
}

.bg-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: block;
  z-index: 0;
  pointer-events: none;
}

.site-header h1 {
  position: relative;
  z-index: 0;
  font-size: 3rem;
}
</style>