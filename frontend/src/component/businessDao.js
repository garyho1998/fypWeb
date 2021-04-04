import config from "../config/config.json";
import axios from "axios";

function getBusinessMatch() {
  let url = "/businessMatch";
  return axios
    .get(config.SERVER_ENDPOINT + url)
    .then((res) => {
      return res.data.data;
    })
    .catch((err) => {
      console.log("API ERROR");
    });
}
function getSolutionMatch(businessID) {
  let url = "/solutionMatch?id=" + businessID;
  return axios
    .get(config.SERVER_ENDPOINT + url)
    .then((res) => {
      return res.data.data;
    })
    .catch((err) => {
      console.log("API ERROR");
    });
}

function getSolution(solutionID) {
  let url = "/it_solution_one?id=" + solutionID;
  return axios
    .get(config.SERVER_ENDPOINT + url)
    .then((res) => {
      return res.data.data;
    })
    .catch((err) => {
      console.log("API ERROR");
    });
}

export { getBusinessMatch, getSolutionMatch, getSolution };
