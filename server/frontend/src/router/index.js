import Vue from "vue";
import VueRouter from "vue-router";

import { graud } from "./guard";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    component: () => import("@/containers/Default"),
    redirect: { name: "Dashboard" },
    name: "Root",
    beforeEnter: graud,
    children: [
      {
          path: "/_",
          name: "Dashboard",
          component: () => import("@/views/Dashboard")
      },
      {
        path: "/settings/",
        name: "Settings",
        component: () => import("@/containers/Settings"),
        redirect: { name: "Setting_Nodes" },
        children: [
          {
            path: "nodes/",
            name: "Setting_Nodes",
            component: () => import("@/views/settings/Nodes")
          },
          {
            path: "teams/",
            name: "Setting_Teams",
            component: () => import("@/views/settings/Teams")
          },
          {
            path: "challenges/",
            name: "Setting_Challenges",
            component: () => import("@/views/settings/Challenges")
          },
          {
            path: "keys/",
            name: "Setting_Keys",
            component: () => import("@/views/settings/Keys")
          },
        ]
      },
      {
        path: "/node/:id",
        name: "Node",
        props: true,
        component: () => import("@/views/Node")
      }
    ]
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/authentication/Login")
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