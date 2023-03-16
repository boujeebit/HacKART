import Vue from 'vue'
import App from './App.vue'
import router from "./router";

import { BootstrapVue } from 'bootstrap-vue'
// Import Bootstrap and BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue)
Vue.use(require('vue-moment'))

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import specific icons */
import { faCircleQuestion, faCircle, faCircleExclamation, faCircleCheck, faTriangleExclamation, faSquareCheck } from '@fortawesome/free-solid-svg-icons'

/* add icons to the library */
library.add(faCircleQuestion, faCircle, faCircleExclamation, faCircleCheck, faTriangleExclamation, faSquareCheck)

/* add font awesome icon component */
Vue.component('font-awesome-icon', FontAwesomeIcon)


import VueApollo from 'vue-apollo'
Vue.use(VueApollo)

import ApolloClient from 'apollo-boost'

const apolloClient = new ApolloClient({
  // You should use an absolute URL here
  uri: '/api/'
})

const apolloProvider = new VueApollo({
  defaultClient: apolloClient,
})

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
  apolloProvider,
  router
}).$mount('#app')
