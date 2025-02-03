export default defineNuxtConfig({
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  plugins: [
    { src: '~/plugins/mitt.js', mode: 'client' },
  ],
  components: [
    {
      path: '~/components',
      pathPrefix: false, // [!code ++]
    },
  ],

  compatibilityDate: '2025-01-22',
})