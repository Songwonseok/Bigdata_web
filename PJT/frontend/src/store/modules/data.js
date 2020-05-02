import api from "../../api";
import router from "../../router";

// initial state
const state = {
  userCount: "",
  storeCount: "",
  reviewCount: "",
  resultPage: "1",
  storeSearchList: [],
  storeReviewList: [],
  storeMenuList: [],
  KNNStoreList: [],
  TFIDFStoreList: [],
  bhour: [],
  store: {
    id: "",
    name: "",
    branch: "",
    area: "",
    tel: "",
    address: "",
    lat: 0.0,
    lng: 0.0,
    categories: [],
    image: "",
    dist: 0,
  },
  review: {
    id: "",
    total_score: 0,
    content: "",
    reg_time: "",
    store_id: "",
    user_id: "",
  },
  currentUser: {
    user: {
      id: "",
      username: "",
      email: "",
    },
    token: "",
    age: "",
    gender: "",
  },
  menu: {
    id: "",
    menu_name: "",
    price: 0,
    store_id: "",
  },
  adminUser: [],
  adminReview: [],
  userLat: 0,
  userLng: 0,
  womenDefault: "https://hotemoji.com/images/emoji/e/1yq83231aqlcde.png",
  menDefault: "https://hotemoji.com/images/emoji/3/1yq8323jqiio3.png",
  is_superuser: false,
};
function getDistanceFromLatLonInKm(lat1, lng1, lat2, lng2) {
  var r = 6371; //지구의 반지름(km)
  var dLat = (lat2 - lat1) * 92;
  var dLng = (lng2 - lng1) * 114;
  var a = Math.sqrt(Math.pow(dLat, 2) + Math.pow(dLng, 2));
  return a;
}

// actions
const actions = {
  async getStores({ commit }, params) {
    const append = params.append;
    const resp = await api.getStores(params);
    let stores = resp.data.results.map((d) => ({
      id: d.id,
      name: d.store_name,
      branch: d.branch,
      area: d.area,
      tel: d.tel,
      address: d.address,
      lat: d.latitude,
      lng: d.longitude,
      categories: d.category_list,
      image: d.image,
    }));
    stores.forEach((el) => {
      el.dist = getDistanceFromLatLonInKm(
        el.lat,
        el.lng,
        this.state.userLat,
        this.state.userLng
      );
    });
    await stores.sort(function(a, b) {
      return a.dist < b.dist ? -1 : a.dist > b.dist ? 1 : 0;
    });
    if (append && resp.data.next !== "null") {
      commit("addStoreSearchList", stores);
    } else {
      commit("setStoreSearchList", stores);
    }
    commit("setResultPage", resp.data.next);
  },
  async getUserLoc({ commit }, params) {},
  async getOneStore({ commit }, params) {
    const resp = await api.getStores(params);
    const storeInfo = resp.data.results.map((d) => ({
      id: d.id,
      name: d.store_name,
      branch: d.branch,
      area: d.area,
      tel: d.tel,
      address: d.address,
      lat: d.latitude,
      lng: d.longitude,
      categories: d.category_list,
      image: d.image,
    }));
    commit("setStoreInfo", storeInfo);
  },

  async login({ commit }, params) {
    var loginSuccess = true;
    const resp = await api.login(params).catch(() => {
      // console.log(error);
      alert("아이디 또는 비밀번호가 틀렸습니다.");
      loginSuccess = false;
    });
    if (loginSuccess) {
      const userInfo = {
        id: resp.data.user.id,
        username: resp.data.user.username,
        email: resp.data.user.email,
        token: resp.data.token,
      };
      commit("setCurrentUser", userInfo);
      if (state.currentUser.token !== "") {
        sessionStorage.userId = state.currentUser.id;
        commit("clearKNNStore");
        alert("로그인 성공");
        router.push("home");
      }
    }
  },
  async adminLogin({ commit }, params) {
    var loginSuccess = true;
    const resp = await api.login(params).catch((error) => {
      console.log(error);
      alert("아이디 또는 비밀번호가 틀렸습니다.");
      loginSuccess = false;
    });
    if (loginSuccess) {
      if (resp.data.user.is_superuser) {
        console.log(resp);

        const userInfo = {
          id: resp.data.user.id,
          username: resp.data.user.username,
          email: resp.data.user.email,
          token: resp.data.token,
        };
        commit("setCurrentUser", userInfo);
        if (state.currentUser.token !== "") {
          console.log("CurrentUser?");
          console.log(state.currentUser);
          alert("관리자 로그인 성공");
          commit("setSuper");
          router.push("/admin/home");
        }
      } else {
        alert("관리자가 아닙니다.");
        loginSuccess = false;
      }
    }
  },

  async logout({ commit }) {
    console.log("Logout called");
    commit("clearCurrentUser");
  },

  async signUp({ commit }, params) {
    await api
      .signUp(params)
      .then(
        alert("회원가입 성공. 다시 로그인 해주세요."),
        router.push("/login")
      )
      .catch(() => {
        // console.log(exp);

        alert("회원가입 오류");
        router.push("/signUp");
      });
  },

  async getUser({ commit }, params) {
    await api.getUser(params).then(function(response) {
      commit("setCurrentUserData", response.data.results[0]);
    });
  },

  async userUpdate({ commit }, params) {
    await api
      .userUpdate(state.currentUser.user.id, params)
      .then(alert("정보 수정 성공."), router.push("home"))
      .catch(() => {
        // console.log(exp);
        alert("정보 수정 오류");
        router.push("/userUpdate");
      });
  },

  async userDelete({ commit }, params) {
    await api
      .userDelete(params)
      .then(
        alert("회원탈퇴 성공."),
        commit("clearCurrentUser"),
        router.push("home")
      )
      .catch(() => {
        // console.log(exp);
        alert("회원탈퇴 오류");
      });
  },

  async storeReviews({ commit }, params) {
    let append = params.append;
    const resp = await api.storeReviews(params);
    const reivews = resp.data.results.map((d) => ({
      id: d.id,
      total_score: d.score,
      content: d.content,
      reg_time: d.reg_time,
      store_id: d.store,
      user_id: d.user,
    }));

    if (append && JSON.stringify(resp.data.next) !== "null") {
      commit("addReviewList", reivews);
    } else {
      commit("setReviewList", reivews);
    }
  },

  async storeMenu({ commit }, params) {
    const resp = await api.getMenu(params);
    const menus = resp.data.results.map((d) => ({
      id: d.id,
      menu_name: d.menu_name,
      price: d.price,
      store_id: d.store_id,
    }));
    commit("setMenuList", menus);
  },

  async createReview({ commit }, params) {
    await api.writeReview(params).catch(() => {
      router.go(-1);
    });
  },
  async editReview({ commit }, params) {
    await api.editReview(params);
  },
  async adminCount({ commit }) {
    await api
      .adminCount()
      .then((Response) => commit("setAdminCount", Response.data));
  },
  async deleteReivew({ commit }, params) {
    await api.deleteReivew(params).then(/*console.log("삭제완료")*/);
  },

  async deleteReview({ commit }, params) {
    await api.removeReview(params).then(/*console.log("삭제완료")*/);
  },
  async getKNN({ commit }, params) {
    const resp = await api.getStores(params);
    let stores = resp.data.results.map((d) => ({
      id: d.id,
      name: d.store_name,
      branch: d.branch,
      area: d.area,
      tel: d.tel,
      address: d.address,
      lat: d.latitude,
      lng: d.longitude,
      categories: d.category_list,
      image: d.image,
    }));
    stores.forEach((el) => {
      el.dist = getDistanceFromLatLonInKm(
        el.lat,
        el.lng,
        this.state.userLat,
        this.state.userLng
      );
    });
    await stores.sort(function(a, b) {
      return a.dist < b.dist ? -1 : a.dist > b.dist ? 1 : 0;
    });
    commit("setKNNStore", stores);
  },
  async storeBhour({ commit }, params) {
    const resp = await api.getBhour(params);
    const bhours = resp.data.results.map((d) => ({
      id: d.id,
      start_time: d.start_time,
      end_time: d.end_time,
      etc: d.etc,
      store: d.store,
    }));
    commit("fetchBhour", bhours);
  },
  async getAdminUser({ commit }, params) {
    await api.getAdminUser(params).then((Response) => {
      console.log(Response.data.results);
      commit("setAdminUser", Response.data.results);
    });
  },
  async getAdminReview({ commit }, params) {
    await api.getAdminReview(params).then((Response) => {
      console.log(Response.data.results);
      commit("setAdminReview", Response.data.results);
    });
  },
  async storeRecomm({ commit }, params) {
    const resp = await api.getTFIDF(params);
    let stores = resp.data.results.map((d) => ({
      id: d.id,
      name: d.store_name,
      branch: d.branch,
      area: d.area,
      tel: d.tel,
      address: d.address,
      lat: d.latitude,
      lng: d.longitude,
      categories: d.category_list,
      image: d.image,
    }));
    stores.forEach((el) => {
      el.dist = getDistanceFromLatLonInKm(
        el.lat,
        el.lng,
        this.state.userLat,
        this.state.userLng
      );
    });
    await stores.sort(function(a, b) {
      return a.dist < b.dist ? -1 : a.dist > b.dist ? 1 : 0;
    });
    commit("fetchTF", stores);
  },
  async changeBlind({ commit }, params) {
    await api.postReviewChange(params);
  },
  async changePer({ commit }, params) {
    await api.postAccPer(params);
  },
};

// mutations
const mutations = {
  setStoreSearchList(state, stores) {
    state.storeSearchList = stores.map((s) => s);
  },
  addStoreSearchList(state, stores) {
    state.storeSearchList = state.storeSearchList.concat(stores);
  },
  setResultPage(state, url) {
    state.resultPage = new URL(url).searchParams.get("page");
  },
  setReviewList(state, reviews) {
    state.storeReviewList = reviews.map((s) => s);
  },
  addReviewList(state, reviews) {
    state.storeReviewList = state.storeReviewList.concat(reviews);
  },
  setStoreInfo(state, storeInfo) {
    // 스토어 id로 정보
    state.store = storeInfo[0];
  },
  setMenuList(state, menus) {
    state.storeMenuList = menus.map((s) => s);
  },
  setCurrentUser(state, userInfo) {
    state.currentUser = userInfo;
    sessionStorage.accessToken = userInfo.token;
  },
  setCurrentUserData(state, data) {
    state.currentUser = data;
  },
  clearCurrentUser(state) {
    // console.log("로그인 정보 초기화");
    state.currentUser.token = "";
    state.currentUser.id = "";
    sessionStorage.clear();
  },
  removeOneReview(state, payload) {
    state.storeReviewList.splice(payload, 1);
  },
  clearStoreList(state) {
    console.log("초기화");
    console.log(state.storeSearchList);
    state.storeSearchList = [];
  },
  setAdminCount(state, stores) {
    console.log(stores);
    state.userCount = stores.userCount;
    state.reviewCount = stores.reviewCount;
    state.storeCount = stores.storeCount;
  },
  setKNNStore(state, stores) {
    state.KNNStoreList = stores.map((s) => s);
  },
  clearKNNStore(state) {
    state.KNNStoreList = [];
  },
  fetchBhour(state, bhours) {
    state.bhour = bhours.map((s) => s);
  },
  fetchTF(state, stores) {
    state.TFIDFStoreList = stores.map((s) => s);
  },
  setAdminUser(state, payload) {
    state.adminUser = payload;
  },
  setAdminReview(state, payload) {
    state.adminReview = payload;
  },
  setSuper(state) {
    state.is_superuser = true;
  },
};

const getters = {
  getCurrentUser() {
    return state.currentUser;
  },
  getReviewCount() {
    return state.storeReviewList.length;
  },
  getReviewAvg() {
    let sum = 0;
    const list = state.storeReviewList;
    if (list.length == 0) return 0;
    for (let i = 0; i < list.length; i++) {
      sum += list[i].total_score;
    }
    let ret = (sum / list.length).toFixed(1) * 1;
    return ret;
  },
  getScoreCount() {
    const scoreCounts = {
      one: 0,
      two: 0,
      three: 0,
      four: 0,
      five: 0,
    };
    const list = state.storeReviewList;
    for (let i = 0; i < list.length; i++) {
      switch (list[i].total_score) {
        case 1:
          scoreCounts.one++;
          break;
        case 2:
          scoreCounts.two++;
          break;
        case 3:
          scoreCounts.three++;
          break;
        case 4:
          scoreCounts.four++;
          break;
        case 5:
          scoreCounts.five++;
          break;
      }
    }
    const chartData = [
      ["", "리뷰 수"],
      ["5.0", scoreCounts.five],
      ["4.0", scoreCounts.four],
      ["3.0", scoreCounts.three],
      ["2.0", scoreCounts.two],
      ["1,0", scoreCounts.one],
    ];

    return chartData;
  },
};

export default {
  namespaced: true,
  state,
  actions,
  mutations,
  getters,
};
