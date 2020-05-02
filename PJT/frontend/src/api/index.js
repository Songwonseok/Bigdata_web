import axios from "axios";

// const apiUrl = "https://i02a108.p.ssafy.io/api";
const apiUrl = "http://localhost:8000/api";


export default {
  getStores(params) {
    return axios.get(`${apiUrl}/stores`, {
      params,
    });
  },
  signUp(params) {
    return axios.post(`${apiUrl}/auth/join/`, params);
  },
  login(params) {
    return axios.post(`${apiUrl}/auth/login/`, params);
  },
  getUser(params) {
    return axios.get(`${apiUrl}/user?user=${params}`);
  },
  userUpdate(id, params) {
    return axios.post(`${apiUrl}/users/change`, params);
  },
  userDelete(params) {
    return axios.delete(`${apiUrl}/user/${params}`);
  },
  storeReviews(params) {
    return axios.get(`${apiUrl}/review`, {
      params,
    });
  },
  getMenu(params) {
    return axios.get(`${apiUrl}/menu`, {
      params,
    });
  },
  writeReview(params){
    return axios.post(`${apiUrl}/review`,params);
  },
  adminCount(){
    return axios.get(`${apiUrl}/admin/count`);
  },
  editReview(params){
    return axios.put(`${apiUrl}/review/${params.id}`,params);
  },
  removeReview(params){
    return axios.delete(`${apiUrl}/review/${params.id}`,params);
  },
  getBhour(params){
    return axios.get(`${apiUrl}/bhour?store=${params.store}`,params);
  },
  getAdminReview(params){
    return axios.get(`${apiUrl}/ad?page=${params.page}&page_size=${params.page_size}`)
  },
  getAdminUser(params){
    return axios.get(`${apiUrl}/adminuser?limit=${params.limit}&offset=${params.offset}`)
  },
  getTFIDF(params){
    return axios.get(`${apiUrl}/stores?id=${params.store}&recomm=${params.store}`,params)
  },
  postAccPer(params){
    return axios.post(`${apiUrl}/admin/user/change`,params)
  },
  postReviewChange(params){
    return axios.post(`${apiUrl}/admin/review/change`,params)
  }
};
