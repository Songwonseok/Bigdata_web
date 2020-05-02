import Home from "@/views/Home";
import Login from "@/views/Login";
import SignUp from "@/views/SignUp";
import MyPage from "@/views/MyPage";
import UserUpdate from "@/views/UserUpdate";
import Search from "@/views/Search";
import StoreKNN from "@/views/StoreKNN";
import Logout from "@/views/Logout";

import StoreDetail from "@/views/StoreDetail";
import AdminHome from "@/views/AdminHome";
import AdminReview from "@/views/AdminReview";
import AdminUser from "@/views/AdminUser";
import AdminStore from "@/views/AdminStore";
import AdminStoreDetail from "@/views/AdminStoreDetail"
import About from "@/views/store/about"
import Reviews from "@/views/store/reviews"
import Recommand from "@/views/store/recommand"


export default [
  {
    path: "*",
    redirect: "/",
  },
  {
    path: "/",
    component: Home,
    name: "home",
  },
  {
    path: "/login",
    component: Login,
    name: "login",
  },
  {
    path: "/logout",
    component: Logout,
    name: "logout",
  },
  {
    path: "/signup",
    component: SignUp,
    name: "signup",
  },
  {
    path: "/mypage",
    component: MyPage,
    name: "mypage",
  },
  {
    path: "/userUpdate",
    component: UserUpdate,
    name: "userUpdate",
  },
  {
    path: "/search",
    component: Search,
    name: "search",
  },
  {
    path: "/storeKNN",
    component: StoreKNN,
    name: "storeKNN",
  }
  ,
  {
    path: "/storeDetail/:id",
    component: StoreDetail,
    name: "storeDetail",
    children: [
      {
        path: "about",
        component: About,
        name: "about",
      },
      {
        path: "reviews",
        component: Reviews,
        name: "reviews",
      },
      {
        path: "recommand",
        component: Recommand,
        name: "recommand",
      }
    ]
  },
  {
    path:"/admin/home",
    component: AdminHome,
    name: "adminHome"
  },
  {
    path:"/admin/review",
    component: AdminReview,
    name: "adminReview"
  },
  {
    path:"/admin/user",
    component: AdminUser,
    name: "adminUser"
  },
  {
    path:"/admin/store",
    component: AdminStore,
    name: "adminStore"
  },{
    path:"/admin/store/:id",
    component: AdminStoreDetail,
    name: "adminStoreDetail"
  }
];
