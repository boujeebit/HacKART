import Vue from "vue";
import VueRouter from "vue-router";

// import { graud, superusergraud } from "./guards";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    component: () => import("@/containers/Default"),
    redirect: { name: "Dashboard" },
    name: "Root",
    //   beforeEnter: graud,
    children: [
    {
        path: "/_",
        name: "Dashboard",
        component: () => import("@/views/Dashboard")
    }
    ]
  },
  {
    path: "*",
    redirect: { name: "Dashboard" },
    component: {
    render(c) {
        return c("router-view");
    }
    }
  }
]

const router = new VueRouter({
  mode: "history",
  routes
})

export default router