import config from "../config/config.json";
import axios from "axios";

async function getNewBusinessMatch(paragraph) {
  let url = "/newbusinessMatch?paragraph=" + paragraph;
  return axios
    .get(config.SERVER_ENDPOINT + url)
    .then((res) => {
      // console.log("res.data.data", res.data.data);
      return res.data.data;
    })
    .catch((err) => {
      console.log("API ERROR");
    });
}
export { getNewBusinessMatch };
