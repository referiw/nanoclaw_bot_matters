import { defineConfig } from '@quasar/app-vite'

export default defineConfig((ctx) => {
  return {
    boot: ['axios'],
    css: ['app.scss'],
    extras: [
      'roboto-font',
      'material-icons',
      'fontawesome-v6'
    ],
    build: {
      vueRouterMode: 'history',
      target: {
        browser: ['es2019', 'edge88', 'firefox78', 'chrome87', 'safari13.1'],
        node: 'node16'
      },
      vueRouterBase: '/',
      vitePlugins: [],
      extendViteConf(viteConf) {
        if (!viteConf.define) viteConf.define = {}
        viteConf.define.__VUE_PROD_HYDRATION_MISMATCH_DETAILS__ = false
      }
    },
    devServer: {
      open: true
    },
    framework: {
      config: {
        brand: {
          primary: '#1976D2',
          secondary: '#424242',
          accent: '#9C27B0',
          dark: '#1d1d1d',
          positive: '#21BA45',
          negative: '#C10015',
          info: '#31CCEC',
          warning: '#F2C037'
        },
        dark: 'auto'
      },
      iconSet: 'material-icons',
      lang: 'zh-CN',
      plugins: ['Notify', 'Loading', 'Dialog']
    },
    animations: [],
    ssr: {
      pwa: false,
      prodPort: 3000,
      extendSSRWebServerConf(esbuildBuildOptions) {},
      middlewares: []
    },
    pwa: {
      workboxMode: 'generateSW',
      injectPwaMetaTags: true,
      swFilename: 'sw.js',
      manifestFilename: 'manifest.json',
      useCredentialsForManifestTag: false
    },
    capacitor: {
      hideSplashscreen: true
    },
    electron: {
      inspectPort: 5858,
      bundler: 'packager',
      packager: {},
      builder: {
        appId: 'stage1st-report'
      }
    }
  }
})
